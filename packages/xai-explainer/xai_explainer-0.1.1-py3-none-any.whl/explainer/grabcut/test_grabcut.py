from tkinter.filedialog import askopenfilename

import cv2 as cv
import grabcut
from matplotlib import pyplot as plt
import numpy as np

# load image
filename = askopenfilename()
img = cv.imread(filename)
assert img is not None, "file could not be read"
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

# load heatmap
filename = askopenfilename()
heatmap = cv.imread(filename)
assert heatmap is not None, "file could not be read"
heatmap = cv.cvtColor(heatmap, cv.COLOR_BGR2GRAY)

# prepare output
f, axes = plt.subplots(2, 2)
axes = axes.ravel()
i = 0

axes[i].imshow(img)
axes[i].set_title("original")
axes[i].axis("off")
i += 1

axes[i].imshow(heatmap)
axes[i].set_title("heatmap")
axes[i].axis("off")
i += 1

_thresh_fgd = 0.7
_thresh_bgd = 0.3

q_fgd = np.quantile(heatmap, _thresh_fgd)
sure_fgd = cv.compare(heatmap, q_fgd, cv.CMP_GE)

q_bgd = np.quantile(heatmap, _thresh_bgd)
sure_bgd = cv.compare(heatmap, q_bgd, cv.CMP_LE)

mask = np.zeros(img.shape[:2], np.uint8)
mask[sure_fgd == 255] = 2
mask[sure_bgd == 255] = 1

axes[i].imshow(mask)
axes[i].set_title("initial mask")
axes[i].axis("off")
i += 1

relevant_area = grabcut.relevantAreaMask(img, heatmap, _thresh_bgd, _thresh_fgd)

axes[i].imshow(img * relevant_area[:, :, np.newaxis])
axes[i].set_title("relevant area")
axes[i].axis("off")
i += 1

plt.show()
