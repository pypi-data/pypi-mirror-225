import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np


def relevantAreaMask(
    img: np.ndarray, heatmap: np.ndarray, thresh_bgd=0.05, thresh_fgd=0.95
):
    q_fgd = np.quantile(heatmap, thresh_fgd)
    sure_fgd = cv.compare(heatmap, q_fgd, cv.CMP_GE)

    q_bgd = np.quantile(heatmap, thresh_bgd)
    sure_bgd = cv.compare(heatmap, q_bgd, cv.CMP_LE)

    mask = np.full(img.shape[:2], cv.GC_PR_BGD, np.uint8)
    mask[sure_fgd == 255] = cv.GC_FGD
    mask[sure_bgd == 255] = cv.GC_BGD

    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    mask, bgdModel, fgdModel = cv.grabCut(
        img, mask, None, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_MASK
    )

    return np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
