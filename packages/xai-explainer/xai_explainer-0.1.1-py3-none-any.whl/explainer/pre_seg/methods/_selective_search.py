# https://github.com/ChenjieXu/selective_search

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import selective_search


def main(img):
    """Proposes boxes for object detection.

    Parameters
    ----------
    img : Any
        The image to apply selective search to.

    Returns
    -------
    List[Tuple[str, str, str, str]]
        A List of boxes (x1, y1, x2, y2)
    """
    # Run selective search
    # mode = single | fast | quality
    boxes = selective_search.selective_search(img, mode="fast", random_sort=False)

    # Filter box proposals
    boxes_filter = selective_search.box_filter(boxes, min_size=20, topN=80)

    ## draw rectangles on the original image
    # fig, ax = plt.subplots(figsize=(6, 6))
    # ax.imshow(img)
    # for x1, y1, x2, y2 in boxes_filter:
    #    bbox = mpatches.Rectangle(
    #        (x1, y1), (x2 - x1), (y2 - y1), fill=False, edgecolor="red", linewidth=1
    #    )
    #    ax[0, 0].add_patch(bbox)
    #
    # plt.axis("off")
    # plt.show()

    return boxes_filter
