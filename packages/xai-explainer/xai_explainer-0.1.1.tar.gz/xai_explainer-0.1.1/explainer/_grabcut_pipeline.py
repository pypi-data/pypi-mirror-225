import math
from tkinter.filedialog import askopenfilename

import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import skimage.segmentation as seg

import explainer.grabcut as grabcut
import explainer.part_extr as part_extr
import explainer.pre_seg as pre_seg


def main():
    _thresh_fgd = 0.8
    _thresh_bgd = 0.4
    _seg_method = "slic"  # "felzenszwalb" # "slic" # "watershed" # "quickshift
    _merge_method = "louvain"  # "normalized_graph_cut" # "greedy_modularity" # "girvan_newman" # "louvain"
    _num_parts = 5  # only relevant for  "normalized_graph_cut" and "girvan_newman"
    _cut = True
    _replace = "blur"  # "mean" # "zero" # "blur" # else

    _show_images = True
    _save_parts = True

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

    relevant_area = grabcut.relevantAreaMask(img, heatmap, _thresh_bgd, _thresh_fgd)

    seg_img = pre_seg.segment(
        img=img, method=_seg_method, n_segments=200, compactness=10, mask=relevant_area
    )
    seg_img[seg_img == 1] = 0

    seg_img_merged = pre_seg.merge_neighbors(
        seg_img, heatmap, _merge_method, _num_parts
    )

    if _show_images:
        show_segmentation(img, heatmap, relevant_area, seg_img, seg_img_merged)

    parts = part_extr.extract_parts(seg_img_merged, img, heatmap, _cut, _replace)

    if _show_images:
        show_parts(parts)
    if _save_parts:
        save_parts(parts, filename)


def show_segmentation(img, heatmap, relevant_area, seg_img, seg_img_merged):
    f, axes = plt.subplots(2, 3)
    axes = axes.ravel()
    i = 0

    axes[i].imshow(img)
    axes[i].set_title("image")
    axes[i].axis("off")
    i += 1

    axes[i].imshow(heatmap)
    axes[i].set_title("heatmap")
    axes[i].axis("off")
    i += 1

    axes[i].imshow(img * relevant_area[:, :, np.newaxis])
    axes[i].set_title("relevant area")
    axes[i].axis("off")
    i += 1

    relevant_img = img * relevant_area[:, :, np.newaxis]

    seg_img_boundaries = seg.mark_boundaries(relevant_img, seg_img)

    seg_img_boundaries *= 255
    seg_img_boundaries = seg_img_boundaries.astype(np.uint8)

    axes[i].imshow(seg_img_boundaries)
    axes[i].set_title("segmented")
    axes[i].axis("off")
    i += 1

    seg_img_merged_boundaries = seg.mark_boundaries(relevant_img, seg_img_merged)

    seg_img_merged_boundaries *= 255
    seg_img_merged_boundaries = seg_img_merged_boundaries.astype(np.uint8)

    axes[i].imshow(seg_img_merged_boundaries)
    axes[i].set_title("merged")
    axes[i].axis("off")
    i += 1
    axes[i].axis("off")

    plt.show()


def show_parts(parts):
    # prepare output
    width = math.ceil(math.sqrt(len(parts)))
    height = math.ceil(len(parts) / width)
    f, axes = plt.subplots(width, height)
    axes = axes.ravel()
    i = 0

    for idx, p in enumerate(parts):
        axes[i].imshow(p[0])
        axes[i].set_title(f"part {idx}")
        axes[i].axis("off")
        i += 1

    for j in range(i, width * height):
        axes[j].axis("off")

    plt.show()


def save_parts(parts, path):
    if path != "":
        for idx, p in enumerate(parts):
            img = cv.cvtColor(p[0], cv.COLOR_RGB2BGR)
            cv.imwrite(f"{path}_part_{idx}.png", img)


if __name__ == "__main__":
    # call with: python3 test_pipeline.py --image <path/to/image.jpg>
    # e.g. python3 test_pipeline.py --image /data/tpeitsch/test_images/motorcycle.jpg
    main()
