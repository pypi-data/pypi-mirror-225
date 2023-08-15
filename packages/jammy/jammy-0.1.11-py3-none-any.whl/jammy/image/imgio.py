#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : imgio.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 01/19/2018
#
# This file is part of Jacinle.
# Distributed under terms of the MIT license.


import os as os
import os.path as osp
import numpy as np

from . import backend
from .imgproc import dimshuffle


__all__ = [
    "imread",
    "imwrite",
    "imshow",
    "plt2pil",
    "plt2nd",
    "nd2pil",
    "pil2nd",
    "savefig",
]


def imread(path, *, shuffle=False):
    if not osp.exists(path):
        return None
    i = backend.imread(path)
    if i is None:
        return None
    if shuffle:
        return dimshuffle(i, "channel_first")
    return i


def imwrite(path, img, *, shuffle=False):
    if shuffle:
        img = dimshuffle(img, "channel_last")
    backend.imwrite(path, img)


def imshow(title, img, *, shuffle=False):
    if shuffle:
        img = dimshuffle(img, "channel_last")
    backend.imshow(title, img)


def plt2pil(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    from PIL import Image

    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

def plt2nd(fig):
    return np.array(plt2pil(fig))

def savefig(fig, fig_name):
    fig_path = fig_name.split("/")
    if len(fig_path) > 1:
        save_path = "/".join(fig_path[:-1])
        if not osp.isdir(save_path):
            os.makedirs(save_path, exist_ok=True)
    fig.savefig(fig_name)


nd2pil=backend.pil_nd2img
pil2nd=backend.pil_img2nd