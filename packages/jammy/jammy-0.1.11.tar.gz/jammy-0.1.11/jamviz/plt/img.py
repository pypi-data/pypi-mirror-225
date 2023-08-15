import numpy as np
import matplotlib.pyplot as plt

__all__ = [
    "ndimgs_in_row",
]

def ndimgs_in_row(list_x, n, dpi=128, img_size=400):
    """
    args:
    list_x: list of elements that imshow can display
    n: number of the element in a row
    """
    length = len(list_x)
    idxes = np.linspace(0, length - 1, n, dtype=int)
    with plt.style.context("img"):
        fig, axs = plt.subplots(
            1, n, figsize=(n * img_size / dpi, img_size / dpi), dpi=dpi
        )
        for j, idx in enumerate(idxes):
            axs[j].imshow(list_x[idx])
            axs[j].set_title(idx)
    return fig