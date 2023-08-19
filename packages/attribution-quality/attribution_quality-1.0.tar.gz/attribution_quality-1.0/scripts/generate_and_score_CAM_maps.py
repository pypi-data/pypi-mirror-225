"""This script iterates over the layer-wise CAMs generated in `generate_layer_maps.py`, merges them into a single CAM for each sample, and evaluates their quality. The CAMs and results are saved in the output folder for the given task/model/fold of the nnU-Net trainer being explained."""
import os

# NOTE - Set these environment variables to the appropriate paths for your system
# os.environ.setdefault('RESULTS_FOLDER', '/PATH/TO/YOUR/nnUNet_models')
# os.environ.setdefault('nnUNet_preprocessed', '/PATH/TO/YOUR/nnUNet_preprocessed')
# os.environ.setdefault('nnUNet_raw_data_base', '/PATH/TO/YOUR/nnUNet_raw')

import glob

import nnunet
import numpy as np
import tqdm.auto as tqdm

from attribution_quality import KWC, GradCAM, GradCAMPlusPlus, ScoreCAM
from attribution_quality.metrics import (compare_entropy,
                                         compute_cam_localization,
                                         compute_masked_metrics)
from attribution_quality.nnunet_utils import (basicname,
                                              convert_id_to_task_name,
                                              get_sample_path, get_trainer,
                                              prep_data, prepare_layer_names)
from attribution_quality.optional_imports import SimpleITK as sitk
from attribution_quality.utils import apply_mask, quick_pred, resize_cam_image


def copy_information(image, ref_image):
    if isinstance(ref_image, str):
        ref_path = ref_image
        ref_image = sitk.ImageFileReader()
        ref_image.SetFileName(ref_path)
        ref_image.ReadImageInformation()
    assert image.GetSize() == ref_image.GetSize(), 'Image size mismatch'
    image.SetOrigin(ref_image.GetOrigin())
    image.SetDirection(ref_image.GetDirection())
    image.SetSpacing(ref_image.GetSpacing())


def combine_maps(task_id, cam_types, fold=0, layer_names=None, results_dst=None, skip_existing_cam=True, save_compressed=False):
    trainer = get_trainer(task_id, fold=fold)
    if layer_names is None:
        layer_names = prepare_layer_names(trainer)
    task_name = convert_id_to_task_name(task_id)
    data_dir = os.path.join(nnunet.paths.nnUNet_raw_data, task_name, 'imagesTs')
    if results_dst is None:
        results_dst = os.path.join(trainer.output_folder, 'cam_results.csv')

    test_sample_ids = glob.glob(os.path.join(data_dir, '*.nii.gz'))
    test_sample_ids = [basicname(path).rsplit('_', 1)[0] for path in test_sample_ids]
    test_sample_ids = sorted(test_sample_ids, key=lambda x: int(x.split('_')[-1]))

    with open(results_dst, 'w') as out_file:
        out_file.write('Sample Name,CAM Type,Attribution Quality,Prediction Preserved,Relative Entropy,Relative Foreground Attribution,External Peak Attribution\n')
        for sample_name in tqdm.tqdm(test_sample_ids):
            data, inv_slicer = prep_data(trainer, sample_name, fold=fold)
            image_path, label_path = get_sample_path(task_id, sample_name)
            label_path = label_path[0].replace('labelsTs', 'labelsTs_full')
            full_label = sitk.ReadImage(label_path)

            data = np.clip(data, -2, 2)
            if data.ndim != 5:
                data = np.expand_dims(data, [i for i in range(5 - data.ndim)])
            if np.any(data.shape[-3:] > trainer.patch_size):
                print('Skipping sample {} - too large for single patch'.format(sample_name))
                continue

            baseline_pred = quick_pred(trainer, data)
            baseline_entropy = compare_entropy(np.squeeze(data))

            for cam_type in tqdm.tqdm(cam_types):
                save_dir = os.path.join(trainer.output_folder, f'explanation_{cam_type.name}', sample_name)
                cam_dst_path = os.path.join(save_dir, f'cam_{cam_type.abbr}.nii')
                if save_compressed:
                    cam_dst_path += '.gz'
                if os.path.exists(cam_dst_path) and skip_existing_cam:
                    cam_image = sitk.ReadImage(cam_dst_path)
                else:
                    cam_image = None
                    for layer_name in layer_names:
                        cam_layer_path = glob.glob(os.path.join(save_dir, f'{layer_name}_{cam_type.abbr}.nii*'))[0]
                        cam_layer_image = sitk.ReadImage(cam_layer_path)
                        cam_layer_image = sitk.GetArrayFromImage(cam_layer_image)
                        cam_layer_image = resize_cam_image(cam_layer_image, target_size=data.shape[2:], rescale=cam_type.abbr != KWC.abbr)
                        cam_image = cam_layer_image if cam_image is None else cam_image + cam_layer_image
                    max_mag = max(abs(cam_image.min()), abs(cam_image.max()))
                    if max_mag > 1e-8:
                        cam_image /= cam_image.max()

                    cam_image = sitk.GetImageFromArray(cam_image)
                    copy_information(cam_image, image_path[0])
                    sitk.WriteImage(cam_image, cam_dst_path)
                cam_view = sitk.GetArrayViewFromImage(cam_image)  # Just so we only operate on 1 copy of the data

                masked_image = apply_mask(data, cam_view)
                masked_pred = quick_pred(trainer, masked_image)
                pred_pres, _, _ = compute_masked_metrics(baseline_pred, masked_pred, cam_view)
                masked_entropy = compare_entropy(masked_image)
                rel_entropy = masked_entropy / baseline_entropy
                rel_fg, ex_peak = compute_cam_localization(cam_view, full_label)
                aq = (pred_pres / rel_entropy) + (rel_fg * (1 + ex_peak))

                out_file.write(f'{sample_name},{cam_type.name},{aq:.4f},{pred_pres:.4f},{rel_entropy:.4f},{rel_fg:.4f}\n')
                out_file.flush()


if __name__ == '__main__':
    cam_types = [KWC, GradCAM, GradCAMPlusPlus, ScoreCAM]  # Add/remove CAM types here
    # generate_maps(507, cam_types, fold=0)  # For the Hippocampus task
    combine_maps(902, cam_types, fold=0, layer_names=None, results_dst=None, skip_existing_cam=True, save_compressed=True)
