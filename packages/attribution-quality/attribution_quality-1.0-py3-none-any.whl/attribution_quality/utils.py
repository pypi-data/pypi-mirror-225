from typing import Any, Iterable, Optional, Union

import numpy as np
import numpy.typing as npt
import skimage.transform
import torch

ShapeType = Union[int, tuple[int, ...]]
FloatArrayType = Union[float, np.floating, npt.NDArray[np.floating]]


# Attribute/Meta Functions
class classproperty(property):
    # https://stackoverflow.com/a/13624858/2348288
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


def getattr_recursive(item, attr_string):
    """Recursively find attributes of the given `item` based on the `attr_string`

    Parameters
    ----------
    item : Any
        The item to find attributes of
    attr_string : str
        The string pattern of the desired attributes

    Notes
    -----
    Each nested attribute in the `attr_string` must be separated with a '.'
    Attributes can be integers to index into `item` (for example: 'item.0' is equivalent to 'item[0]')

    Examples
    --------
    `item.first.2.last` is equivalent to `item.first[2].last`

    `item.0.1.second.third.4` is equivalent to `item[0][1].second.third[4]`
    """
    nested_type = type(item).__name__
    cur_item = item
    for key in attr_string.split('.'):
        if key.isdecimal() and hasattr(cur_item, '__getitem__'):
            try:
                cur_item = cur_item[int(key)]
            except TypeError:
                raise TypeError("Cannot index {} with {}".format(nested_type, key))
        else:
            try:
                cur_item = getattr(cur_item, key)
                nested_type += '.' + type(cur_item).__name__
            except AttributeError:
                raise AttributeError("'{}' object has no attribute '{}'".format(nested_type, key))
    return cur_item


class DummyContext():
    """Dummy context to replace torch.autocast when amp is not being used"""
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass


# Converter Functions
def to_torch(data):
    if isinstance(data, (list, tuple)):
        out_type = type(data)
        data = out_type([to_torch(item) if not isinstance(item, torch.Tensor) else item for item in data])
    elif not isinstance(data, torch.Tensor):
        data = torch.from_numpy(data).float()
    return data


def to_cuda(data):
    if isinstance(data, (list, tuple)):
        data = type(data)([item.cuda() for item in data])
    else:
        data = data.cuda()
    return data


def to_cuda_torch(data):
    data = to_torch(data)
    if torch.cuda.is_available():
        data = to_cuda(data)
    return data


def to_numpy(data):
    if isinstance(data, (list, tuple)):
        out_type = type(data)
        data = out_type([to_numpy(item) if not isinstance(item, np.ndarray) else item for item in data])
    elif isinstance(data, np.ndarray):
        pass
    elif isinstance(data, torch.Tensor):
        data = data.cpu().detach().numpy()
    else:
        data = np.asarray(data)
    return data


# Data Operations
def resize_cam_image(cam: npt.NDArray[np.floating], target_size: Optional[ShapeType] = None, rescale: bool = True) -> npt.NDArray[np.floating]:
    """Resize the input CAM to the target size

    Parameters
    ----------
    cam : npt.NDArray[np.floating]
        Class Activation Map to resize, can either be a single CAM or multiple CAMs stacked along the first axis
    target_size : Optional[ShapeType], optional
        Output size, by default None
    rescale : bool, optional
        Whether to scale the output map so the maximum value is 1, by default True

    Returns
    -------
    npt.NDArray[np.floating]
        Resized CAM
    """
    rescale_kwargs = {'mode': 'edge', 'anti_aliasing': False, 'preserve_range': True}
    result = []
    if isinstance(cam, np.ndarray) and (cam.ndim == len(target_size)):
        cam = [cam]
    for img in cam:
        if rescale:
            img = img / (np.max(img) + 1e-7)
        if target_size is not None:
            img = skimage.transform.resize(img, target_size, **rescale_kwargs)
        result.append(img)
    result = np.float32(result)
    return result


def softmax(x: np.ndarray, axis: Optional[Union[int, tuple[int, ...]]] = None) -> np.ndarray:
    """Softmax activation function for numpy arrays

    Parameters
    ----------
    x : np.ndarray
        Input array
    axis : Union[int, tuple[int, ...]], optional
        Axes to operate across, by default None

    Returns
    -------
    np.ndarray
        Result array
    """
    s = np.max(x, axis=axis, keepdims=True)
    e_x = np.exp(x - s)
    div = np.sum(e_x, axis=axis, keepdims=True)
    return np.divide(e_x, div, where=div != 0, out=np.zeros_like(x))


def apply_mask(data: np.ndarray, mask: np.ndarray, min_mask: bool = False) -> np.ndarray:
    """Apply a mask to the input data

    Parameters
    ----------
    data : np.ndarray
        The array to mask
    mask : np.ndarray
        The mask to apply to the array
    min_mask : bool, optional
        If True, use the minimum value in `data` as the masking value. If False, 0 is used. by default False

    Returns
    -------
    np.ndarray
        The masked array
    """
    if data.shape != mask.shape:  # Convenience in case data shape is [1, 1, h, w, d] and mask is [h, w, d]
        to_expand = np.argwhere(np.asarray(data.shape) == 1).flatten()
        data = np.squeeze(data)
    else:
        to_expand = None
    if min_mask:
        data = (data * mask) + ((1 - mask) * data.min())
    else:
        data = data * mask
    if to_expand is not None:
        data = np.expand_dims(data, to_expand.tolist())
    return data


def quick_pred(net: torch.nn.Module, data: np.ndarray, mask: Optional[Union[np.ndarray, list[np.ndarray]]] = None, target_idx: int = 1, min_mask: bool = False, as_tensor: bool = False) -> Union[torch.Tensor, np.ndarray]:
    """Short-cut method for predicting normal and masked samples with a network

    Parameters
    ----------
    net : torch.nn.Module
        Network or nnUNet trainer class that has a loaded network
    data : np.ndarray
        Input sample for the network
    mask : Optional[Union[np.ndarray, list[np.ndarray]]], optional
        Optional mask(s) to apply to the input sample, by default None
    target_idx : int, optional
        The target class to return predictions from. If None, returns entire prediction. by default 1 (foreground class)
    min_mask : bool, optional
        If True, masks with the minimum value of the input data, otherwise masks with 0, by default False
    as_tensor : bool, optional
        If True, returns result as torch.Tensor, otherwise as np.ndarray, by default False

    NOTE
    ----
    If multiple masks are used, then the first dimension of the result tensor will be the number of masks. Otherwise, there will be no sample dimension.
    If the target_idx is not None, then only the target_idx class will be returned and there will be no class dimension.
    If both multiple masks are used and the target_idx is None, the result will have the shape (num_masks, num_classes, *data.shape)
    In nnUNet models with a binary prediction, a target_idx of 0 will return the background class and a target_idx of 1 will return the foreground class.
    """
    if 'nnUNetTrainer' in str(type(net)) and hasattr(net, 'network'):
        net = net.network
    with torch.no_grad():
        data = np.expand_dims(data, [i for i in range(5 - data.ndim)])
        if mask is not None:
            if isinstance(mask, (list, tuple)):
                masks = [np.expand_dims(item, [i for i in range(5 - item.ndim)]) for item in mask]
                data = np.concatenate([apply_mask(data, item, min_mask=min_mask) for item in masks], axis=0)
            else:
                mask = np.expand_dims(mask, [i for i in range(5 - mask.ndim)])
                data = apply_mask(data, mask, min_mask=min_mask)
        data = to_cuda_torch(data)
        pred = torch.softmax(net(data), axis=1)
        if target_idx is not None:
            pred = pred[:, target_idx]
        pred = torch.squeeze(pred, dim=0)

        if as_tensor:
            pred = pred.cpu().detach()
        else:
            pred = to_numpy(pred)
    return pred


def is_iter(x: Any, non_iter: Iterable[type] = (str, bytes, bytearray, np.ndarray, torch.Tensor)) -> bool:
    """Check if x is iterable

    Parameters
    ----------
    x : Any
        The variable to check
    non_iter : Iterable[type], optional
        Types to not count as iterable types, by default (str, bytes, bytearray)

    Note
    ----
    The intended use of this method is to check for lists, tuples, sets, and other basic iterables. It is not intended to check for arrays and tensors.
    """
    if isinstance(x, tuple(non_iter)):
        return False

    try:
        iter(x)
    except TypeError:
        return False
    else:
        return True
