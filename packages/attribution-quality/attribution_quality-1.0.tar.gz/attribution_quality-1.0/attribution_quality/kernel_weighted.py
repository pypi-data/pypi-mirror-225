import warnings

import torch
import tqdm.auto as tqdm

from attribution_quality.base import BaseCAM
from attribution_quality.splitnet import SplitNet, Split_nnUNet
from attribution_quality.utils import to_cuda, to_numpy, classproperty


class KernelWeighted(BaseCAM):
    def __init__(self,
                 model,
                 target_layers,
                 batch_size=4,
                 use_cuda=torch.cuda.is_available(),
                 allow_splitnet=True,
                 n_spatial_dim=3,
                 verbose=0, **kwargs):
        if allow_splitnet:
            type_string = str(type(model))
            if 'nnunet' in type_string and 'Generic_UNet' in type_string:
                model = Split_nnUNet(model)
            else:
                warnings.warn('Could not find SplitNet for model type: ' + type_string + '. This will likely lead to slower performance.')
        super().__init__(model, target_layers, use_cuda=use_cuda, uses_gradients=False,
                         rescale_output_range=False,
                         remove_negative=False, magnitude_activations=True,
                         rescale_activations=True,
                         n_spatial_dim=n_spatial_dim, batch_size=batch_size, verbose=verbose, **kwargs)

    def get_cam_weights(self, input_tensor, target_layer, target_func, activations, grads):
        if isinstance(self.model, SplitNet):
            return self.get_splitnet_cam_weights(input_tensor, target_layer, target_func, activations, grads)
        torch.cuda.empty_cache()
        self.activations_and_grads.release()
        with torch.no_grad():
            if self.cuda:
                input_tensor = to_cuda(input_tensor)
            with self.amp_context(device_type='cuda', dtype=torch.float16):
                outputs = self.model(input_tensor)
                outputs = self.activation_func(outputs)
            outputs = target_func(outputs)
            baseline_weight = 1. / torch.sum(outputs, self.sample_reduction_axes)

            # NOTE - Conv layers use output channels as axis 0 in the weight, while Transpose Conv layers use output channels as axis 1
            if 'Transpose' in str(type(target_layer)):
                output_axis = 1
            else:
                output_axis = 0

            kernel = torch.clone(target_layer.weight).detach()
            # empty_kernel = torch.empty(kernel.shape, dtype=torch.float32)
            # torch.nn.init.xavier_uniform_(empty_kernel)
            empty_kernel = torch.zeros(kernel.shape, dtype=torch.float32)
            if self.cuda:
                empty_kernel = to_cuda(empty_kernel)

            weights = torch.zeros([input_tensor.shape[0], kernel.shape[output_axis]])
            idx_slice = [slice(None) for _ in range(kernel.ndim)]
            if self.verbose == 2:
                iterator = tqdm.trange(kernel.shape[output_axis], leave=False)
            else:
                iterator = range(kernel.shape[output_axis])

            for idx in iterator:
                temp_kernel = torch.clone(kernel).detach()
                idx_slice[output_axis] = idx
                temp_kernel[idx_slice] = empty_kernel[idx_slice]
                target_layer.weight = torch.nn.Parameter(temp_kernel, requires_grad=False)
                with self.amp_context(device_type='cuda', dtype=torch.float16):
                    dependent_pred = self.model(input_tensor)
                    dependent_pred = self.activation_func(dependent_pred)
                dependent_pred = target_func(dependent_pred)
                dependent_contrib = torch.sum(outputs - torch.minimum(dependent_pred, outputs), dim=self.sample_reduction_axes, keepdim=True)

                temp_kernel = torch.clone(empty_kernel).detach()
                temp_kernel[idx_slice] = kernel[idx_slice]
                target_layer.weight = torch.nn.Parameter(temp_kernel, requires_grad=False)
                with self.amp_context(device_type='cuda', dtype=torch.float16):
                    independent_pred = self.model(input_tensor)
                    independent_pred = self.activation_func(independent_pred)
                independent_pred = target_func(independent_pred)
                independent_contrib = torch.sum(torch.minimum(independent_pred, outputs), dim=self.sample_reduction_axes, keepdim=True)

                weight = (dependent_contrib * independent_contrib) * baseline_weight
                weight = weight.view(input_tensor.shape[0], -1)
                weights[:, idx] = weight

            target_layer.weight = torch.nn.Parameter(kernel)
        return to_numpy(weights)

    def get_splitnet_cam_weights(self, input_tensor, target_layer, target_func, activations, grads):
        torch.cuda.empty_cache()
        self.model.set_split_point(target_layer)
        self.activations_and_grads.release()
        with torch.no_grad():
            with self.amp_context(device_type='cuda', dtype=torch.float16):
                layer_activations = self.model.first_half(input_tensor, run_target=True)
                outputs = self.model.second_half(layer_activations, run_target=False)
                outputs = self.activation_func(outputs)
            outputs = target_func(outputs)
            baseline_weight = 1. / torch.sum(outputs, self.sample_reduction_axes)

            weights = torch.zeros([input_tensor.shape[0], layer_activations.shape[1]])
            if self.verbose == 2:
                iterator = tqdm.trange(0, layer_activations.shape[1], self.batch_size, leave=False)
            else:
                iterator = range(0, layer_activations.shape[1], self.batch_size)
            for idx in iterator:
                batch_stop = min(layer_activations.shape[1], idx + self.batch_size)
                current_batch_size = batch_stop - idx
                temp_input = torch.clone(layer_activations).repeat(current_batch_size, 1, 1, 1, 1)
                for sub_idx in range(idx, batch_stop):
                    temp_input[sub_idx - idx, sub_idx] = 0
                with self.amp_context(device_type='cuda', dtype=torch.float16):
                    dependent_pred = self.model.second_half(temp_input, run_target=False)
                    dependent_pred = self.activation_func(dependent_pred)
                dependent_pred = target_func(dependent_pred)
                dependent_contrib = torch.sum(outputs - torch.minimum(dependent_pred, outputs), dim=self.sample_reduction_axes, keepdim=False)

                temp_input = torch.zeros_like(layer_activations).repeat(current_batch_size, 1, 1, 1, 1)
                for sub_idx in range(idx, batch_stop):
                    temp_input[sub_idx - idx, sub_idx] = layer_activations[:, sub_idx]
                with self.amp_context(device_type='cuda', dtype=torch.float16):
                    independent_pred = self.model.second_half(temp_input, run_target=False)
                    independent_pred = self.activation_func(independent_pred)
                independent_pred = target_func(independent_pred)
                independent_contrib = torch.sum(torch.minimum(independent_pred, outputs), dim=self.sample_reduction_axes, keepdim=False)

                assert torch.all(dependent_contrib >= 0) and torch.all(independent_contrib >= 0), 'Sanity check for bad values, likely caused by missing activation function'
                weight = (dependent_contrib * independent_contrib) * baseline_weight
                weight = weight.view(input_tensor.shape[0], -1)
                weights[:, idx:batch_stop] = weight
        return to_numpy(weights)

    @classproperty
    def name(self):
        return "KernelWeighted"

    @classproperty
    def abbr(self):
        "Abbreviation for the method. Used in filenames."
        return 'KWC'

    @classproperty
    def uses_grad(self):
        return False
