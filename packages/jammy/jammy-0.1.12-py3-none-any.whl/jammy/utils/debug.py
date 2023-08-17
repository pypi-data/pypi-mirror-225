import collections
import contextlib
import functools
import os
import sys
import threading
from typing import Any, Dict, List, Tuple, Union

import numpy as np
import torch
from loguru._logger import Core as _Core
from loguru._logger import Logger as _Logger

import jammy.io as jio
from jammy.logging.logger import LOG_FORMAT
from jammy.utils.env import jam_getenv
from jammy.utils.registry import CallbackRegistry

# skip precommit check for debug statement
if jam_getenv("pdb", "ipdb").lower() == "ipdb":
    import ipdb as pdb  # noqa
else:
    import pudb as pdb  # noqa # pylint: disable=import-error

__all__ = [
    "hook_exception_ipdb",
    "unhook_exception_ipdb",
    "exception_hook",
    "decorate_exception_hook",
    "replayer",
]

# pylint: disable=invalid-name, redefined-builtin


def _custom_exception_hook(type, value, tb):
    if hasattr(sys, "ps1") or not sys.stderr.isatty():
        # we are in interactive mode or we don't have a tty-like
        # device, so we call the default hook
        sys.__excepthook__(type, value, tb)
    else:
        import traceback

        # we are NOT in interactive mode, print the exception...
        traceback.print_exception(type, value, tb)
        # ...then start the debugger in post-mortem mode.
        pdb.post_mortem(tb)


def hook_exception_ipdb():
    if not hasattr(_custom_exception_hook, "origin_hook"):
        _custom_exception_hook.origin_hook = sys.excepthook
        sys.excepthook = _custom_exception_hook


def unhook_exception_ipdb():
    assert hasattr(_custom_exception_hook, "origin_hook")
    sys.excepthook = _custom_exception_hook.origin_hook


@contextlib.contextmanager
def exception_hook(enable=True):
    if enable:
        hook_exception_ipdb()
        yield
        unhook_exception_ipdb()
    else:
        yield


def decorate_exception_hook(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        with exception_hook():
            return func(*args, **kwargs)

    return wrapped


def _TimeoutEnterIpdbThread(locals_, cv, timeout):
    del locals_
    with cv:
        if not cv.wait(timeout):

            pdb.set_trace()


@contextlib.contextmanager
def timeout_ipdb(locals_, timeout=3):
    cv = threading.Condition()
    thread = threading.Thread(
        target=_TimeoutEnterIpdbThread, args=(locals_, cv, timeout)
    )
    thread.start()
    yield
    with cv:
        cv.notify_all()


def _default_replayer_fallback(obj, *args, **kwargs):
    del args, kwargs
    if len(obj) == 0:
        return obj
    item_type = type(obj)
    raise ValueError('Unknown itme type: "{}".'.format(item_type))


class _RePlayerCallbackRegistry(CallbackRegistry):
    def dispatch(self, name, *args, **kwargs):
        return super().dispatch_direct(name, *args, **kwargs)


def replay_proc_dict(obj: Dict[str, Any]):
    rtn_dict = {}
    for k, v in obj.items():
        rtn_dict[k] = replayer_processing(v)
    return rtn_dict


def replay_proc_module(obj: torch.nn.Module):
    grads_dict = {}
    for k, v in obj.named_parameters():
        # record weights value and grad if exists
        if v.grad is not None:
            grads_dict[k] = v.grad.clone().detach()
    return {
        "weights": obj.state_dict(),
        "grads": grads_dict,
    }


def replay_proc_basic(obj: List[Union[int, float, str, complex]]):
    assert type(obj) in [int, float, str, complex, np.ndarray, torch.Tensor]
    return obj


def replay_proc_iter(obj: Union[List, Tuple]):
    rtn = []
    for cur_obj in obj:
        rtn.append(replayer_processing(cur_obj))
    return rtn


_replayer_registry = _RePlayerCallbackRegistry()
_replayer_registry.set_fallback_callback(_default_replayer_fallback)
_replayer_registry.register(int, replay_proc_basic)
_replayer_registry.register(str, replay_proc_basic)
_replayer_registry.register(float, replay_proc_basic)
_replayer_registry.register(complex, replay_proc_basic)
_replayer_registry.register(np.ndarray, replay_proc_basic)
_replayer_registry.register(torch.Tensor, replay_proc_basic)
_replayer_registry.register(dict, replay_proc_dict)
_replayer_registry.register(collections.OrderedDict, replay_proc_dict)
_replayer_registry.register(collections.defaultdict, replay_proc_dict)
_replayer_registry.register(tuple, replay_proc_iter)
_replayer_registry.register(list, replay_proc_iter)


def replayer_processing(obj: Any):
    return _replayer_registry.dispatch(type(obj), obj)


class RePlayer:
    def __init__(self, savedir, level="INFO"):
        self.savedir = savedir
        self.counter = 0
        self.data = {}
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        self.logger = _Logger(
            core=_Core(),
            exception=None,
            depth=0,
            record=False,
            lazy=False,
            colors=False,
            raw=False,
            capture=True,
            patchers=[],
            extra={},
        )
        self.logger.add(
            os.path.join(savedir, "_jam_replayer.log"),
            level=level,
            mode="w",
            format=LOG_FORMAT,
        )
        self.logger.add(
            sys.stdout,
            level="INFO",
            format=LOG_FORMAT,
        )

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self.logger.critical(*args, **kwargs)

    def log(self, **kwargs):
        self.data.update(replayer_processing(kwargs))

    def reset(self):
        self.data = {}
        self.counter = 0

    def dump(self):
        self.counter += 1
        jio.dump(
            f"{self.savedir}/jam_replay_{self.counter:04d}.pkl",
            self.data,
        )
        self.data = {}

    def load(self, idx, savedir=None):
        if savedir is None:
            savedir = self.savedir
        self.data = jio.load(
            f"{savedir}/jam_replay_{idx:04d}.pkl",
        )
        self.counter = idx


replayer = RePlayer("/tmp/jam_replayer")
