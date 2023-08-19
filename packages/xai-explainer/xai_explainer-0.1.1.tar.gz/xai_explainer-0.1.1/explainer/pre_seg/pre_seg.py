from functools import wraps
from typing import List, Optional, Tuple

import cv2
import networkx as nx
import numpy as np
from sklearn.cluster import SpectralClustering

__methods__ = {}


def filter_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _kwargs = {k: v for k, v in kwargs.items() if k in func.__code__.co_varnames}
        return func(*args, **_kwargs)

    return wrapper


def get_available_methods():
    return list(__methods__.keys())


def register(
    func: callable, transform: Optional[callable] = None, name: Optional[str] = None
) -> None:
    """
    Registers a function as a segmentation method.

    Parameters
    ----------
    func : callable
        Function to be registered.
    transform : callable, optional
        Function to be applied to the image before segmentation, by default None.
    name : str, optional
        Name of the function, by default None. If None, the function name is used.

    Returns
    -------
    None

    """

    global __methods__

    assert callable(func), "func must be callable"
    if name is None:
        name = func.__name__
    if transform is not None:
        assert callable(transform), "transform must be callable"
    __methods__[name] = (func, transform)
    return func


def segment(img: np.ndarray, method: str = "slic", **kwargs) -> np.ndarray:
    """
    Segments an RGB-image using the specified method.

    Parameters
    ----------
    img : np.ndarray
        RGB-Image to be segmented.
    method : str, optional
        Method to be used for segmentation, by default "slic"
    **kwargs
        Keyword arguments to be passed to the segmentation method.

    Returns
    -------
    np.ndarray
        Segmented image.

    Raises
    ------
    ValueError
        If the specified method is not found.

    """
    global __methods__
    if method not in __methods__:
        raise ValueError(f"Method {method} not found.")
    func, transform = __methods__[method]
    if transform is not None:
        img = transform(img)

    _res = func(img, **kwargs).astype(int)

    if _res.min() == 0:
        _res += 1

    return _res


def _eval_segment(
    segmentation: np.ndarray,
    heatmap: np.ndarray,
    segment_id: int,
    method: str = "mean",
    num_pixels: int = -1,
    **kwargs,
) -> float:
    segment_values = heatmap[segmentation == segment_id].flatten()
    if num_pixels > 0:
        num_pixels = min(num_pixels, segment_values.shape[0])
        segment_values = np.sort(segment_values)[-num_pixels:]
        assert segment_values.shape[0] == num_pixels

    if method == "mean":
        return segment_values.mean()
    elif method == "max":
        return segment_values.max()
    elif method == "min":
        return segment_values.min()
    elif method == "median":
        return np.median(segment_values)
    elif method in ["abs", "sum"]:
        return segment_values.sum()
    else:
        raise ValueError(f"Method {method} not found.")


def _extract_segments(
    segmentation: np.ndarray, segmentation_scores: dict, method="threshold", **kwargs
):
    relevant_segments = np.zeros_like(segmentation)
    if method == "threshold":
        threshold = kwargs.get("threshold", 0.25)

        for segment_id, score in segmentation_scores.items():
            if score >= threshold:
                relevant_segments[segmentation == segment_id] = segment_id

    elif method == "top_k_segments":
        num_segments = kwargs.get("num_segments", 10)
        num_segments = min(num_segments, len(segmentation_scores))
        relevant_segment_ids = sorted(
            segmentation_scores, key=segmentation_scores.get, reverse=True
        )[:num_segments]
        for segment_id in relevant_segment_ids:
            relevant_segments[segmentation == segment_id] = segment_id

    else:
        raise ValueError(f"Method {method} not found.")

    return relevant_segments


def merge_neighbors(
    segmentation: np.ndarray,
    heatmap: np.ndarray,
    method="normalized_graph_cut",
    num_parts=5,
    **kwargs,
) -> np.ndarray:
    """
    Merges neighboring segments.

    Parameters
    ----------
    segmentation : np.ndarray
        Segmentation to be filtered. Must be a 2D array of integers. Non-relevant segments must be set to 0.
    partition_method : str
        Method to be used for merging segments.
        Available methods: "normalized_graph_cut", "greedy_modularity", "girvan_newman", "louvain"
    num_parts : bool
        Sets the target number of parts when merging neighboring segments. Default: 5. Only relevant if partition_method == "normalized_graph_cut" or partition_method == "girvan_newman"
    Returns
    -------
    np.ndarray
        Filtered segmentation.

    """
    assert segmentation.shape == heatmap.shape

    relevant_segments = np.unique(segmentation)
    relevant_segments = sorted(relevant_segments)
    relevant_segments = [
        x for x in relevant_segments if x != 0
    ]  # remove background (0 values)
    max_segment = np.max(segmentation)
    segment_id_map = [
        relevant_segments.index(segment_id) if segment_id in relevant_segments else -1
        for segment_id in range(0, max_segment + 1)
    ]

    adj_matrix = construct_neighbor_graph(
        segmentation, heatmap, len(relevant_segments), segment_id_map
    )

    if method == "normalized_graph_cut":
        n_clusters, clustering = normalized_graph_cut(adj_matrix, num_parts)
    elif method == "greedy_modularity":
        n_clusters, clustering = greedy_modularity(adj_matrix)
    elif method == "girvan_newman":
        n_clusters, clustering = girvan_newman(adj_matrix, num_parts)
    elif method == "louvain":
        n_clusters, clustering = louvain(adj_matrix)

    merged_mapping = {segment_id: None for segment_id in relevant_segments}

    for i in range(n_clusters):
        s_id = -1
        for s in relevant_segments:
            if clustering[segment_id_map[s]] == i:
                if s_id < 0:
                    s_id = s
                merged_mapping[s] = s_id
    # print("merged mapping:", merged_mapping)

    segmentation = segmentation.copy()
    for segment_id in relevant_segments:
        segmentation[segmentation == segment_id] = merged_mapping[segment_id]

    return segmentation


def normalized_graph_cut(
    adj_matrix: np.ndarray, num_parts: int
) -> Tuple[int, list[int]]:
    clustering = SpectralClustering(n_clusters=num_parts, affinity="precomputed").fit(
        adj_matrix
    )
    return num_parts, clustering.labels_


def greedy_modularity(adj_matrix: np.ndarray) -> Tuple[int, list[int]]:
    n_segments = adj_matrix.shape[0]
    graph = nx.Graph(incoming_graph_data=adj_matrix)

    res = nx.community.greedy_modularity_communities(graph)

    clustering = [0 for i in range(n_segments)]
    n_clusters = len(res)
    for i in range(n_segments):
        for c in range(n_clusters):
            if i in res[c]:
                clustering[i] = c
                break
    return n_clusters, clustering


def girvan_newman(adj_matrix: np.ndarray, num_parts: int) -> Tuple[int, list[int]]:
    n_segments = adj_matrix.shape[0]
    graph = nx.Graph(incoming_graph_data=adj_matrix)

    comp = nx.community.girvan_newman(graph)

    res = next(comp)
    while len(res) < num_parts:
        res = next(comp)

    clustering = [0 for i in range(n_segments)]
    n_clusters = len(res)
    for i in range(n_segments):
        for c in range(n_clusters):
            if i in res[c]:
                clustering[i] = c
                break
    return n_clusters, clustering


def louvain(adj_matrix: np.ndarray) -> Tuple[int, list[int]]:
    n_segments = adj_matrix.shape[0]
    graph = nx.Graph(incoming_graph_data=adj_matrix)

    res = nx.community.louvain_communities(graph)

    clustering = [0 for i in range(n_segments)]
    n_clusters = len(res)
    for i in range(n_segments):
        for c in range(n_clusters):
            if i in res[c]:
                clustering[i] = c
                break
    return n_clusters, clustering


def construct_neighbor_graph(
    segmentation: np.ndarray, heatmap: np.ndarray, n_segments: int, segment_id_map: list
) -> np.ndarray:
    """
    Creates the neighbor graph
    The neighbor graph is a weighted undirected graph. It has one node for each relevant segment. The weight of an edge between two segments corresponds to the mean relevance along the border between these segments.

    Parameters
    ----------
    segmentation : np.ndarray
        Segmentation. Must be a 2D array of integers.
    heatmap: np.ndarray
        Heatmap. Must be a 2D array
    n_segments: int
        number of relevant segments
    segment_id_map: list
        assigns each segment which appears in segmentation a new id.
        id for relevant segments is between 0 (inclusive) and n_segments (exclusive)
        id for other segments is < 0

    Returns
    -------
    np.ndarray
        graph as adjacency matrix

    """

    _directions_4 = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
    ]  # neighbors for deciding if a pixel is a border or not
    _directions_8 = [
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1),
    ]  # neighbors for discovering new pixels

    discovered_segments = {
        segment_id: False for segment_id in range(0, n_segments)
    }  # bool if each relevant segment was discovered so that every segment is only counted once in n_discovered
    discovered_pixel = np.full(
        segmentation.shape, False
    )  # bool if each pixel was discovered so that every pixel is added at most once to the stack
    n_discovered = 0  # number of discovered segments
    relevance_sum = np.zeros((n_segments, n_segments))
    border_length = np.full(
        (n_segments, n_segments), 0.001
    )  # start with non-zero value to avoid dividing by zero for non-neighboring segments
    stack = [
        (0, 0)
    ]  # stack of all discovered pixels which were not yet visited. Starts at (0,0) which is guaranteed to be a border pixel
    discovered_pixel[(0, 0)] = True

    # coordinates for linear search
    i = -1  # i starts at -1 because loop increments coordinates first
    j = 0
    while n_discovered < n_segments:  # iterate until every segment was discovered...
        # if the stack is empty, use linear search to find the next undiscovered segment.
        # this search will only execute in edge-cases, if there is one segment fully enclosing one or more other segments
        while not stack:
            # increment i,j
            i += 1
            if i >= segmentation.shape[0]:
                i = 0
                j += 1
                assert (
                    j <= segmentation.shape[1]
                )  # j > segmentation.shape[1] means that the entire area was searched

            s = segmentation[i][j]
            if (
                segment_id_map[s] >= 0 and not discovered_segments[segment_id_map[s]]
            ):  # new segment discovered
                stack.append((i, j))  # add this segment
                discovered_pixel[(i, j)] = True
                break

        while stack:  # expore segments until stack is empty
            current = stack.pop()
            s = segmentation[current]

            # see if this is a border pixel
            is_border = False
            for direction in _directions_4:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if (
                    neighbor[0] < 0
                    or neighbor[1] < 0
                    or neighbor[0] >= segmentation.shape[0]
                    or neighbor[1] >= segmentation.shape[1]
                    or segmentation[neighbor] != s
                ):
                    is_border = True
                    break

            # only visit border pixels
            if is_border:
                # add all neighbors to the stack
                for direction in _directions_8:
                    neighbor = (current[0] + direction[0], current[1] + direction[1])

                    if (
                        neighbor[0] < 0
                        or neighbor[1] < 0
                        or neighbor[0] >= segmentation.shape[0]
                        or neighbor[1] >= segmentation.shape[1]
                    ):
                        continue  # skip out-of-bounds neighbors

                    # add all undiscovered neighbors to stack
                    if not discovered_pixel[neighbor]:
                        stack.append(neighbor)
                        discovered_pixel[neighbor] = True
                    # Note: we explore the borders of all segments, not only the relevant segments. This is to improve runtime. Exploring all segments means that we will only have to do a linear search if there is a segment which fully encloses one or more segments.

                if segment_id_map[s] >= 0:
                    # count this segment if this is the first time encountering it
                    if not discovered_segments[segment_id_map[s]]:
                        discovered_segments[segment_id_map[s]] = True
                        n_discovered += 1
                    # if this segment is relevant, look for borders with other relevant segments
                    for direction in _directions_4:
                        neighbor = (
                            current[0] + direction[0],
                            current[1] + direction[1],
                        )
                        if (
                            neighbor[0] < 0
                            or neighbor[1] < 0
                            or neighbor[0] >= segmentation.shape[0]
                            or neighbor[1] >= segmentation.shape[1]
                        ):
                            continue  # skip out-of-bounds neighbors

                        # increase edge-weight if neighbor belongs to different segment
                        s_n = segmentation[neighbor]
                        if s_n != s and segment_id_map[s_n] >= 0:
                            s_id = segment_id_map[s]
                            s_n_id = segment_id_map[s_n]
                            relevance_sum[(s_id, s_n_id)] += heatmap[current]
                            border_length[(s_id, s_n_id)] += 1
                            # enforce symatrical matrix
                            relevance_sum[(s_n_id, s_id)] += heatmap[current]
                            border_length[(s_n_id, s_id)] += 1

    return np.divide(relevance_sum, border_length)


def extract_relevant_segments(
    segmentation: np.ndarray,
    heatmap: np.ndarray,
    evaluation_method: str = "mean",
    extraction_method: str = "threshold",
    merge_neightbors: bool = True,
    partition_method="min_k_cut",
    num_parts=5,
    **kwargs,
) -> np.ndarray:
    """
    Extracts relevant segments from a segmentation based on a heatmap.

    Parameters
    ----------
    segmentation : np.ndarray
        Segmentation to be filtered. Must be a 2D array of integers.
    heatmap : np.ndarray
        Heatmap to be used for filtering. Must have the same shape as the segmentation.
        The heatmap must be normalized to the range [0, 1].
    evaluation_method : str, optional
        Method to be used for evaluating the segments, by default "mean".
        Available methods: "mean", "max", "min", "median", "sum".
        Additional keyword arguments:
            - num_pixels: Number of pixels (sorted descendingly) to be used for evaluation. If -1, all pixels are used.
    extraction_method : str, optional
        Method to be used for extracting the relevant segments, by default "threshold".
        Available methods: "threshold", "top_k_segments".
        Additional keyword arguments:
            - threshold: Threshold for the evaluation method. Default: 0.25. Only relevant if extraction_method == "threshold".
            - n_segments: Number of segments to be extracted. Default: 10. Only relevant if extraction_method == "top_k_segments".
    merge_neightbors : bool
        If True, neighboring segments are merged. Default: True.
    partition_method : str
        Method to be used for merging segments.
        Available methods: "normalized_graph_cut", "greedy_modularity", "girvan_newman", "louvain"
    num_parts : bool
        Sets the target number of parts when merging neighboring segments. Default: 5. Only relevant if merge_neighbors == true and if partition_method == "normalized_graph_cut" or partition_method == "girvan_newman"

    **kwargs
        Keyword arguments to be passed to the evaluation and extraction methods.

    Returns
    -------
    np.ndarray
        Relevant segments. Non-relevant segments are set to 0.

    """
    assert (
        segmentation.shape == heatmap.shape
    ), f"Shape mismatch: {segmentation.shape} != {heatmap.shape}"

    # 0-1 Normalization (heatmap)
    heatmap = heatmap.copy()
    heatmap -= heatmap.min()
    heatmap /= heatmap.max()

    segmentation_scores = {
        segment_id: _eval_segment(
            segmentation, heatmap, segment_id, method=evaluation_method, **kwargs
        )
        for segment_id in np.unique(segmentation)
    }

    relevant_segments = _extract_segments(
        segmentation, segmentation_scores, method=extraction_method, **kwargs
    )

    if merge_neightbors:
        relevant_segments = merge_neighbors(
            relevant_segments, heatmap, partition_method, num_parts, **kwargs
        )

    return relevant_segments


def bounding_boxes_from_segmentation(
    segmentation: np.ndarray,
) -> List[Tuple[int, int, int, int]]:
    """
    Computes the bounding boxes of a segmentation.

    Parameters
    ----------
    segmentation : np.ndarray
        Segmentation to be processed. Must be a 2D array of integers.

    Returns
    -------
    List[Tuple[int, int, int, int]]
        List of bounding boxes (x_min, y_min, x_max, y_max).

    """

    boxes = []

    for segment_id in np.unique(segmentation):
        if segment_id == 0:
            continue  # background

        segment = segmentation == segment_id
        segment = segment.astype(np.uint8)

        x_min = np.min(np.where(segment)[1])
        x_max = np.max(np.where(segment)[1])
        y_min = np.min(np.where(segment)[0])
        y_max = np.max(np.where(segment)[0])

        rect = (x_min, y_min, x_max, y_max)

        boxes.append(rect)

    return boxes


def extract_relevant_boxes(
    boxes: List[Tuple[str, str, str, str]],
    heatmap: np.ndarray,
    threshold: float = 0.2,
    top_k: int = 1,
) -> List[tuple]:
    """Extracts relevant boxes from a list of boxes based on a heatmap.

    Parameters
    ----------
    boxes : List[Tuple[str, str, str, str]]
        The boxes to be filtered. Each box is a tuple of the form (x1, y1, x2, y2).
    heatmap : np.ndarray
        The heatmap to be used for filtering. Must have the same shape as the image.
    threshold : float, optional
        Discard pixel in the heatmap, which have a lesser value, by default 0.2
    top_k : int, optional
        Return the top_k boxes, by default 1

    Returns
    -------
    List[tuple]
        A list of the top_k relevant boxes, where each entry is a tuple of the form (box, score).
    """
    # threshold heatmap
    heatmap = heatmap.copy()
    heatmap[heatmap < threshold] *= -1

    # plt.imshow(heatmap)
    # plt.show()

    # find boxes with highest score
    box_scores = {}
    for box in boxes:
        x1, y1, x2, y2 = box
        assert x1 <= x2 and y1 <= y2, f"Invalid box: {box}"
        inner = heatmap[y1:y2, x1:x2].sum()
        outer = heatmap.sum() - inner
        box_scores[box] = inner - outer

    # return top_k boxes with highest score
    sorted_box_scores = sorted(box_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_box_scores[:top_k]
