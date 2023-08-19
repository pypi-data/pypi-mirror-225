import argparse

from __init__ import _selective_search
import cv2
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pre_seg


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--img", type=str, required=True, help="path to image")
    parser.add_argument("--heatmap", type=str, required=True, help="path to heatmap")
    parser.add_argument(
        "--threshold", type=float, default=0.2, help="threshold for heatmap"
    )
    parser.add_argument("--top_k", type=int, default=1, help="top k boxes to extract")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    # parse img
    args = _parse_args()
    img = cv2.imread(args.img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # parse heatmap
    heatmap = cv2.imread(args.heatmap)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2GRAY)
    heatmap = heatmap.astype(np.float32)
    heatmap /= 255
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))

    # run selective search and extract most relevant box
    boxes = _selective_search(img)
    most_relevant_boxes = pre_seg.extract_relevant_boxes(
        boxes=boxes, heatmap=heatmap, threshold=args.threshold, top_k=args.top_k
    )

    # draw boxes on the image
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(12, 12))
    ax[0].imshow(img)
    for x1, y1, x2, y2 in boxes:
        bbox = mpatches.Rectangle(
            (x1, y1), (x2 - x1), (y2 - y1), fill=False, edgecolor="red", linewidth=1
        )
        ax[0].add_patch(bbox)

    # draw most relevant boxes on the image
    ax[1].imshow(img)
    for idx, (box, score) in enumerate(most_relevant_boxes, start=1):
        x1, y1, x2, y2 = box
        bbox = mpatches.Rectangle(
            (x1, y1), (x2 - x1), (y2 - y1), fill=False, edgecolor="red", linewidth=1
        )
        ax[1].add_patch(bbox)
        ax[1].text(x1, y1, f"{idx:.2f}", color="red", fontsize=8)

    # draw heatmap
    ax[2].imshow(heatmap)

    plt.axis("off")
    plt.show()
