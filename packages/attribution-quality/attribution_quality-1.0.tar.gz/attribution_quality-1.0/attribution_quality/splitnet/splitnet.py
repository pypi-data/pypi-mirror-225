from typing import Callable, Optional, Union

import torch


class SplitNet:
    """Base class for networks that can be run in two halves"""
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
        self.model = model
        self.forward = self.model.forward
        self.split_point = split_point
        self.active = False
        self.skips = []
        self._encoding_layers = None
        self._bottleneck_layers = None
        self._decoding_layers = None
        self.output_activation = output_activation

    def __call__(self, *args, **kwargs):
        return self.model(*args, **kwargs)

    def clear_stored(self):
        self.skips = [None for _ in self.skips]
        self.active = False

    def set_split_point(self, split_point):
        self.clear_stored()
        self.split_point = split_point

    @property
    def target_layer(self):
        raise NotImplementedError('This should be implemented by a subclass')

    def first_half(self, x: torch.Tensor, run_target: bool = True):
        raise NotImplementedError('This should be implemented by a subclass')

    def second_half(self, x: torch.Tensor, run_target: bool = False):
        raise NotImplementedError('This should be implemented by a subclass')

    def _prep_splits(self):
        raise NotImplementedError('This should be implemented by a subclass')

    @property
    def encoding_layers(self):
        if self._encoding_layers is None:
            self._prep_splits()
        return self._encoding_layers

    @property
    def bottleneck_layers(self):
        if self._bottleneck_layers is None:
            self._prep_splits()
        return self._bottleneck_layers

    @property
    def decoding_layers(self):
        if self._decoding_layers is None:
            self._prep_splits()
        return self._decoding_layers

    def list_split_points(self):
        return self.encoding_layers + self.bottleneck_layers + self.decoding_layers

    @property
    def num_split_points(self):
        return len(self.list_split_points())

    # NOTE - Added for BaseCAM compatability
    def eval(self):
        self.model = self.model.eval()
        return self

    def cuda(self, *args, **kwargs):
        self.model = self.model.cuda(*args, **kwargs)
        return self

    def zero_grad(self, set_to_none: bool = False):
        self.model.zero_grad(set_to_none=set_to_none)

    def __getattr__(self, attr):
        if self.model is not None and hasattr(self.model, attr):
            return getattr(self.model, attr)
        else:
            raise AttributeError('SplitNet has no attribute {}'.format(attr))
