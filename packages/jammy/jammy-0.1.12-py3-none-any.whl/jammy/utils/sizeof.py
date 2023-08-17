import sys

import numpy as np
import torch as th

from jammy.io.common import fsize_format
from jammy.utils.registry import CallbackRegistry

__all__ = ["sizeof"]

sys_sizeof = sys.getsizeof


def torch_sizeof(obj):
    return obj.element_size() * obj.nelement()


def np_sizeof(obj):
    return obj.nbytes


class _Registry(CallbackRegistry):
    def dispatch(self, name, *args, readable_string=True, **kwargs):
        size_in_byte = super().dispatch_direct(name, *args, **kwargs)
        if readable_string:
            return fsize_format(size_in_byte)
        return size_in_byte


_size_of_registry = _Registry()
_size_of_registry.set_fallback_callback(sys_sizeof)
_size_of_registry.register(int, sys_sizeof)
_size_of_registry.register(float, sys_sizeof)
_size_of_registry.register(complex, sys_sizeof)
_size_of_registry.register(np.ndarray, np_sizeof)
_size_of_registry.register(th.Tensor, torch_sizeof)


def sizeof(obj, readable_string=True):
    return _size_of_registry.dispatch(type(obj), obj, readable_string=readable_string)


if __name__ == "__main__":
    from jammy.utils.printing import stprint

    stprint(sizeof(1))
    stprint(sizeof(1.0))
    stprint(sizeof(1 + 1j))
    stprint(sizeof(np.zeros((2, 3))))
    stprint(sizeof(th.zeros((30000, 3, 256, 256))))
