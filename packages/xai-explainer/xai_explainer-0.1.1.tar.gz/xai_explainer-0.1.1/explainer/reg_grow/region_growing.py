from tkinter.filedialog import askopenfilename

import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np

FOREGROUND_QUANTILE = (
    0.8  # only pixels above or equal to this quantile can be used as peaks
)
BACKGROUND_QUANTILE = (
    0.2  # all pixels below or equal to this quantile will become background
)
MERGE_DISTANCE = 5  # number of iterations when merging peaks


def segmentation(heatmap: np.ndarray):
    if heatmap.dtype == np.float32:
        heatmap *= 255
        heatmap = heatmap.astype(np.uint8)

    # kernel used for dilate and erode operations
    kernel = np.ones((3, 3), np.uint8)

    # prepare output
    # f, axes = plt.subplots(3,3)
    # axes = axes.ravel()
    # i = 0

    # axes[i].imshow(heatmap)
    # axes[i].set_title(f'({i+1}) original')
    # axes[i].axis('off')
    # i += 1

    # foreground pixels
    q = np.quantile(heatmap, FOREGROUND_QUANTILE)
    ret, sure_fg = cv.threshold(heatmap, q, 255, cv.THRESH_BINARY)

    # axes[i].imshow(sure_fg)
    # axes[i].set_title(f'({i+1}) foreground')
    # axes[i].axis('off')
    # i += 1

    # background pixels
    q = np.quantile(heatmap, BACKGROUND_QUANTILE)
    ret, sure_bg = cv.threshold(heatmap, q, 255, cv.THRESH_BINARY)

    # axes[i].imshow(sure_bg)
    # axes[i].set_title(f'({i+1}) background')
    # axes[i].axis('off')
    # i += 1

    # get peaks in foreground
    blurred = cv.blur(heatmap, (5, 5))  # blur image
    peaks = cv.dilate(
        blurred, kernel, iterations=1
    )  # set every pixel to the local maximum within kernel
    peaks = cv.compare(
        blurred, peaks, cv.CMP_GE
    )  # a peak is equal to its local maximum

    # axes[i].imshow(peaks)
    # axes[i].set_title(f'({i+1}) local maxima')
    # axes[i].axis('off')
    # i += 1

    peaks = cv.bitwise_and(peaks, sure_fg)  # only use peaks in foreground

    # axes[i].imshow(peaks)
    # axes[i].set_title(f'({i+1}) maxima in foreground')
    # axes[i].axis('off')
    # i += 1

    # merge peaks
    peaks = cv.dilate(
        peaks, kernel, iterations=MERGE_DISTANCE
    )  # dilute to merge nearby peaks
    peaks = cv.erode(
        peaks, kernel, iterations=MERGE_DISTANCE - 1
    )  # erode to shrink around merged peaks

    # axes[i].imshow(peaks)
    # axes[i].set_title(f'({i+1}) merged maxima')
    # axes[i].axis('off')
    # i += 1

    # unknown pixels
    unknown = cv.subtract(sure_bg, peaks)

    # axes[i].imshow(unknown)
    # axes[i].set_title(f'({i+1}) unkown regions')
    # axes[i].axis('off')
    # i += 1

    # initial markers for watershed
    ret, markers = cv.connectedComponents(peaks)
    markers = markers + 1
    markers[unknown == 255] = 0

    # axes[i].imshow(markers)
    # axes[i].set_title(f'({i+1}) initial markers')
    # axes[i].axis('off')
    # i += 1

    # execute watershed
    img = cv.cvtColor(heatmap, cv.COLOR_GRAY2BGR)  # watershed requires color image
    markers = cv.watershed(img, markers)

    # axes[i].imshow(markers)
    # axes[i].set_title(f'({i+1}) segmentation')
    # axes[i].axis('off')
    # i += 1

    markers[markers == 1] = 0
    markers[markers == -1] = 0

    return markers
