import sys

if sys.version_info[:2] >= (3, 9):
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "AttributionQuality"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError


from attribution_quality.gradcam import (GradCAM, GradCAMPlusPlus, XGradCAM, GradCAMElementWise, HiResCAM, LayerCAM)
from attribution_quality.kernel_weighted import KernelWeighted
KWC = KernelWeighted  # alias
from attribution_quality.scorecam import ScoreCAM
