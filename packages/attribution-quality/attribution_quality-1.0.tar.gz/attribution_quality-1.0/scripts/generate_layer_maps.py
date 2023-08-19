"""This script generates CAMs for each layer of a trained nnU-Net model and saves them to disk. All samples present in the imagesTs directory for the given task are processed. The CAMs are saved in the output folder for the given task/model/fold of the nnU-Net trainer being explained."""
import os
# NOTE - Set these environment variables to the appropriate paths for your system
# os.environ.setdefault('RESULTS_FOLDER', '/PATH/TO/YOUR/nnUNet_models')
# os.environ.setdefault('nnUNet_preprocessed', '/PATH/TO/YOUR/nnUNet_preprocessed')
# os.environ.setdefault('nnUNet_raw_data_base', '/PATH/TO/YOUR/nnUNet_raw')

import functools
import glob

import nnunet
import numpy as np
import torch
import tqdm.auto as tqdm
from nnunet.utilities.task_name_id_conversion import convert_id_to_task_name

from attribution_quality.optional_imports import SimpleITK as sitk
from attribution_quality import KWC, GradCAM, GradCAMPlusPlus, ScoreCAM
from attribution_quality.nnunet_utils import (basicname, prepare_layer_names,
                                              get_trainer, prep_data)


def generate_maps(task_id, cam_types, fold=0, skip_existing=True, save_compressed=False):
    trainer = get_trainer(task_id, fold=fold)
    task_name = convert_id_to_task_name(task_id)
    data_dir = os.path.join(nnunet.paths.nnUNet_raw_data, task_name, 'imagesTs')
    test_sample_ids = glob.glob(os.path.join(data_dir, '*.nii.gz'))
    test_sample_ids = [basicname(path).rsplit('_', 1)[0] for path in test_sample_ids]
    test_sample_ids = sorted(test_sample_ids, key=lambda x: int(x.split('_')[-1]))

    layer_names, target_layers = prepare_layer_names(trainer, return_targets=True)

    activation_func = functools.partial(torch.nn.functional.softmax, dim=1)
    cam_kwargs = {
        'use_cuda': True,
        'n_spatial_dim': 3,
        'verbose': 2,
        'allow_amp': True,
        'resize_to_input': False,  # The per-layer CAMs will be resized when combined later
        'activation_func': activation_func}

    for sample_name in tqdm.tqdm(test_sample_ids):
        data, inv_slicer = prep_data(trainer, sample_name, fold=fold)
        if data.ndim != 5:
            data = np.expand_dims(data, [i for i in range(5 - data.ndim)])
        if np.any(data.shape[-3:] > trainer.patch_size):
            # Sanity check - doesn't occur with the nodule dataset, but does several times with Hippocampus
            print('Skipping sample {} - too large for single patch'.format(sample_name))
            continue

        for cam_type in cam_types:
            save_dir = os.path.join(trainer.output_folder, f'explanation_{cam_type.name}', sample_name)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir, exist_ok=True)
            if cam_type.uses_grad:
                # GradCAM and GradCAM++
                # Gradient-based methods are less stable but can compute the CAM for all layers in one pass if enough memory is available
                exists_check = True
                for layer_name in layer_names:
                    dst_path = os.path.join(save_dir, f'{layer_name}_{cam_type.abbr}.nii')
                    if save_compressed:
                        dst_path += '.gz'
                    exists_check = exists_check and os.path.exists(dst_path)
                if exists_check and skip_existing:
                    continue

                with cam_type(trainer.network, target_layers, batch_size=1, **cam_kwargs) as cam_model:
                    layer_cams = cam_model.forward(data)
                for layer_idx in range(len(target_layers)):
                    layer_cam = layer_cams[layer_idx]
                    layer_name = layer_names[layer_idx]
                    dst_path = os.path.join(save_dir, f'{layer_name}_{cam_model.abbr}.nii')
                    if save_compressed:
                        dst_path += '.gz'
                    image = sitk.GetImageFromArray(np.squeeze(layer_cam))
                    dst_spacing = (np.asarray(np.squeeze(data).shape) / np.asarray(layer_cam.shape))[2:][::-1]
                    image.SetSpacing(dst_spacing.tolist())
                    sitk.WriteImage(image, dst_path)
            else:
                # Kernel-Weighted Contribution and ScoreCAM
                # Non-gradient methods tend to be more stable but can only analyze one layer at a time
                for layer_idx in range(len(target_layers)):
                    layer_name = layer_names[layer_idx]
                    dst_path = os.path.join(save_dir, f'{layer_name}_{cam_type.abbr}.nii')
                    if save_compressed:
                        dst_path += '.gz'
                    if os.path.exists(dst_path) and skip_existing:
                        continue
                    with cam_type(trainer.network, target_layers[layer_idx], batch_size=4, **cam_kwargs) as cam_model:
                        layer_cam = cam_model.forward(data)[0]
                    image = sitk.GetImageFromArray(np.squeeze(layer_cam))
                    dst_spacing = (np.asarray(data.shape) / np.asarray(layer_cam.shape))[2:][::-1]
                    image.SetSpacing(dst_spacing.tolist())
                    sitk.WriteImage(image, dst_path)


if __name__ == '__main__':
    cam_types = [KWC, GradCAM, GradCAMPlusPlus, ScoreCAM]  # Add/remove CAM types here
    # generate_maps(507, cam_types, fold=0)  # For the Hippocampus task
    generate_maps(902, cam_types, fold=0)
