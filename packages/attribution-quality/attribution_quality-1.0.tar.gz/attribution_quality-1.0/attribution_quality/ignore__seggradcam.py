from functools import partial

import numpy as np
from skimage.measure import block_reduce
from skimage.transform import resize

from attribution_quality.base import BaseCAM
from attribution_quality.utils import classproperty


class SegXResCAM(BaseCAM):
    # Hasany et al. "Seg-XRes-CAM: Explaining Spatially Local Regions in Image Segmentation." Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Workshops. 2023.
    # https://openaccess.thecvf.com/content/CVPR2023W/XAI4CV/html/Hasany_Seg-XRes-CAM_Explaining_Spatially_Local_Regions_in_Image_Segmentation_CVPRW_2023_paper.html
    def __init__(self, model, target_layers, pooling='max', pool_size=4, **kwargs):
        super().__init__(model, target_layers, **kwargs)
        if pooling == 'none':
            self.pooling_op = lambda x: x
        else:
            op = np.max if pooling == 'max' else np.mean
            pool = [1, 1] + [pool_size] * self.n_spatial_dim
            self.pooling_op = partial(block_reduce, block_size=pool, func=op)

    def get_cam_weights(self, input_tensor, target_layer, targets, activations, grads):
        resize_kwargs = {'mode': 'edge', 'anti_aliasing': False, 'preserve_range': True, 'order': 0}
        grads = resize(self.pooling_op(grads), grads.size(), **resize_kwargs)
        # TODO

    @classproperty
    def name(self):
        return "SegXResCAM"

    @classproperty
    def abbr(self):
        "Abbreviation for the method. Used in filenames."
        return 'SXRC'

    @classproperty
    def uses_grad(self):
        return True


class SegGradCAM(SegXResCAM):
    # Kira Vinogradova et al. "Towards Interpretable Semantic Segmentation via Gradient-weighted Class Activation Mapping." Proceedings of the AAAI Conference on Artificial Intelligence. 2020.
    # https://doi.org/10.1609/aaai.v34i10.7244
    def __init__(self, model, target_layers, **kwargs):
        super().__init__(model, target_layers, pooling='none', pool_size=1, **kwargs)

    @classproperty
    def name(self):
        return "SegGradCAM"

    @classproperty
    def abbr(self):
        "Abbreviation for the method. Used in filenames."
        return 'SGC'

    @classproperty
    def uses_grad(self):
        return True
