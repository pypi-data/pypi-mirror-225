import warnings
from typing import Callable, Optional, Union

import torch
from torch.nn import (Conv2d, Conv3d, ConvTranspose2d, ConvTranspose3d, Module, Sequential)

from attribution_quality.splitnet.splitnet import SplitNet
from attribution_quality.utils import getattr_recursive


class Split_nnUNet(SplitNet):
    """SplitNet for the v1 U-Net style nnUNet"""
    def __init__(self, model, split_point: Optional[str] = None, output_activation: Union[bool, Callable] = False):
        """Constructor for SplitNet

        Parameters
        ----------
        model : torch.nn.Module
            PyTorch model to wrap
        split_point : str, optional
            The layer to split on, by default None
        output_activation : Union[bool, Callable], optional
            Whether to run the output activation OR the output activation function, by default False

        Note
        ----
        If a Callable is provided for output_activation, it will be used instead of the model's default output activation
        """
        super().__init__(model, split_point=split_point, output_activation=output_activation)
        self.model = model
        self.skips = []
        if split_point is not None:
            self.set_split_point(split_point)
        self.active = False

    def set_split_point(self, split_point: str):
        self.clear_stored()
        self.split_name = split_point
        self.split_point = split_point.split('.')
        self.split_point = [int(item) if item.isdecimal() else item for item in self.split_point]
        if len(self.split_point) < 5:
            self.split_point += [0] * (5 - len(self.split_point))

    @property
    def target_layer(self):
        return getattr_recursive(self.model, self.split_name)

    def _prep_splits(self):
        self._encoding_layers, self._bottleneck_layers, self._decoding_layers, _ = decompose_nnunet(self.model, names_only=True)

    def first_half(self, x: torch.Tensor, run_target: bool = True):
        """Run the first half of the model

        Parameters
        ----------
        x : torch.Tensor
            Input data to the model
        run_target : bool, optional
            Whether to split before (True) or after (False) the target layer, by default True
        """
        if self.split_point is None:
            raise ValueError("Split point not set")
        self.skips = []
        for d in range(len(self.model.conv_blocks_context) - 1):
            if self.split_point[0] == 'conv_blocks_context' and self.split_point[1] == d:
                for block_idx in range(self.split_point[3]):
                    x = self.model.conv_blocks_context[d].blocks[block_idx](x)
                if run_target:
                    x = self.model.conv_blocks_context[d].blocks[self.split_point[3]](x)
                self.active = True
                return x
            else:
                x = self.model.conv_blocks_context[d](x)
            self.skips.append(x)
            if not self.model.convolutional_pooling:
                x = self.td[d](x)  # only pooling ops

        if self.split_point[0] == 'conv_blocks_context' and self.split_point[1] == len(self.model.conv_blocks_context) - 1:
            for seq_idx in range(self.split_point[2]):
                x = self.model.conv_blocks_context[-1][seq_idx](x)
            target_blocks = self.model.conv_blocks_context[-1][self.split_point[2]].blocks
            for block_idx in range(self.split_point[4]):
                x = target_blocks[block_idx](x)
            if run_target:
                x = target_blocks[self.split_point[4]](x)
            self.active = True
            return x
        else:
            x = self.model.conv_blocks_context[-1](x)

        for u in range(len(self.model.tu)):
            if self.split_point[0] == 'tu' and self.split_point[1] == u:
                if run_target:
                    x = self.model.tu[u](x)  # only a bare transpose conv or upsampling
                self.active = True
                return x
            else:
                x = self.model.tu[u](x)  # only a bare transpose conv or upsampling
            x = torch.cat((x, self.skips[-(u + 1)]), dim=1)
            self.skips[-(u + 1)] = None  # keep the place for indexing, but free memory
            if self.split_point[0] == 'conv_blocks_localization' and self.split_point[1] == u:
                for seq_idx in range(self.split_point[2]):
                    x = self.model.conv_blocks_localization[u][seq_idx](x)
                target_blocks = self.model.conv_blocks_localization[u][self.split_point[2]].blocks
                for block_idx in range(self.split_point[4]):
                    x = target_blocks[block_idx](x)
                if run_target:
                    x = target_blocks[self.split_point[4]](x)
                self.active = True
                return x
            else:
                x = self.model.conv_blocks_localization[u](x)
        x = self.model.seg_outputs[len(self.model.tu) - 1](x)
        if isinstance(self.output_activation, bool):
            if self.output_activation:
                # final_nonlin is identity in some cases where tta is expected - softmax after tta, so not part of model
                x = self.model.final_nonlin(x)
        else:
            # x = torch.nn.functional.softmax(x, dim=1)  # recommended for nnUNet if setting output_activation manually
            x = self.output_activation(x)
        return x

    def second_half(self, x: torch.Tensor, run_target: bool = False):
        """Run the second half of the model

        Parameters
        ----------
        x : torch.Tensor
            Result data from running `first_half`
        run_target : bool, optional
            Whether to run the target layer, by default False

        Note
        ----
        `run_target` should only be True if it was False in `first_half` and vice-versa
        """
        assert self.active, "First half of model must be run before second half"
        if self.split_point is None:
            raise ValueError("Split point not set")
        temp_skips = []
        for item in self.skips:
            if item is None:
                pass
            elif item.shape[0] != x.shape[0]:
                item = item.repeat(x.shape[0], 1, 1, 1, 1)
            temp_skips.append(item)
        # Iterate through the encoder
        if self.split_point[0] == 'conv_blocks_context' and self.split_point[1] < len(self.model.conv_blocks_context) - 1:
            conv_block = self.model.conv_blocks_context[self.split_point[1]].blocks[self.split_point[3]]
            if run_target:
                x = conv_block(x)

            # Iterate through the remaining blocks in the layer
            for block_idx in range(self.split_point[3] + 1, len(self.model.conv_blocks_context[self.split_point[1]].blocks)):
                x = self.model.conv_blocks_context[self.split_point[1]].blocks[block_idx](x)
            temp_skips.append(x)

            # Iterate through the remaining layers in the encoder
            for d in range(self.split_point[1] + 1, len(self.model.conv_blocks_context) - 1):
                x = self.model.conv_blocks_context[d](x)
                temp_skips.append(x)
                if not self.model.convolutional_pooling:
                    x = self.model.td[d](x)

        # Iterate through the bottleneck
        if self.split_point[0] == 'conv_blocks_context':
            if self.split_point[1] == len(self.model.conv_blocks_context) - 1:
                conv_block = self.model.conv_blocks_context[-1][self.split_point[2]].blocks
                if run_target:
                    x = conv_block[self.split_point[4]](x)

                for block_idx in range(self.split_point[4] + 1, len(conv_block)):
                    x = conv_block[block_idx](x)
                for seq_idx in range(self.split_point[2] + 1, len(self.model.conv_blocks_context[-1])):
                    x = self.model.conv_blocks_context[-1][seq_idx](x)
            else:
                # If we've already passed the split point, we can just run the whole layer
                x = self.model.conv_blocks_context[-1](x)

        # Start mid-layer in the decoder if needed
        if self.split_point[0] in ['tu', 'conv_blocks_localization']:
            u_start = self.split_point[1]
            if self.split_point[0] == 'tu':
                if run_target:
                    x = self.model.tu[self.split_point[1]](x)
                x = torch.cat((x, temp_skips[-(self.split_point[1] + 1)]), dim=1)
            if self.split_point[0] == 'conv_blocks_localization':
                conv_block = self.model.conv_blocks_localization[self.split_point[1]][self.split_point[2]].blocks
                if run_target:
                    x = conv_block[self.split_point[4]](x)

                for block_idx in range(self.split_point[4] + 1, len(conv_block)):
                    x = conv_block[block_idx](x)

                for seq_idx in range(self.split_point[2] + 1, len(self.model.conv_blocks_localization[self.split_point[1]])):
                    x = self.model.conv_blocks_localization[self.split_point[1]][seq_idx](x)
            else:
                x = self.model.conv_blocks_localization[self.split_point[1]](x)
        else:
            u_start = -1

        # Iterate through the decoder
        for u in range(u_start + 1, len(self.model.tu)):
            x = self.model.tu[u](x)
            x = torch.cat((x, temp_skips[-(u + 1)]), dim=1)
            x = self.model.conv_blocks_localization[u](x)
        x = self.model.seg_outputs[len(self.model.tu) - 1](x)
        if isinstance(self.output_activation, bool):
            if self.output_activation:
                # final_nonlin is identity in some cases where tta is expected - softmax after tta, so not part of model
                x = self.model.final_nonlin(x)
        else:
            # x = torch.nn.functional.softmax(x, dim=1)  # recommended for nnUNet if setting output_activation manually
            x = self.output_activation(x)
        return x


def _unstack_nnunet_layer(layer: Module, layer_string: str) -> list[dict]:
    results = []
    if isinstance(layer, Sequential):
        for b_idx in range(len(layer)):
            block = layer[b_idx]
            results.extend(_unstack_nnunet_layer(block, layer_string + f'.{b_idx}'))
    elif 'StackedConvLayers' in str(type(layer)):
        for b_idx, block in enumerate(layer.blocks):
            sublayer = layer.blocks[b_idx].conv
            sublayer_string = layer_string + f'.blocks.{b_idx}.conv'
            results.extend(_unstack_nnunet_layer(sublayer, sublayer_string))
    elif isinstance(layer, (Conv3d, Conv2d, ConvTranspose2d, ConvTranspose3d)):
        results.append({'name': layer_string, 'shape': layer.weight.shape, 'type': type(layer)})
    else:
        raise ValueError('Unset use case')
    return results


def decompose_nnunet(net: torch.nn.Module, assume_bottleneck=True, names_only: bool = False) -> tuple[list, list, list, list]:
    """Return the layer decomposition of a v1 nnUNet model

    Parameters
    ----------
    net : torch.nn.Module
        model to decompose
    assume_bottleneck : bool, optional
        Whether to treat the unmatched encoder block as a bottleneck layer, by default True
    names_only : bool, optional
        Whether to only return the layer names, by default False

    Returns
    -------
    tuple[list, list, list, list]
        [encoding_layers, bottleneck_layers, decoding_layers, skip_connections]

    Note
    ----
    nnUNet does not explicitly use a bottleneck, but there is an unmatched encoder block that is structurally equivalent
    """
    if 'Generic_UNet' not in str(type(net)):
        warnings.warn('Only Generic_UNet style nnUNet v1 models are currently supported - this method will likely fail')
    skip_src = []
    encoding_layers = []
    for d in range(len(net.conv_blocks_context) - 1):
        layer = net.conv_blocks_context[d]
        layer_string = f'conv_blocks_context.{d}'
        encoding_layers.extend(_unstack_nnunet_layer(layer, layer_string))
        skip_src.append(encoding_layers[-1])
        # NOTE - the net.td are just pooling ops

    bottleneck = _unstack_nnunet_layer(net.conv_blocks_context[-1], f'conv_blocks_context.{len(net.conv_blocks_context) - 1}')
    if not assume_bottleneck:
        encoding_layers.extend(bottleneck)
        bottleneck = []

    skips = []
    decoding_layers = []
    for u in range(len(net.tu)):
        layer = net.tu[u]
        if net.convolutional_upsampling:
            layer_string = f'tu.{u}'
            decoding_layers.extend(_unstack_nnunet_layer(layer, layer_string))
        cat_src = decoding_layers[-1]
        layer = net.conv_blocks_localization[u]
        layer_string = f'conv_blocks_localization.{u}'
        next_decoding = _unstack_nnunet_layer(layer, layer_string)
        decoding_layers.extend(next_decoding)
        skips.append({'src': [skip_src[-(u + 1)], cat_src], 'dst': next_decoding[0]})

    if names_only:
        encoding_layers = [item['name'] for item in encoding_layers]
        bottleneck = [item['name'] for item in bottleneck]
        decoding_layers = [item['name'] for item in decoding_layers]
        skips = [{'src': [subitem['name'] for subitem in item['src']], 'dst': item['dst']['name']} for item in skips]
    return encoding_layers, bottleneck, decoding_layers, skips
