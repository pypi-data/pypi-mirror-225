from typing import Any, Dict, List, Tuple
import numpy as np
from scipy.spatial.distance import (
    chebyshev as chebyshev_distance,
    cosine as cosine_distance,
    euclidean as euclidean_distance,
    minkowski as minkowski_distance,
    cityblock as manhattan_distance,
)
from sklearn.cluster import MiniBatchKMeans
from dl_matrix.coordinate.base import Coordinate
from dl_matrix.coordinate.tree import CoordinateTree


def cluster_coordinates(
    coordinates: List[Coordinate], k: int, distance_metric: str
) -> List[Coordinate]:
    if distance_metric not in ["euclidean", "cosine"]:
        raise ValueError(f"Invalid distance metric: {distance_metric}")

    kmeans = MiniBatchKMeans(
        n_clusters=k,
        random_state=0,
        init="k-means++",
        max_iter=100,
        n_init=1,
        verbose=False,
    ).fit([coord.z for coord in coordinates])

    cluster_centers = kmeans.cluster_centers_
    return [
        Coordinate(x=0, y=0, z=cluster_center) for cluster_center in cluster_centers
    ]


def cluster_prompts(
    prompts: List[List[float]], k: int, distance_metric: str
) -> List[List[float]]:
    if distance_metric not in ["euclidean", "cosine"]:
        raise ValueError(f"Invalid distance metric: {distance_metric}")

    kmeans = MiniBatchKMeans(
        n_clusters=k,
        random_state=0,
        init="k-means++",
        max_iter=100,
        n_init=1,
        verbose=False,
    ).fit(prompts)

    return kmeans.cluster_centers_


class KMeansMatcher:
    def __init__(self, distance_metric: str, k: int):
        self.distance_metric = distance_metric
        self.k = k

    @staticmethod
    def _calculate_distance(
        coord1: "Coordinate", coord2: "Coordinate", distance_metric: str
    ) -> float:
        if distance_metric == "euclidean":
            return euclidean_distance(coord1, coord2)
        elif distance_metric == "cosine":
            return cosine_distance(coord1, coord2)
        elif distance_metric == "minkowski":
            return minkowski_distance(coord1, coord2)
        elif distance_metric == "chebyshev":
            return chebyshev_distance(coord1, coord2)
        elif distance_metric == "manhattan":
            return manhattan_distance(coord1, coord2)
        else:
            raise ValueError(f"Invalid distance metric: {distance_metric}")

    def match_coordinate(
        self, coord: Coordinate, coordinates: List[Coordinate]
    ) -> Coordinate:
        distances = [
            self._calculate_distance(coord, other_coord, self.distance_metric)
            for other_coord in coordinates
        ]
        min_distance = min(distances)
        min_distance_idx = distances.index(min_distance)
        return coordinates[min_distance_idx]

    def match_coordinates(self, coordinates: List[Coordinate]) -> List[Coordinate]:
        return [self.match_coordinate(coord, coordinates) for coord in coordinates]

    def match(
        self, coordinates: List[Coordinate], type: str = "cluster"
    ) -> List[Coordinate]:
        if type == "match":
            return self.match_coordinates(coordinates)
        elif type == "cluster":
            return cluster_coordinates(coordinates, self.k, self.distance_metric)
        else:
            raise ValueError(f"Invalid type: {type}")

    def match_batch(
        self, coordinates: List[List[Coordinate]], type: str = "cluster"
    ) -> List[List[Coordinate]]:
        if type == "match":
            return [self.match_coordinates(coord) for coord in coordinates]
        elif type == "cluster":
            return [
                cluster_coordinates(coord, self.k, self.distance_metric)
                for coord in coordinates
            ]
        else:
            raise ValueError(f"Invalid type: {type}")

    @staticmethod
    def _find_messages_exact_coordinates(
        coordinates: Tuple[float, float, float, float],
        tetra_dict: Dict[str, Coordinate],
    ) -> List[str]:
        return [
            message_id
            for message_id, coords in tetra_dict.items()
            if np.allclose(coords[:3], coordinates[:3])
        ]

    @staticmethod
    def _find_messages_similar_coordinates(
        coordinates: Tuple[float, float, float, float],
        tetra_dict: Dict[str, Coordinate],
        message_dict: Dict[str, Any],
        tolerance: float,
        distance_metric: str,
    ) -> List[Dict[str, Any]]:
        messages = []
        for message_id, message_coords in tetra_dict.items():
            # Convert the Coordinate to a tuple before passing it in
            distance = KMeansMatcher._calculate_distance(
                Coordinate.from_tuple(message_coords.to_tuple()),
                Coordinate.from_tuple(coordinates),
                distance_metric,
            )
            if distance <= tolerance:
                messages.append(message_dict[message_id])
        return messages

    def find_messages(
        self,
        coordinates: Tuple[float, float, float, float],
        tetra_dict: Dict[str, Coordinate],
        message_dict: Dict[str, Any],
        tolerance: float,
    ) -> List[Dict[str, Any]]:
        exact_messages = self._find_messages_exact_coordinates(coordinates, tetra_dict)
        similar_messages = self._find_messages_similar_coordinates(
            coordinates, tetra_dict, message_dict, tolerance, self.distance_metric
        )
        return exact_messages + similar_messages

    def find_messages_batch(
        self,
        coordinates: List[Tuple[float, float, float, float]],
        tetra_dict: Dict[str, Coordinate],
        message_dict: Dict[str, Any],
        tolerance: float,
    ) -> List[List[Dict[str, Any]]]:
        exact_messages = [
            self._find_messages_exact_coordinates(coord, tetra_dict)
            for coord in coordinates
        ]
        similar_messages = [
            self._find_messages_similar_coordinates(
                coord, tetra_dict, message_dict, tolerance, self.distance_metric
            )
            for coord in coordinates
        ]
        return [
            exact + similar for exact, similar in zip(exact_messages, similar_messages)
        ]


class CoordinateTreeMatcher:
    def __init__(
        self,
        distance_metric: str,
        k: int,
        max_depth: int,
        max_siblings: int,
        max_sibling_count: int,
        max_time: int,
    ):
        self.distance_metric = distance_metric
        self.k = k
        self.max_depth = max_depth
        self.max_siblings = max_siblings
        self.max_sibling_count = max_sibling_count
        self.max_time = max_time

    @staticmethod
    def _calculate_distance(
        coordinate1: Coordinate, coordinate2: Coordinate, distance_metric: str
    ) -> float:
        if distance_metric == "euclidean":
            return np.linalg.norm(
                Coordinate.flatten(coordinate1) - Coordinate.flatten(coordinate2)
            )
        elif distance_metric == "cosine":
            return cosine_distance(
                Coordinate.flatten(coordinate1), Coordinate.flatten(coordinate2)
            )
        else:
            raise ValueError(f"Invalid distance metric: {distance_metric}")

    def _calculate_distances(
        self, coordinate1: Coordinate, coordinate2: Coordinate
    ) -> List[float]:
        return [
            self._calculate_distance(coordinate1, coordinate2, self.distance_metric)
        ]

    def _calculate_tree_distances(
        self, tree1: CoordinateTree, tree2: CoordinateTree
    ) -> List[float]:
        return [
            self._calculate_distance(
                tree1.coordinate, tree2.coordinate, self.distance_metric
            )
        ]

    def _calculate_tree_distances_recursive(
        self, tree1: CoordinateTree, tree2: CoordinateTree
    ) -> List[float]:
        distances = self._calculate_tree_distances(tree1, tree2)
        for child1, child2 in zip(tree1.children, tree2.children):
            distances.extend(self._calculate_tree_distances_recursive(child1, child2))
        return distances

    def _calculate_tree_distances_recursive_with_depth(
        self, tree1: CoordinateTree, tree2: CoordinateTree, depth: int
    ) -> List[float]:
        distances = self._calculate_tree_distances(tree1, tree2)
        for child1, child2 in zip(tree1.children, tree2.children):
            if depth < self.max_depth:
                distances.extend(
                    self._calculate_tree_distances_recursive_with_depth(
                        child1, child2, depth + 1
                    )
                )
        return distances

    def _calculate_tree_distances_recursive_with_siblings(
        self, tree1: CoordinateTree, tree2: CoordinateTree, siblings: int
    ) -> List[float]:
        distances = self._calculate_tree_distances(tree1, tree2)
        for child1, child2 in zip(tree1.children, tree2.children):
            if siblings < self.max_siblings:
                distances.extend(
                    self._calculate_tree_distances_recursive_with_siblings(
                        child1, child2, siblings + 1
                    )
                )
        return distances

    def cluster_coordinates(
        self,
        tetra_dict: Dict[str, Coordinate],
        k: int,
        type: str = "cluster",
        distance_metric: str = "euclidean",
    ) -> List[Coordinate]:
        """Cluster the coordinates based on the k-means clustering algorithm.

        Args:
            k (int): The number of clusters.
            type (str, optional): The type of operation, either 'match' or 'cluster'. Defaults to 'cluster'.
            distance_metric (str, optional): The distance metric for k-means clustering.
                                            Can be either 'euclidean' or 'cosine'. Defaults to 'euclidean'.

        Returns:
            List[Coordinate]: List of matched or cluster center coordinates.
        """
        coordinates = list(tetra_dict.values())
        matcher = KMeansMatcher(distance_metric, k)
        return matcher.match(coordinates, type)

    def cluster_prompts(
        self,
        prompts: List[List[float]],
        k: int,
        type: str = "cluster",
        distance_metric: str = "euclidean",
    ) -> List[List[float]]:
        """Cluster the prompts based on the k-means clustering algorithm.

        Args:
            prompts (List[List[float]]): The list of prompts.
            k (int): The number of clusters.
            type (str, optional): The type of operation, either 'match' or 'cluster'. Defaults to 'cluster'.
            distance_metric (str, optional): The distance metric for k-means clustering.
                                            Can be either 'euclidean' or 'cosine'. Defaults to 'euclidean'.

        Returns:
            List[List[float]]: List of matched or cluster center prompts.
        """
        matcher = KMeansMatcher(distance_metric, k)
        return matcher.match(prompts, type)

    def cluster_coordinates_batch(
        self,
        tetra_dict: Dict[str, Coordinate],
        k: int,
        type: str = "cluster",
        distance_metric: str = "euclidean",
    ) -> List[Coordinate]:
        """Cluster the coordinates based on the k-means clustering algorithm.

        Args:
            k (int): The number of clusters.
            type (str, optional): The type of operation, either 'match' or 'cluster'. Defaults to 'cluster'.
            distance_metric (str, optional): The distance metric for k-means clustering.
                                            Can be either 'euclidean' or 'cosine'. Defaults to 'euclidean'.

        Returns:
            List[Coordinate]: List of matched or cluster center coordinates.
        """
        coordinates = list(tetra_dict.values())
        matcher = KMeansMatcher(distance_metric, k)
        return matcher.match_batch(coordinates, type)
