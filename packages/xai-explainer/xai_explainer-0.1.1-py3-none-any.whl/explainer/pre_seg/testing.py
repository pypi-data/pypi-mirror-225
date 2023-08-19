import os

from __init__ import (
    bounding_boxes_from_segmentation,
    extract_relevant_segments,
    segment,
)
import cv2
import numpy as np
from skimage import segmentation as seg

method = "slic"  # "felzenszwalb" # "slic" # "watershed" # "quickshift

img_path = "person.jpg"
if not os.path.exists(img_path):
    img_path = os.path.join(os.path.dirname(__file__), img_path)
    if not os.path.exists(img_path):
        raise FileNotFoundError("Image not found.")

img = cv2.imread(img_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Segmentation
print(f"Running {method} on {img_path}")
seg_img = segment(img, method=method, n_segments=1000, compactness=10)

# show segmentation on image
seg_img_boundaries = seg.mark_boundaries(img, seg_img)

seg_img_boundaries *= 255
seg_img_boundaries = seg_img_boundaries.astype(np.uint8)
seg_img_boundaries = cv2.cvtColor(seg_img_boundaries, cv2.COLOR_RGB2BGR)
cv2.imshow("Segmentation", seg_img_boundaries)
cv2.waitKey(0)
cv2.destroyAllWindows()

# random heatmap
print(img.shape)

img_path = "person_heatmap.png"
# img_path = "person_heatmap.pngda"  # force error
_exists = True
if not os.path.exists(img_path):
    img_path = os.path.join(os.path.dirname(__file__), img_path)
    if not os.path.exists(img_path):
        _exists = False
        print("Image not found.")

if not _exists:
    heatmap = np.zeros((img.shape[0], img.shape[1]), dtype=np.float32)
    print(heatmap.shape)
    for _ in range(1000):
        x = np.random.randint(0, img.shape[1])
        y = np.random.randint(0, img.shape[0])
        x_delta = np.random.randint(0, 25)
        y_delta = np.random.randint(0, 25)
        x1 = max(0, x - x_delta)
        y1 = max(0, y - y_delta)
        x2 = min(img.shape[1], x + x_delta)
        y2 = min(img.shape[0], y + y_delta)

        heatmap[y1:y2, x1:x2] += np.random.rand()

    heatmap /= heatmap.max()

else:
    heatmap = cv2.imread(img_path)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2GRAY)
    heatmap = heatmap.astype(np.float32)
    heatmap /= 255
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))

    assert len(heatmap.shape) == 2


# show heatmap on image
cv2.imshow("Random Heatmap", heatmap)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Extract relevant segments
relevant_segments = extract_relevant_segments(
    segmentation=seg_img,
    heatmap=heatmap,
    evaluation_method="mean",
    merge_neightbors=True,
    num_pixels=-1,
    extraction_method="top_k_segments",  # "threshold", "top_k_segments"
    threshold=0.35,
    num_segments=10,
)
relevant_segment_ids = np.unique(relevant_segments)
n_relevant_segments = np.unique(relevant_segments).shape[0] - 1
print(f"Found {n_relevant_segments} relevant segments.")
print(f"{relevant_segments.shape = }")
print(f"{relevant_segment_ids = }")

# show relevant segments on image
relevant_segments_img = np.zeros_like(img)
for segment_id in np.unique(relevant_segments):
    if segment_id != 0:
        mask = relevant_segments == segment_id
        relevant_segments_img[mask] = img[mask]


relevant_segments_boundaries = seg.mark_boundaries(
    relevant_segments_img, relevant_segments
)
relevant_segments_boundaries *= 255
relevant_segments_boundaries = relevant_segments_boundaries.astype(np.uint8)
relevant_segments_boundaries = cv2.cvtColor(
    relevant_segments_boundaries, cv2.COLOR_RGB2BGR
)

cv2.imshow("Relevant segments", relevant_segments_boundaries)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Extract bounding boxes
bounding_boxes = bounding_boxes_from_segmentation(relevant_segments)
print(f"{bounding_boxes = }")

# show bounding boxes on image
bounding_boxes_img = np.zeros_like(img)
for box in bounding_boxes:
    x1, y1, x2, y2 = box
    bounding_boxes_img = cv2.rectangle(
        bounding_boxes_img, (x1, y1), (x2, y2), (0, 255, 0), 2
    )

cv2.imshow("Bounding boxes", bounding_boxes_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
