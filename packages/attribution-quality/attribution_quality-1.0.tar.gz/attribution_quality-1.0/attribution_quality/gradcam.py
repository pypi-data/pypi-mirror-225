"""
GradCAM flavours of explainability methods - The implementations are from the pytorch-grad-cam repository with slight alterations to enable 3D and segmentation-based usage.
https://github.com/jacobgil/pytorch-grad-cam/
"""
import numpy as np

from attribution_quality.base import BaseCAM
from attribution_quality.utils import classproperty


class GradCAM(BaseCAM):
    # Selvaraju et al. "Grad-cam: Visual explanations from deep networks via gradient-based localization." Proceedings of the IEEE international conference on computer vision. 2017.
    # https://doi.org/10.1109/ICCV.2017.74
    def get_cam_weights(self, input_tensor, target_layer, target_func, activations, grads):
        return np.mean(grads, axis=self.reduction_axes)

    @classproperty
    def name(self):
        return "GradCAM"

    @classproperty
    def abbr(self):
        "Abbreviation for the method. Used in filenames."
        return 'GC'

    @classproperty
    def uses_grad(self):
        return True


class GradCAMPlusPlus(BaseCAM):
    # Chattopadhay et al. "Grad-cam++: Generalized gradient-based visual explanations for deep convolutional networks." 2018 IEEE winter conference on applications of computer vision (WACV). IEEE, 2018.
    # https://doi.org/10.1109/WACV.2018.00097
    def get_cam_weights(self, input_tensor, target_layers, target_func, activations, grads):
        grads_pow2 = grads ** 2
        grads_pow3 = grads_pow2 * grads
        sum_activations = np.sum(activations, axis=self.reduction_axes)
        eps = 1e-6
        denom = (2 * grads_pow2 + sum_activations[self.space_expansion_slice] * grads_pow3 + eps)
        aij = np.divide(grads_pow2, denom, where=denom != 0, out=np.zeros_like(grads_pow2))
        aij = aij * (grads != 0)
        weights = np.maximum(grads, 0) * aij
        return np.sum(weights, axis=self.reduction_axes)

    @classproperty
    def name(self):
        return "GradCAM++"

    @classproperty
    def abbr(self):
        "Abbreviation for the method. Used in filenames."
        return 'GCP'

    @classproperty
    def uses_grad(self):
        return True


class XGradCAM(BaseCAM):
    # Ruigang Fu et al. "Axiom-based Grad-CAM: Towards Accurate Visualization and Explanation of CNNs." (2020).
    # https://www.bmvc2020-conference.com/conference/papers/paper_0631.html
    def get_cam_weights(self, input_tensor, target_layers, target_func, activations, grads):
        sum_activations = np.sum(activations, axis=self.reduction_axes)
        eps = 1e-7
        weights = grads * activations / (sum_activations[self.space_expansion_slice] + eps)
        return weights.sum(axis=self.reduction_axes)

    @classproperty
    def name(self):
        return "XGradCAM"

    @classproperty
    def abbr(self):
        "Abbreviation for the method. Used in filenames."
        return 'XGC'

    @classproperty
    def uses_grad(self):
        return True


class GradCAMElementWise(BaseCAM):
    # Jacob Gildenblat, et al. "PyTorch library for CAM methods." . (2021).
    # https://github.com/jacobgil/pytorch-grad-cam/blob/master/pytorch_grad_cam/grad_cam_elementwise.py
    def get_cam_image(self, input_tensor, target_layer, target_category, activations, grads, eigen_smooth=False):
        element_activations = np.maximum(grads * activations, 0)
        cam = element_activations.sum(axis=1)
        return cam

    @classproperty
    def name(self):
        return "GradCAMElementWise"

    @classproperty
    def abbr(self):
        "Abbreviation for the method. Used in filenames."
        return 'GCE'

    @classproperty
    def uses_grad(self):
        return True


class HiResCAM(BaseCAM):
    # Draelos et al. "Use HiResCAM instead of Grad-CAM for faithful explanations of convolutional neural networks". arXiv preprint arXiv:2011.08891. (2020).
    # https://doi.org/10.48550/arXiv.2011.08891
    def get_cam_image(self, input_tensor, target_layer, target_category, activations, grads, eigen_smooth=False):
        elementwise_activations = grads * activations
        cam = elementwise_activations.sum(axis=1)
        return cam

    @classproperty
    def name(self):
        return 'HiResCAM'

    @classproperty
    def abbr(self):
        "Abbreviation for the method. Used in filenames."
        return 'HRC'

    @classproperty
    def uses_grad(self):
        return True


class LayerCAM(BaseCAM):
    # Jiang et al. "LayerCAM: Exploring Hierarchical Class Activation Maps for Localization". IEEE Transactions on Image Processing 30. (2021): 5875-5888.
    # https://doi.org/10.1109/TIP.2021.3089943
    def get_cam_image(self, input_tensor, target_layer, target_category, activations, grads, eigen_smooth=False):
        spatial_weighted_activations = np.maximum(grads, 0) * activations
        cam = spatial_weighted_activations.sum(axis=1)
        return cam

    @classproperty
    def name(self):
        return 'LayerCAM'

    @classproperty
    def abbr(self):
        "Abbreviation for the method. Used in filenames."
        return 'LC'

    @classproperty
    def uses_grad(self):
        return True
