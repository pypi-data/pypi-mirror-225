"""
Utility functions for experiments using nnUNet models
"""
import io
import glob
import os
import sys
from typing import Union

import nnunet
import numpy as np
import torch
from batchgenerators.augmentations.utils import pad_nd_image
from nnunet.paths import network_training_output_dir
from nnunet.training.model_restore import load_model_and_checkpoint_files, recursive_find_python_class
from nnunet.training.network_training import nnUNetTrainer
from nnunet.utilities.task_name_id_conversion import convert_id_to_task_name

from attribution_quality.splitnet.split_nnunet import decompose_nnunet


def prep_model_from_dir(model_dir: str, checkpoint_name: str = 'model_final_checkpoint', folds: Union[int, str, list[Union[int, str]]] = None, mixed_precision: bool = True):
    """Prepare the trainer-class and parameters for a given model

    Parameters
    ----------
    model_dir : str
        nnUNet-style directory for the target model
    checkpoint_name : str, optional
        Name of the checkpoint to load, by default 'model_final_checkpoint'
    folds : Union[int, str, list[Union[int, str]]], optional
        Which fold(s) of the target model to load, by default None
    mixed_precision : bool, optional
        Whether to allow amp for model weights, by default True

    Note
    ----
    Use "all" for folds for a model that was trained on all training data (no validation) or None to autodetect trained folds

    See Also
    --------
    nnunet.training.model_restore.restore_model
        Loads a model from a pkl checkpoint file (the lower-level version of this function)
    """
    if isinstance(folds, str) and folds != 'all':
        folds = int(folds)
    if isinstance(folds, list):
        if folds[0] == 'all' and len(folds) == 1:
            pass
        else:
            folds = [int(i) for i in folds]
    torch.cuda.empty_cache()
    trainer, params = load_model_and_checkpoint_files(model_dir, folds, mixed_precision=mixed_precision, checkpoint_name=checkpoint_name)
    return trainer, params


def get_trainer(task: Union[str, int], fold: Union[int, str, list[Union[int, str]]] = 0, use_best: bool = False, load: bool = True, eval: bool = True):
    """Load the nnUNet trainer for a given task/fold

    Parameters
    ----------
    task : str | int
        The name or ID of the task
    fold : int, Union[int, str, list[Union[int, str]]]
        Which fold(s) the desired model was trained on, by default 0
    use_best : bool, optional
        If true, loads the model with the lowest validation loss. Otherwise, loads the final model checkpoint. By default False
    load : bool, optional
        Whether to load the model weights into RAM, by default True
    eval : bool, optional
        Whether to load the model in evaluation mode (as opposed to training mode), by default True

    Returns
    -------
    nnUNet model trainer

    Note
    ----
    The deep learning model/network can be found at `trainer.network`
    """
    if isinstance(task, int):
        task = convert_id_to_task_name(task)
    model_folder = os.path.join(network_training_output_dir, '3d_fullres', task, 'nnUNetTrainerV2__nnUNetPlansv2.1')
    assert os.path.exists(model_folder), 'Missing model folder for task: {}'.format(model_folder)
    checkpoint_name = 'model_best' if use_best else 'model_final_checkpoint'
    trainer, params = prep_model_from_dir(model_folder, checkpoint_name, folds=fold)
    if load:
        trainer.load_checkpoint_ram(params[0], False)
    if eval:
        trainer.network.eval()
        trainer.network.do_ds = False
    return trainer


def get_trainer_preprocessor(trainer: nnUNetTrainer):
    pname = trainer.plans.get('preprocessor_name')
    if pname is None:
        pname = 'GenericPreprocessor' if trainer.threeD else 'PreprocessorFor2D'
    pclass = recursive_find_python_class([os.path.join(nnunet.__path__[0], 'preprocessing')], pname, current_module='nnunet.preprocessing')
    assert pclass is not None, f'Could not find preprocessor {pname} in nnunet.preprocessing'
    preprocessor = pclass(trainer.normalization_schemes, trainer.use_mask_for_norm, trainer.transpose_forward, trainer.intensity_properties)
    return preprocessor


def basicname(path):
    head, tail = os.path.split(path)
    splitpath = tail.split('.')
    to_add = ''
    while splitpath[0] == '':
        splitpath = splitpath[1:]
        to_add += '.'
    splitpath[0] = to_add + splitpath[0]
    return splitpath[0]


def get_trainer_task(trainer):
    return int(basicname(trainer.dataset_directory).rsplit('_', 1)[0].replace('Task', ''))


def get_sample_path(task: int, sample_name: Union[str, os.PathLike]) -> tuple[list, list]:
    raw_dir = os.path.join(nnunet.paths.nnUNet_raw_data, os.path.basename(convert_id_to_task_name(task)))
    test_img_check = glob.glob(os.path.join(raw_dir, 'imagesTs', f'{sample_name}_*.nii.gz'))
    if len(test_img_check) > 0:
        if not os.path.exists(os.path.join(raw_dir, 'labelsTs')):
            return test_img_check, []
        test_label_check = glob.glob(os.path.join(raw_dir, 'labelsTs', f'{sample_name}.nii.gz'))
        return test_img_check, test_label_check

    train_img_check = glob.glob(os.path.join(raw_dir, 'imagesTr', f'{sample_name}_*.nii.gz'))
    if len(train_img_check) > 0:
        train_label_check = glob.glob(os.path.join(raw_dir, 'labelsTr', f'{sample_name}.nii.gz'))
        return train_img_check, train_label_check
    raise ValueError(f'No image/labels found for sample `{sample_name}`')


def prep_data(trainer, sample_id, fold=0, verbose=False):
    preprocessor = get_trainer_preprocessor(trainer)
    if isinstance(sample_id, (list, tuple)):
        image_paths = sample_id
        label_paths = None
    else:
        task = get_trainer_task(trainer)
        image_paths, label_paths = get_sample_path(task, sample_id)
    if not verbose:
        with OutputMuffle():
            # Lots of stdout from nnunet during preprocessing...
            data, seg, prop = preprocessor.preprocess_test_case(image_paths, trainer.plans['plans_per_stage'][trainer.stage]['current_spacing'])
    else:
        data, seg, prop = preprocessor.preprocess_test_case(image_paths, trainer.plans['plans_per_stage'][trainer.stage]['current_spacing'])

    data, slicer = pad_nd_image(data, trainer.patch_size, 'constant', {'constant_values': 0}, return_slicer=True, shape_must_be_divisible_by=None)
    data = np.clip(data, -2, 2)  # prevents extreme pixels from throwing off gradients
    return data, slicer


class OutputMuffle:
    """Context manager that redirects output streams into a string buffer"""
    def __init__(self, stream='stdout'):
        self.stream = [stream] if isinstance(stream, str) else stream
        self._old_targets = {key: [] for key in self.stream}
        self.new_targets = {key: io.StringIO() for key in self.stream}

    def __enter__(self):
        for key in self.stream:
            self._old_targets[key].append(getattr(sys, key))
            setattr(sys, key, self.new_targets[key])
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        for key in self.stream:
            setattr(sys, key, self._old_targets[key].pop())

    def __getitem__(self, key):
        return self.new_targets[key].getvalue()


def clean_layer_name(layer_name):
    """Make nnUNet layer names slightly easier to read and usable in filenames"""
    layer_name = layer_name.replace('.', '_')
    layer_name = layer_name.replace('conv_blocks_context', 'conv_blocks')
    layer_name = layer_name.replace('_blocks_0_conv', '_block0')
    layer_name = layer_name.replace('_blocks_1_conv', '_block1')
    return layer_name


def prepare_layer_names(trainer: nnUNetTrainer, return_targets: bool = False, skip_transpose: bool = False):
    encoder_layers, bottleneck_layers, decoder_layers, _ = decompose_nnunet(trainer.network, names_only=True)
    if skip_transpose:
        decoder_layers = [layer for layer in decoder_layers if not layer.startswith('tu.')]
    target_layers = encoder_layers + decoder_layers
    layer_names = []
    for layer_idx, layer_name in enumerate(target_layers):
        if layer_idx < len(encoder_layers):
            idx = layer_idx
            target_layer = encoder_layers[idx]
            prefix = f'enc{idx}'
        else:
            idx = layer_idx - len(encoder_layers)
            target_layer = decoder_layers[idx]
            prefix = f'dec{idx}'
        layer_name = prefix + '_' + clean_layer_name(target_layer)
        layer_names.append(layer_name)
    if return_targets:
        return layer_names, target_layers
    return layer_names
