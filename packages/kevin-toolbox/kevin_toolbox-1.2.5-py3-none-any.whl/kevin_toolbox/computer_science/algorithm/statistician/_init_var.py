import torch
import numpy as np


def _init_var(like=None, data_format=None):
    if like is not None:
        if torch.is_tensor(like):
            var = torch.zeros_like(like)
        elif isinstance(like, (np.ndarray,)):
            var = np.zeros_like(like)
        elif isinstance(like, (int, float, np.number,)):
            var = 0.0
        else:
            raise ValueError("paras 'like' should be np.ndarray, torch.tensor or int/float")
    elif data_format is not None:
        assert isinstance(data_format, (dict,)) and "type_" in data_format and "shape" in data_format
        k_s = copy.deepcopy(data_format)
        k_s.pop("type_")
        k_s.pop("shape")
        if data_format["type_"] == "torch":
            var = torch.zeros(size=data_format["shape"], **k_s)
        else:
            var = np.zeros(shape=data_format["shape"], **k_s)
    else:
        var = None

    return var
