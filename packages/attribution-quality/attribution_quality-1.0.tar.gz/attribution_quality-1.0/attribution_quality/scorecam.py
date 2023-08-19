"""ScoreCAM implemented for 3D"""
from functools import partial

import numpy as np
import torch
import tqdm.auto as tqdm

from attribution_quality.base import BaseCAM
from attribution_quality.utils import to_numpy, to_torch, classproperty, softmax


class ScoreCAM(BaseCAM):
    # Wang et al. "Score-CAM: Score-Weighted Visual Explanations for Convolutional Neural Networks." 2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW). 2020.
    # https://doi.org/10.1109/CVPRW50498.2020.00020
    def __init__(self, model, target_layers, batch_size=2, **kwargs):
        super().__init__(model, target_layers, uses_gradients=False, batch_size=batch_size, **kwargs)
        self.target_class = 1

    def get_cam_weights(self, input_tensor, target_layer, target_func, activations, grads):
        self.activations_and_grads.release()
        with torch.no_grad():
            upsample = partial(torch.nn.functional.interpolate, size=input_tensor.shape[2:], mode='trilinear' if self.space_dim != 2 else 'bilinear')

            activation_tensor = to_torch(activations)
            input_tensor = to_torch(to_numpy(input_tensor))

            upsampled: torch.Tensor = upsample(activation_tensor)
            maxs = upsampled.view(upsampled.size(0), upsampled.size(1), -1).amax(dim=-1)
            mins = upsampled.view(upsampled.size(0), upsampled.size(1), -1).amin(dim=-1)
            maxs = maxs[self.space_expansion_slice]
            mins = mins[self.space_expansion_slice]
            upsampled = (upsampled - mins) / (maxs - mins)
            upsampled = torch.nan_to_num(upsampled, nan=0.0, posinf=0.0, neginf=0.0)

            # both have shape: [batch, feature, channels, x, y, z]
            input_tensors = input_tensor[:, None] * upsampled[:, :, None]

            scores = []
            num_classes = None
            for tensor in input_tensors:
                iterator = range(0, tensor.size(0), self.batch_size)
                if self.verbose:
                    iterator = tqdm.tqdm(iterator, leave=False)
                for idx in iterator:
                    batch = tensor[idx: idx + self.batch_size]
                    with self.amp_context(device_type='cuda', dtype=torch.float16):
                        if self.cuda:
                            # Normally already cuda, but needed for amp
                            batch = batch.cuda()
                        output = self.activation_func(self.model(batch))
                    output = target_func(output)
                    output = to_numpy(output).astype(np.float32)
                    num_classes = num_classes or output.shape[1]
                    output = output.sum(axis=self.reduction_axes)
                    scores.append(output)
            scores = np.concatenate(scores, axis=0)
            scores = scores.reshape(num_classes, activations.shape[1])
            weights = softmax(scores, axis=0)
            return weights

    @classproperty
    def name(self):
        return "ScoreCAM"

    @classproperty
    def abbr(self):
        "Abbreviation for the method. Used in filenames."
        return 'SC'

    @classproperty
    def uses_grad(self):
        return False
