from typing import Callable, List, Tuple, Union

import numpy as np
import torch

from attribution_quality.hooks import ActsAndGrads
from attribution_quality.splitnet import SplitNet
from attribution_quality.utils import (getattr_recursive, resize_cam_image, to_cuda, to_numpy, to_torch, classproperty, DummyContext)


class BaseCAM:
    def __init__(self,
                 model: torch.nn.Module,
                 target_layers: Union[Union[torch.nn.Module, str], List[Union[torch.nn.Module, str]]],
                 use_cuda: bool = torch.cuda.is_available(),
                 compute_input_gradient: bool = False,  # not used in current methods, but kept in case it's needd
                 uses_gradients: bool = True,
                 n_spatial_dim: int = 3,
                 batch_size: int = 2,  # only used for ScoreCAM & KernelWeighted
                 rescale_output_range: bool = True,
                 remove_negative: bool = True,
                 magnitude_activations: bool = False,
                 rescale_activations: bool = False,
                 activation_func: Callable = None,
                 resize_to_input: bool = True,
                 allow_amp: bool = True,  # only used if `use_cuda` is True
                 verbose: bool = False) -> None:
        self.model = model.eval()
        if isinstance(target_layers, (str, torch.nn.Module)):
            self.target_layers = [target_layers]
        else:
            self.target_layers = target_layers
        if self.target_layers is not None and not isinstance(self.model, SplitNet):  # NOTE: SplitNet needs the strings to set breakpoints
            self.target_layers = [getattr_recursive(self.model, layer) if isinstance(layer, str) else layer for layer in self.target_layers]
        self.cuda = use_cuda
        if self.cuda:
            self.model = model.cuda()
        self.compute_input_gradient = compute_input_gradient
        self.uses_gradients = uses_gradients
        self.activations_and_grads = ActsAndGrads(
            self.model, self.target_layers, save_gradients=self.uses_gradients)
        self.verbose = verbose
        self.batch_size = batch_size
        self.resize_to_input = resize_to_input

        # These are parameters for specific activation handling
        self.rescale_output_range = rescale_output_range  # Occurs per-layer and then after aggregation
        self.remove_negative = remove_negative  # Occurs per-layer and then before aggregation
        self.magnitude_activations = magnitude_activations  # Applied to activations before they are multiplied by weights
        self.rescale_activations = rescale_activations  # Scale activations to have max=1 before they are multiplied by weights
        # This class assumes dim 0 = batch, dim 1 = channel, and dim 2+ are spatial
        self.space_dim = n_spatial_dim
        self.reduction_axes = tuple([i for i in range(2, self.space_dim + 2)])
        self.sample_reduction_axes = tuple([i for i in range(1, self.space_dim + 2)])
        self.space_expansion_slice = tuple([slice(None), slice(None)] + [None] * self.space_dim)
        self.channel_expansion_slice = tuple([slice(None), None] + [slice(None)] * self.space_dim)

        self.amp_context = torch.autocast if allow_amp and self.cuda else DummyContext
        if activation_func is None:
            self.activation_func = lambda x: x
        else:
            self.activation_func = activation_func

    def change_target_layers(self, target_layers: List[Union[torch.nn.Module, str]]):
        self.activations_and_grads.release()
        if isinstance(target_layers, (str, torch.nn.Module)):
            self.target_layers = [target_layers]
        else:
            self.target_layers = target_layers
        if not isinstance(self.model, SplitNet):  # NOTE: SplitNet needs the strings to set breakpoints
            self.target_layers = [getattr_recursive(self.model, layer) if isinstance(layer, str) else layer for layer in self.target_layers]
        self.activations_and_grads = ActsAndGrads(
            self.model, self.target_layers, save_gradients=self.uses_gradients)

    def get_cam_weights(self,
                        input_tensor: torch.Tensor,
                        target_layers: List[Union[torch.nn.Module, str]],
                        target_func: Callable,
                        activations: torch.Tensor,
                        grads: torch.Tensor) -> np.ndarray:
        raise Exception("Not Implemented")

    def get_cam_image(self,
                      input_tensor: torch.Tensor,
                      target_layer: torch.nn.Module,
                      target_func: Callable,
                      activations: torch.Tensor,
                      grads: torch.Tensor) -> np.ndarray:

        weights = self.get_cam_weights(input_tensor,
                                       target_layer,
                                       target_func,
                                       activations,
                                       grads)
        activations = to_numpy(activations)
        if self.magnitude_activations:
            activations = np.abs(activations)
        if self.rescale_activations:
            activations /= max(abs(np.min(activations)), np.max(activations))
        weighted_activations = weights[self.space_expansion_slice] * activations
        cam = weighted_activations.sum(axis=1)
        return cam

    def forward(self,
                input_tensor: torch.Tensor,
                targets: Union[Callable, int, list[int], np.ndarray, str, torch.Tensor, None] = 1,
                activation_func: Callable = None,
                return_components: bool = False) -> Union[list[np.ndarray], tuple[list[np.ndarray], list[np.ndarray]]]:
        """Generate CAM explanation for the target layers in this model for the given input tensor

        Parameters
        ----------
        input_tensor : torch.Tensor
            Input to explain the model's prediction for
        targets : Union[Callable, int, list[int], np.ndarray, str, torch.Tensor, None], optional
            The target(s) to be examined in the generated CAM (see Notes), by default 1
        activation_func : Callable, optional
            The activation function applied to the model output. If not `None`, this argument takes precedence over the `activation_func` passed during initialization. By default, None
        return_components : bool, optional
            If True, returns layer activations and weights as separate arrays rather than combining for the final CAM. Only works for CAM types that implement `get_cam_weights`. by default False

        Returns
        -------
        Union[np.ndarray, tuple[np.ndarray, np.ndarray]]
            A list containing either a CAM image for each target layer or a tuple of the layer activations and weights for each target layer if `return_components` is True

        Notes
        -----
        The `targets` parameter can be one of the following:
            * A callable that takes the model output as input and returns a tensor of the same shape as the model output
            * An integer or list/tuple of integers representing the class(es) to generate a CAM for (e.g. 1 for foreground in binary segmentation)
            * A numpy array or torch tensor that can be multiplied against the model output to mask unwanted values
                * ex. An array with the same shape as the model output, but with 0s for background and 1s for explanation targets
            * The string "argmax", which will generate a CAM for the "winning" class(es) (i.e. the class(es) with the highest model output at each spatial location)

        The resulting CAM(s) will be the same shape as the input tensor, with the channel dimension removed. The batch dimension is preserved to allow for batched inputs.
        """
        if self.target_layers is None:
            raise ValueError("`target_layers` must be set before calling forward")
        activation_func = self.activation_func if activation_func is None else activation_func
        if isinstance(input_tensor, np.ndarray):
            input_tensor = torch.from_numpy(input_tensor)
        if self.cuda:
            input_tensor = input_tensor.cuda()

        if self.compute_input_gradient:
            input_tensor = torch.autograd.Variable(input_tensor,
                                                   requires_grad=True)
        self.activations_and_grads.start()
        context = DummyContext if self.uses_gradients else torch.no_grad
        with context():
            outputs = self.activations_and_grads(input_tensor)
            if self.uses_gradients:
                self.model.zero_grad()
            if activation_func is not None:
                outputs = activation_func(outputs)

        if targets is None:
            model_target = outputs

            def target_func(x):
                return x
        elif isinstance(targets, (int, list, tuple)):
            # Only get gradient for specified classes
            targets = [targets] if isinstance(targets, int) else targets
            targets = tuple(targets)
            target_mask = torch.zeros_like(outputs)
            for target_category in targets:
                target_mask[:, target_category] = 1
            model_target = outputs * target_mask

            def target_func(x):
                return x[:, targets]
        elif isinstance(targets, str) and targets == 'argmax':
            # Only get gradient for "winning" classes
            target_mask = torch.argmax(outputs, dim=1)
            target_mask = torch.nn.functional.one_hot(target_mask, num_classes=outputs.shape[1])
            target_mask = torch.unsqueeze(target_mask, dim=1)
            target_mask = torch.transpose(target_mask, -1, 1)
            target_mask = torch.squeeze(target_mask, -1)
            model_target = outputs * target_mask

            def target_func(x):
                return x * target_mask
        elif isinstance(targets, (np.ndarray, torch.Tensor)):
            # Get gradient for regions that are part of the target mask
            targets = to_torch(targets)
            if self.cuda:
                targets = to_cuda(targets)
            # If targets is a spatial mask w/o batch or channel dimensions, add them
            while targets.ndim < outputs.ndim:
                targets = torch.unsqueeze(targets, dim=0)
            model_target = outputs * targets

            def target_func(x):
                return x * targets
        elif callable(targets):
            # Allow custom target functions to be passed
            model_target = targets(outputs)
            target_func = targets
        else:
            raise ValueError('Unknown target type. Must be one of [int, list[int], tuple[int], "argmax", np.ndarray, torch.Tensor]')

        loss = torch.sum(model_target)
        if self.uses_gradients:
            loss.backward(retain_graph=False)
        if return_components:
            return self.compute_components_per_layer(input_tensor, target_func)
        return self.compute_cam_per_layer(input_tensor, target_func)

    def get_target_size(self, input_tensor: torch.Tensor) -> Tuple[int, ...]:
        # This only needed to be reversed for opencv Height/Width usage
        return input_tensor.size()[2:]

    def compute_cam_per_layer(
            self,
            input_tensor: torch.Tensor,
            target_func: Callable) -> np.ndarray:
        activations_list = [a.cpu().data.numpy()
                            for a in self.activations_and_grads.activations]
        grads_list = [g.cpu().data.numpy()
                      for g in self.activations_and_grads.gradients]
        target_size = self.get_target_size(input_tensor)
        cam_per_target_layer = []
        # Loop over the saliency image from every layer
        for i in range(len(self.target_layers)):
            target_layer = self.target_layers[i]
            layer_activations = None
            layer_grads = None
            if i < len(activations_list):
                layer_activations = activations_list[i]
            if i < len(grads_list):
                layer_grads = grads_list[i]

            cam = self.get_cam_image(input_tensor,
                                     target_layer,
                                     target_func,
                                     layer_activations,
                                     layer_grads)
            if self.remove_negative:
                cam = np.maximum(cam, 0)
            if self.resize_to_input:
                cam = resize_cam_image(cam, target_size, rescale=self.rescale_output_range)
            cam_per_target_layer.append(cam[self.channel_expansion_slice])
        return cam_per_target_layer

    def compute_components_per_layer(
            self,
            input_tensor: torch.Tensor,
            target_func: Callable) -> tuple[np.ndarray, np.ndarray]:
        # NOTE - only works with methods that define get_cam_weights
        activations_list = [a.cpu().data.numpy()
                            for a in self.activations_and_grads.activations]
        grads_list = [g.cpu().data.numpy()
                      for g in self.activations_and_grads.gradients]
        activations = to_numpy(activations_list)
        weights_per_layer = []

        for i in range(len(self.target_layers)):
            target_layer = self.target_layers[i]
            layer_activations = None
            layer_grads = None
            if i < len(activations_list):
                layer_activations = activations_list[i]
            if i < len(grads_list):
                layer_grads = grads_list[i]
            weights = self.get_cam_weights(input_tensor,
                                           target_layer,
                                           target_func,
                                           layer_activations,
                                           layer_grads)
            weights_per_layer.append(weights)
        return activations, weights_per_layer

    def release(self):
        if hasattr(self, 'activations_and_grads'):
            self.activations_and_grads.release()

    def __call__(self, *args, **kwargs) -> np.ndarray:
        return self.forward(*args, **kwargs)

    def __del__(self):
        self.release()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.activations_and_grads.release()

    @classproperty
    def name(self):
        raise NotImplementedError('This should be implemented in the subclass')

    @classproperty
    def abbr(self):
        "Abbreviation for the method. Used in filenames."
        raise NotImplementedError('This should be implemented in the subclass')
