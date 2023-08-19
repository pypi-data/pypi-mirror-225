import os
import tempfile
from typing import Optional, Union

import numpy as np
import torch
from attribution_quality.optional_imports import SimpleITK as sitk
from attribution_quality.utils import quick_pred

if hasattr(sitk, 'is_dummy'):
    IMAGE_TYPE = np.ndarray
else:
    IMAGE_TYPE = Union[sitk.Image, np.ndarray]


def compare_entropy(image: IMAGE_TYPE, mask: Optional[IMAGE_TYPE] = None) -> float:
    """Compute the estimated entropy of an image or the relative entropy of a masked image

    Parameters
    ----------
    image : Union[sitk.Image, np.ndarray]
        Baseline image or image to compare
    mask : Optional[Union[sitk.Image, np.ndarray]], optional
        Optional mask to use when computing masked entropy, by default None

    Returns
    -------
    float
        The estimated entropy of the image or the relative entropy of the masked image
    """
    if isinstance(image, np.ndarray):
        image = np.squeeze(image)
    if isinstance(mask, np.ndarray):
        mask = np.squeeze(mask)
    with tempfile.TemporaryDirectory() as tmp_dir:
        if sitk is not None:
            sitk_image = image if isinstance(image, sitk.Image) else sitk.GetImageFromArray(image)
            sitk.WriteImage(sitk_image, os.path.join(tmp_dir, 'baseline.nii'))
            baseline_size = os.path.getsize(os.path.join(tmp_dir, 'baseline.nii'))
            sitk.WriteImage(sitk_image, os.path.join(tmp_dir, 'compressed.nii.gz'), True, -1)
            compressed_size = os.path.getsize(os.path.join(tmp_dir, 'compressed.nii.gz'))
        else:
            # Our work used SimpleITK, but the numpy compression also uses DEFLATE if required
            np.savez(image, os.path.join(tmp_dir, 'baseline.npy'))
            baseline_size = os.path.getsize(os.path.join(tmp_dir, 'baseline.npy'))
            np.savez_compressed(image, os.path.join(tmp_dir, 'compressed.npz'))
            compressed_size = os.path.getsize(os.path.join(tmp_dir, 'compressed.npz'))
    relative_entropy = compressed_size / baseline_size

    if mask is not None:
        masked_entropy = compare_entropy(image * mask)
        return masked_entropy / relative_entropy
    return relative_entropy


def run_label_stats(label_image: sitk.Image):
    """Short-cut method for running the SimpleITK LabelShapeStatisticsImageFilter"""
    label_filt = sitk.LabelShapeStatisticsImageFilter()
    label_filt.SetBackgroundValue(0)
    label_filt.SetComputeFeretDiameter(False)
    label_filt.SetComputePerimeter(False)
    label_filt.SetComputeOrientedBoundingBox(False)
    label_filt.Execute(label_image)
    return label_filt


def compute_cam_localization(cam_image: IMAGE_TYPE, full_label_image: IMAGE_TYPE, fg_idx=3, bg_idx=0, dbg_idx=2, cam_percentile=99, min_peak_size=100, max_centroid_dist=10, min_dbg_coverage=0.25, strong_dbg_coverage_count=3, dbg_median_coverage=0.75) -> tuple[float, float]:
    """Compute the Relative Foreground Attribution and External Peak Attribution for a given CAM

    Parameters
    ----------
    cam_image : Union[sitk.Image, np.ndarray]
        The CAM to evaluate
    full_label_image : Union[sitk.Image, np.ndarray]
        A labelmap of the source image with labels for the foreground (fg), background (bg), and discriminating background (dbg)
    fg_idx : int, optional
        The index of the fg label in `full_label_image`, by default 3
    bg_idx : int, optional
        The index of the bg label in `full_label_image`, by default 0
    dbg_idx : int, optional
        The index of the dbg label in `full_label_image`, by default 2
    cam_percentile : int, optional
        The lower percentile threshold for attribution peaks, by default 99
    min_peak_size : int, optional
        The minimum size for an object to be an attribution peak, by default 100
    max_centroid_dist : int, optional
        The maximum distance between an attribution peak centroid and dbg object centroid to be a "hit", by default 10
    min_dbg_coverage : float, optional
        The minimum percent of the attribution peak that must be dbg to be a "hit", by default 0.25
    strong_dbg_coverage_count : int, optional
        The minimum number of dbg objects an attribution peak must at least 90% cover to be considered a "hit", by default 3
    dbg_median_coverage : float, optional
        The minimum median percent covered of dbg objects that overlap the attribution peak for the peak to be a "hit", by default 0.75

    Returns
    -------
    float, float
        The Relative Foreground Attribution and External Peak Attribution scores
    """
    full_label_image = full_label_image if isinstance(full_label_image, sitk.Image) else sitk.GetImageFromArray(full_label_image)
    cam_image = cam_image if isinstance(cam_image, sitk.Image) else sitk.GetImageFromArray(cam_image)

    fg_label = full_label_image == fg_idx
    bg_label = full_label_image == bg_idx
    fg_cam = sitk.GetArrayViewFromImage(cam_image)[sitk.GetArrayFromImage(fg_label).astype(bool)]
    bg_cam = sitk.GetArrayViewFromImage(cam_image)[sitk.GetArrayFromImage(bg_label).astype(bool)]
    rel_fg_score = fg_cam.mean() - bg_cam.mean()

    dbg_label = full_label_image == dbg_idx
    dbg_cc = sitk.ConnectedComponent(dbg_label)
    dbg_stats = run_label_stats(dbg_cc)

    peak_image = cam_image > np.percentile(sitk.GetArrayViewFromImage(cam_image), cam_percentile)
    peak_image = peak_image * (1 - fg_label)
    peak_cc = sitk.ConnectedComponent(peak_image)
    peak_stats = run_label_stats(peak_cc)

    hit_peaks = 0
    missed_peaks = 0
    for peak_idx in peak_stats.GetLabels():
        if peak_stats.GetPhysicalSize(peak_idx) < min_peak_size:
            continue
        local_peak = peak_cc == peak_idx
        covered_dbg_cc = sitk.Mask(dbg_cc, local_peak)
        covered_dbg_stats = run_label_stats(covered_dbg_cc)
        covered_dbg = None
        dbg_coverage = []
        for dbg_item_idx in covered_dbg_stats.GetLabels():
            local_dbg_coverage = covered_dbg_stats.GetPhysicalSize(dbg_item_idx) / dbg_stats.GetPhysicalSize(dbg_item_idx)
            dbg_coverage.append(local_dbg_coverage)
            local_dbg = dbg_cc == dbg_item_idx
            covered_dbg = local_dbg if covered_dbg is None else covered_dbg + local_dbg
        if covered_dbg is None:
            missed_peaks += 1
            continue
        dbg_coverage = np.asarray(dbg_coverage)

        covered_dbg_stats = run_label_stats(covered_dbg)
        assert covered_dbg_stats.GetNumberOfLabels() == 1, 'There should only be 1 label here.'
        peak_center = np.asarray(peak_stats.GetCentroid(peak_idx))
        dbg_center = np.asarray(covered_dbg_stats.GetCentroid(1))
        centroid_distance = np.sqrt(np.sum((peak_center - dbg_center) ** 2))
        center_check = centroid_distance < max_centroid_dist

        local_covered_dbg = sitk.Mask(covered_dbg, local_peak)
        local_covered_dbg_stats = run_label_stats(local_covered_dbg)
        local_dbg_percent = local_covered_dbg_stats.GetPhysicalSize(1) / peak_stats.GetPhysicalSize(1)
        perc_check = local_dbg_percent > min_dbg_coverage

        cov_med_check = np.median(dbg_coverage) > dbg_median_coverage
        cov_count_check = (dbg_coverage > 0.9).sum() >= strong_dbg_coverage_count
        valid = center_check and (perc_check or cov_med_check or cov_count_check)
        hit_peaks += int(valid)

    if hit_peaks == 0:
        return rel_fg_score, 0
    else:
        return rel_fg_score, hit_peaks / (hit_peaks + missed_peaks)


def compute_masked_metrics(baseline_pred: np.ndarray, masked_pred: np.ndarray, mask: np.ndarray) -> tuple[float, float, float]:
    """Compute the Prediction Preserved, Image Preserved, and Excess Prediction from the baseline segmentation, masked segmentation, and CAM

    Parameters
    ----------
    baseline_pred : np.ndarray
        The baseline predicted segmentation
    masked_pred : np.ndarray
        The predicted segmentation of the image masked by the CAM
    mask : np.ndarray
        The CAM used to mask the image (rescaled to [0, 1])

    Returns
    -------
    tuple[float, float, float]
        The Prediction Preserved, Image Preserved, and Excess Prediction scores

    Raises
    ------
    ValueError
        The baseline segmentation cannot be empty

    Notes
    -----
    The `baseline_pred` should be the predicted segmentation when the image is fed to the model being investigated.
    The `masked_pred` should be the predicted segmentation when the CAM is rescaled to [0, 1], point-wise multiplied with the image, and fed to the model being investigated.
    The `mask` should be the CAM rescaled to [0, 1].
    """
    baseline_pred = np.asarray(baseline_pred).astype(np.float32)
    masked_pred = np.asarray(masked_pred).astype(np.float32)
    mask = np.asarray(mask).astype(np.float32)
    baseline_size = np.sum(baseline_pred)
    if baseline_size == 0:
        raise ValueError("Baseline prediction cannot be empty")
    pred_pres = np.minimum(baseline_pred, masked_pred).sum() / baseline_size
    image_pres = np.mean(mask)
    excess_pred = np.maximum(masked_pred - baseline_pred, 0).sum() / baseline_size
    return pred_pres, image_pres, excess_pred


def compute_masked_metrics_from_source(network: torch.nn.Module, input_image: np.ndarray, mask: np.ndarray) -> tuple[float, float, float]:
    """Wrapper method for `compute_masked_metrics` that take the model, input, and CAM as opposed to the baseline and masked predictions

    Parameters
    ----------
    network : torch.nn.Module
        The model being investigated
    input_image : np.ndarray
        The input image to the model
    mask : np.ndarray
        The CAM generated to explain the model's segmentation of `input_image`

    Returns
    -------
    tuple[float, float, float]
        The Prediction Preserved, Image Preserved, and Excess Prediction scores

    See Also
    --------
    attribution_quality.metrics.compute_masked_metrics
        Effectively the same method, but may work better when iterating over multiple masks since you can run the baseline prediction and CAM rescaling once rather than once per mask.
    """
    mask /= mask.max()
    baseline_pred = quick_pred(network, input_image)
    masked_pred = quick_pred(network, input_image, mask=mask)
    return compute_masked_metrics(baseline_pred, masked_pred, mask)


def compute_quality_score(network: torch.nn.Module, input_image: np.ndarray, cam_mask: np.ndarray, full_label_image: np.ndarray, localization_kwargs: Optional[dict] = None) -> tuple[float, tuple[float, float, float, float]]:
    """Compute the comprehensive Attribution Quality score for a given CAM

    Parameters
    ----------
    network : torch.nn.Module
        The model being investigated
    input_image : np.ndarray
        The input image to the model
    cam_mask : np.ndarray
        The CAM generated to explain the model's segmentation of `input_image`
    full_label_image : np.ndarray
        A labelmap of the source image with labels for the foreground (fg), background (bg), and discriminating background (dbg)
    localization_kwargs : Optional[dict], optional
        Optional keyword arguments for `compute_cam_localization`, by default None

    Returns
    -------
    tuple[float, tuple[float, float, float, float]]
        The Attribution Quality Score, then the Prediction Preserved, Image Preserved, Relative Foreground Attribution, and External Peak Attribution scores as a separate tuple

    See Also
    --------
    attribution_quality.metrics.compute_masked_metrics_from_source
        Computes the Prediction Preserved
    attribution_quality.metrics.compare_entropy
        Computes the Relative Entropy
    attribution_quality.metrics.compute_cam_localization
        Computes the Relative Foreground Attribution and External Peak Attribution
    """
    cam_mask /= cam_mask.max()
    pred_pres, _, _ = compute_masked_metrics_from_source(network, input_image, cam_mask)
    rel_entropy = compare_entropy(input_image, mask=cam_mask)
    localization_kwargs = {} if localization_kwargs is None else localization_kwargs
    rel_fg, ex_peak = compute_cam_localization(cam_mask, full_label_image, **localization_kwargs)
    aq = (pred_pres / rel_entropy) + (rel_fg * (1 + ex_peak))
    return aq, (pred_pres, rel_entropy, rel_fg, ex_peak)
