from tkinter.filedialog import askopenfilename

import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import region_growing

# load image
filename = askopenfilename()
img = cv.imread(filename)
assert img is not None, "file could not be read"
# img = cv.resize(img, dsize = None, fx = 0.35, fy = 0.35)

# prepare output
f, axes = plt.subplots(2, 2)
axes = axes.ravel()
i = 0

axes[i].imshow(img)
axes[i].set_title("original")
axes[i].axis("off")
i += 1

# convert to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

axes[i].imshow(gray)
axes[i].set_title("gray")
axes[i].axis("off")
i += 1

segmentation = region_growing.segmentation(gray)

axes[i].imshow(segmentation)
axes[i].set_title("segmentation")
axes[i].axis("off")
i += 1

img[segmentation == -1] = [255, 0, 0]

axes[i].imshow(img)
axes[i].set_title("overlay")
axes[i].axis("off")
i += 1

cv.imwrite(f"{filename}seg.png", img)

plt.show()
