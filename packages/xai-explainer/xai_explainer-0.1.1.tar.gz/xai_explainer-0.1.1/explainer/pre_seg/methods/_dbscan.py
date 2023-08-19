import numpy as np
from sklearn.cluster import DBSCAN


def main(img, **kwargs):
    # convert MxNx3 img to (M * N)x3 and to float
    Z = np.float32(img.reshape((-1, 3)))

    # apply DBSCAN
    db = DBSCAN(eps=2, min_samples=100).fit(Z[:, :2])

    # convert back to uint8 and access labels
    return np.uint8(db.labels_.reshape(img.shape[:2]))
