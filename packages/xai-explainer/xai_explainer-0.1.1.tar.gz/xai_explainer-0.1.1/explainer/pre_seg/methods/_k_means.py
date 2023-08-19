import cv2
import numpy as np


def main(img, k=3):
    attempts = 6

    # convert MxNx3 img to (M * N)x3
    vectorized = img.reshape((-1, 3))

    # convert unit8 values to float
    vectorized = np.float32(vectorized)

    # Define criteria and apply kmeans
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(
        vectorized, k, None, criteria, attempts, cv2.KMEANS_RANDOM_CENTERS
    )

    # convert back to uint8
    center = np.uint8(center)

    # access the labels
    res = center[label.flatten()]
    result_image = res.reshape((img.shape))
    result_image = np.uint8(label.reshape(img.shape[:2]))

    return result_image
