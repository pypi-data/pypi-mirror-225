import math
from collections import deque
from sklearn.cluster import DBSCAN
from fastdtw import fastdtw
from dl_matrix.transformation.base import Operations, Coordinate
from dl_matrix.transformation.tree import CoordinateTree
from typing import List, Tuple, Dict, Union, Optional, Deque
import math
import numpy as np


class CoordinateOperations(Operations):
    """
    The `CoordinateOperations` class is responsible for providing tools to:
    - Predict movements
    - Calculate effects of gravity wells
    - Optimize paths to specific coordinates
    - Determine visible fields of view
    - Detect points in the vicinity of high gravity

    Attributes:
    - tree: An instance of the `CoordinateTree`, which represents a hierarchical structure of coordinates.
    - history: A dictionary that maps each node's `root_id` to a deque tracking the last 100 positions.
    - subscribers: A list to store potential subscribers for any real-time updates or notifications. (Placeholder for now)
    - gravity_wells: A list of tuples where each tuple represents the position and strength of a gravity well.
    """

    def __init__(
        self,
        tree: List["CoordinateTree"],
        gravity_wells: List[Tuple[Tuple[float, float, float], float]],
    ):
        """
        Initialize the CoordinateOperations with a given CoordinateTree.

        Parameters:
        - tree (CoordinateTree): A tree of hierarchical coordinates.
        """
        self.tree = tree
        self.history = {
            node.root_id: deque(maxlen=100) for node in self.tree
        }  # Store the last 100 positions for each node

        self.gravity_wells = gravity_wells  # List of gravity wells and their strengths

    def add_gravity_well(self, position, strength):
        """Introduce gravity wells that can pull the coordinate."""
        self.gravity_wells.append((position, strength))

    def _extract_coordinate(
        self, item: Union["Coordinate", "CoordinateTree"]
    ) -> "Coordinate":
        """Private utility function to fetch the coordinate from either a Coordinate or a CoordinateTree."""
        return item if isinstance(item, Coordinate) else item.coordinate_node

    def compute_gravity_effect(
        self, item: Union["Coordinate", "CoordinateTree"]
    ) -> Dict[str, float]:
        """
        Calculate the net gravitational force exerted on a coordinate (or node in the tree) due to all gravity wells.

        Parameters:
        - item (Union[Coordinate, CoordinateTree]): The coordinate or tree node to calculate the gravitational effect for.

        Returns:
        - Dict[str, float]: A dictionary representing the gravitational forces in x, y, and z directions.
        """
        coordinate = self._extract_coordinate(item)
        net_force = {"dx": 0, "dy": 0, "dz": 0}
        for well, strength in self.gravity_wells:
            distance = math.dist((coordinate.x, coordinate.y, coordinate.z), well)
            if distance == 0:  # To avoid division by zero.
                continue
            force = strength / (distance**2)
            net_force["dx"] += force * (well[0] - coordinate.x)
            net_force["dy"] += force * (well[1] - coordinate.y)
            net_force["dz"] += force * (well[2] - coordinate.z)
        return net_force

    def optimize_path_to(
        self,
        item: Union["Coordinate", "CoordinateTree"],
        target_coordinate: "Coordinate",
    ) -> List["Coordinate"]:
        """
        Compute the most efficient path to a target coordinate considering gravitational effects.

        Parameters:
        - item (Union[Coordinate, CoordinateTree]): The starting point.
        - target_coordinate (Coordinate): The destination.

        Returns:
        - List[Coordinate]: A list of coordinates representing the optimized path.
        """
        current = self._extract_coordinate(item)
        path = [current]
        while current != target_coordinate:
            effects = self.compute_gravity_effect(current)
            movement = {
                "x": (target_coordinate.x - current.x) + effects["dx"],
                "y": (target_coordinate.y - current.y) + effects["dy"],
                "z": (target_coordinate.z - current.z) + effects["dz"],
            }
            current = Coordinate(
                x=current.x + movement["x"],
                y=current.y + movement["y"],
                z=current.z + movement["z"],
            )
            path.append(current)
        return path

    def field_of_view(
        self,
        item: Union["Coordinate", "CoordinateTree"],
        all_coordinates: List["Coordinate"],
        view_radius: float,
    ) -> List["Coordinate"]:
        """
        Determine which coordinates are visible from the current position within a specific radius.

        Parameters:
        - item (Union[Coordinate, CoordinateTree]): The current position or node.
        - all_coordinates (List[Coordinate]): A list of all potential coordinates that could be visible.
        - view_radius (float): The radius within which coordinates are considered visible.

        Returns:
        - List[Coordinate]: A list of coordinates that are visible.
        """
        coordinate = self._extract_coordinate(item)
        visible = []
        for coord in all_coordinates:
            distance = math.dist(
                (coordinate.x, coordinate.y, coordinate.z), (coord.x, coord.y, coord.z)
            )
            if distance <= view_radius:
                visible.append(coord)
        return visible

    def event_horizon_detection(
        self, item: Union["Coordinate", "CoordinateTree"]
    ) -> List[Tuple[float, float, float]]:
        """
        Identify points near a gravity well where the gravitational pull becomes too strong, effectively acting as points of no return.

        Parameters:
        - item (Union[Coordinate, CoordinateTree]): The current position or node to calculate critical points for.

        Returns:
        - List[Tuple[float, float, float]]: A list of critical points in the vicinity of strong gravity wells.
        """
        coordinate = self._extract_coordinate(item)
        critical_points = []
        for well, strength in self.gravity_wells:
            if (
                strength > 10
            ):  # Threshold which can be adjusted based on domain knowledge.
                distance = math.sqrt(strength / 10)
                critical_point = (
                    well[0] + (coordinate.x - well[0]) / distance,
                    well[1] + (coordinate.y - well[1]) / distance,
                    well[2] + (coordinate.z - well[2]) / distance,
                )
                critical_points.append(critical_point)
        return critical_points

    def update_history(self):
        """
        Update the history with the current positions of all nodes.
        """
        for node in self.tree:
            self.history[node.root_id].append(node.coordinate_node)

    def predict_next_move_for_all_nodes(
        self, external_forces: Optional[List[Tuple["Coordinate", float]]] = None
    ) -> Dict[str, Dict]:
        """
        Predict the next movement for all nodes in the tree, considering external forces.

        Returns:
        - Dict[str, Dict]: Dictionary mapping node IDs to their predicted movements.
        """
        return {
            node.root_id: self.predict_next_move(node, external_forces)
            for node in self.tree
        }

    def predict_next_move(
        self,
        node: "CoordinateTree",
        external_forces: Optional[List[Tuple["Coordinate", float]]] = None,
    ) -> Dict:
        """
        Predict the next movement for a specific node, based on its history and external forces.

        Returns:
        - Dict: Contains the predicted positions and a confidence score.
        """
        coordinate = node.coordinate_node
        node_history = self.history.get(node.root_id, deque())

        avg_deltas = {
            "x": self._calculate_avg_delta(node_history, "x"),
            "y": self._calculate_avg_delta(node_history, "y"),
            "z": self._calculate_avg_delta(node_history, "z"),
            "t": self._calculate_avg_delta(node_history, "t"),
        }

        self._adjust_for_forces(avg_deltas, coordinate, external_forces)

        predicted_positions = {
            "x": coordinate.x + avg_deltas["x"],
            "y": coordinate.y + avg_deltas["y"],
            "z": coordinate.z + avg_deltas["z"],
            "t": coordinate.t + avg_deltas["t"],
        }

        confidence = self.compute_prediction_confidence(avg_deltas)

        return {
            "predicted_positions": Coordinate(**predicted_positions),
            "confidence": confidence,
        }

    def _calculate_avg_delta(
        self, node_history: Deque["Coordinate"], axis: str
    ) -> float:
        """
        Compute the average movement for a given axis from the node's historical data.

        Returns:
        - float: Average delta of the node's movement for the specified axis.
        """
        if not node_history or len(node_history) < 2:
            return 0

        deltas = [
            getattr(node_history[i], axis) - getattr(node_history[i - 1], axis)
            for i in range(1, len(node_history))
        ]
        return sum(deltas) / len(deltas)

    def _adjust_for_forces(
        self,
        avg_deltas: Dict[str, float],
        coordinate: "Coordinate",
        external_forces: Optional[List[Tuple["Coordinate", float]]] = None,
    ) -> None:
        """
        Adjust the predicted movements based on the effects of gravitational and external forces.
        """
        for well, strength in self.gravity_wells:
            effect = self.compute_gravity_effect_on_point(coordinate, well, strength)
            for axis in avg_deltas:
                avg_deltas[axis] += effect[axis]

        if external_forces:
            for force_location, force_strength in external_forces:
                direction_factor = self.get_direction_factor(coordinate, force_location)
                for axis in avg_deltas:
                    avg_deltas[axis] += direction_factor[axis] * force_strength

    def compute_gravity_effect_on_point(
        self, point: "Coordinate", well: Tuple[float, float, float], strength: float
    ) -> Dict[str, float]:
        """
        Calculate the gravitational effect on a given point due to a specified gravity well.

        Returns:
        - Dict[str, float]: Gravitational effect on the point across each axis.
        """
        distance = math.dist([point.x, point.y, point.z], well)
        if distance == 0:
            return {"x": 0, "y": 0, "z": 0}

        scaling_factor = strength / (distance**2)

        return {
            "x": scaling_factor * (well[0] - point.x),
            "y": scaling_factor * (well[1] - point.y),
            "z": scaling_factor * (well[2] - point.z),
        }

    def get_direction_factor(
        self, start: "Coordinate", end: "Coordinate"
    ) -> Dict[str, float]:
        """
        Calculate the normalized directional factor between two points.

        Returns:
        - Dict[str, float]: Directional factor for each axis.
        """
        dist = math.dist([start.x, start.y, start.z], [end.x, end.y, end.z])
        if dist == 0:
            return {"x": 0, "y": 0, "z": 0}

        return {
            "x": (end.x - start.x) / dist,
            "y": (end.y - start.y) / dist,
            "z": (end.z - start.z) / dist,
        }

    def compute_prediction_confidence(self, avg_deltas: Dict[str, float]) -> float:
        """
        Compute the confidence score for a movement prediction based on historical variance.

        Returns:
        - float: Confidence score between 0 (low confidence) and 1 (high confidence).
        """
        variance = np.var(list(avg_deltas.values()))
        return 1 - min(1, variance)

    def detect_anomaly(self) -> List[int]:
        """
        Detect unusual movements by checking rapid changes in direction.

        Returns:
        - List[int]: Indices of the detected anomalies in the history.
        """
        anomalies = []

        for node_id, node_history in self.history.items():
            for i in range(2, len(node_history)):
                v1 = np.array(
                    [
                        node_history[i - 1].x - node_history[i - 2].x,
                        node_history[i - 1].y - node_history[i - 2].y,
                        node_history[i - 1].z - node_history[i - 2].z,
                    ]
                )
                v2 = np.array(
                    [
                        node_history[i].x - node_history[i - 1].x,
                        node_history[i].y - node_history[i - 1].y,
                        node_history[i].z - node_history[i - 1].z,
                    ]
                )

                cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                angle = np.arccos(np.clip(cos_angle, -1, 1))

                if angle > np.pi / 2:
                    anomalies.append(i)

        return anomalies

    def temporal_influence(self) -> float:
        """
        Analyze how t influences movements.

        Returns:
        - float: Average temporal influence between nodes.
        """
        time_influences = []

        for node_id, node_history in self.history.items():
            time_influences.extend(
                [
                    node_history[i].t - node_history[i - 1].t
                    for i in range(1, len(node_history))
                ]
            )

        avg_influence = (
            sum(time_influences) / len(time_influences) if time_influences else 0
        )

        return avg_influence

    def cluster_coordinates(
        self, coordinates: List["Coordinate"]
    ) -> Dict[int, List["Coordinate"]]:
        """
        Cluster coordinates based on proximity using DBSCAN.

        Returns:
        - Dict[int, List[Coordinate]]: Dictionary mapping cluster labels to their coordinates.
        """
        coord_array = np.array([[coord.x, coord.y, coord.z] for coord in coordinates])
        clustering = DBSCAN(eps=3, min_samples=2).fit(coord_array)
        labels = clustering.labels_

        clusters = {}
        for i, label in enumerate(labels):
            clusters.setdefault(label, []).append(coordinates[i])

        return clusters

    def get_energy_consumption(self, path: List["Coordinate"]) -> float:
        """
        Estimate the energy consumed when following a given path.

        Returns:
        - float: Estimated energy consumption.
        """
        energy = 0

        for i in range(1, len(path)):
            dist = np.linalg.norm(
                [
                    path[i].x - path[i - 1].x,
                    path[i].y - path[i - 1].y,
                    path[i].z - path[i - 1].z,
                ]
            )
            energy += dist + self.compute_gravity_effect_on_path_segment(
                path[i - 1], path[i]
            )

        return energy

    def compute_gravity_effect_on_path_segment(
        self, start: "Coordinate", end: "Coordinate"
    ) -> float:
        """
        Compute gravity effect on a segment of the path.

        Returns:
        - float: Gravity effect on the path segment.
        """
        segment_length = np.linalg.norm(
            [start.x - end.x, start.y - end.y, start.z - end.z]
        )
        gravity_effect = 0

        for well, strength in self.gravity_wells:
            closest_point_on_segment = self.get_closest_point_on_line(start, end, well)
            distance_to_well = np.linalg.norm(
                [
                    closest_point_on_segment.x - well[0],
                    closest_point_on_segment.y - well[1],
                    closest_point_on_segment.z - well[2],
                ]
            )
            gravity_effect += strength / (
                distance_to_well**2 if distance_to_well != 0 else 1
            )

        return gravity_effect * segment_length

    @staticmethod
    def get_closest_point_on_line(
        a: "Coordinate", b: "Coordinate", p: Tuple[float, float, float]
    ) -> "Coordinate":
        """
        Get the closest point on the line segment AB to point P.

        Returns:
        - Coordinate: Closest point on the line segment.
        """
        ap = np.array([p[0] - a.x, p[1] - a.y, p[2] - a.z])
        ab = np.array([b.x - a.x, b.y - a.y, b.z - a.z])
        magnitude_ab = np.dot(ab, ab)

        if magnitude_ab == 0:
            return a

        t = max(0, min(magnitude_ab, np.dot(ap, ab))) / magnitude_ab
        return Coordinate(x=a.x + ab[0] * t, y=a.y + ab[1] * t, z=a.z + ab[2] * t)

    def smooth_path(self, path: List["Coordinate"]) -> List["Coordinate"]:
        """
        Smoothens the given path using an average filter.
        """
        smoothed_path = [path[0]]
        for i in range(1, len(path) - 1):
            avg_x = (path[i - 1].x + path[i].x + path[i + 1].x) / 3
            avg_y = (path[i - 1].y + path[i].y + path[i + 1].y) / 3
            avg_z = (path[i - 1].z + path[i].z + path[i + 1].z) / 3
            smoothed_path.append(Coordinate(avg_x, avg_y, avg_z))
        smoothed_path.append(path[-1])
        return smoothed_path

    def find_optimal_path(
        self, start: "Coordinate", end: "Coordinate"
    ) -> List["Coordinate"]:
        """
        Determines the optimal path between start and end points considering energy consumption.
        This is a naive approach and more complex algorithms like A* can be used.
        """
        # Note: This is a placeholder and can be far more complex in real scenarios
        straight_path = [start, end]
        return self.smooth_path(straight_path)

    def project_anomalies(self) -> List["Coordinate"]:
        """
        Projects potential future anomalies based on current anomalies and past trajectories.
        This is a simplistic projection and can be improved with more advanced models.
        """
        anomalies = self.detect_anomaly()
        projected_anomalies = []

        for idx in anomalies:
            for node_id, node_history in self.history.items():
                if idx < len(node_history) - 1:
                    delta_x = node_history[idx].x - node_history[idx - 1].x
                    delta_y = node_history[idx].y - node_history[idx - 1].y
                    delta_z = node_history[idx].z - node_history[idx - 1].z

                    projected_anomaly = Coordinate(
                        node_history[idx].x + delta_x,
                        node_history[idx].y + delta_y,
                        node_history[idx].z + delta_z,
                    )
                    projected_anomalies.append(projected_anomaly)

        return projected_anomalies

    def gravity_well_influence_zone(self, threshold: float = 0.5) -> List["Coordinate"]:
        """
        Identifies zones that have strong influence from gravity wells.
        Returns the center points of these zones.
        """
        influence_zones = []
        for well, strength in self.gravity_wells:
            # A naive approach to determine the influence based on the threshold
            radius = strength / threshold
            # Taking the center of the gravity well as the influence zone
            influence_zones.append(Coordinate(well[0], well[1], well[2], radius))
        return influence_zones

    def is_path_safe(self, path: List["Coordinate"]) -> bool:
        """
        Checks if the given path is safe considering the gravity wells and anomalies.
        """
        anomalies = self.detect_anomaly()
        influence_zones = self.gravity_well_influence_zone()

        for coord in path:
            for anomaly in anomalies:
                if (
                    math.dist(
                        [coord.x, coord.y, coord.z], [anomaly.x, anomaly.y, anomaly.z]
                    )
                    < 1.0
                ):  # Assuming 1.0 as danger distance
                    return False
            for zone in influence_zones:
                if (
                    math.dist([coord.x, coord.y, coord.z], [zone.x, zone.y, zone.z])
                    < zone.t
                ):  # zone.t is the radius
                    return False
        return True

    def move(self, delta_x=0, delta_y=0, delta_z=0, delta_t=0, target=None):
        """Simulate movement by adjusting the coordinate or moving to a target."""
        if target:
            target_coord = self._extract_coordinate(target)
            self.coordinate = target_coord
        else:
            self.coordinate.x += delta_x
            self.coordinate.y += delta_y
            self.coordinate.z += delta_z
            self.coordinate.t += delta_t

        self.history.append(
            (self.coordinate.x, self.coordinate.y, self.coordinate.z, self.coordinate.t)
        )
        self.broadcast_movement()

    def detect_collision(self, other, threshold=0.5) -> bool:
        """Detect collision or near-collision with another coordinate."""
        other_coord = self._extract_coordinate(other)
        distance = math.dist(
            (self.coordinate.x, self.coordinate.y, self.coordinate.z),
            (other_coord.x, other_coord.y, other_coord.z),
        )
        return distance <= threshold

    def nearest_neighbors(self, coordinates: list, n=5) -> list:
        """Find the n closest coordinates based on Euclidean distance."""
        distances = [
            (
                coord,
                math.dist(
                    (self.coordinate.x, self.coordinate.y, self.coordinate.z),
                    (
                        self._extract_coordinate(coord).x,
                        self._extract_coordinate(coord).y,
                        self._extract_coordinate(coord).z,
                    ),
                ),
            )
            for coord in coordinates
        ]
        distances.sort(key=lambda x: x[1])
        return distances[:n]

    def analyze_region_density(self, coordinates: list, threshold=5.0) -> dict:
        """Analyze a region's density by checking how many points are close to our current position within a threshold."""
        neighbors = [
            coord for coord in coordinates if self.detect_collision(coord, threshold)
        ]
        density = len(neighbors) / self.path_length()
        return {"density": density, "neighbors": neighbors}

    def generate_report(self):
        """Generate a comprehensive report of the node's activity."""
        report = {
            "current_position": self.coordinate,
            "traversed_path": self.get_traversed_path(),
            "path_length": self.path_length(),
            "predicted_next_move": self.predict_next_move(),
            "anomalies_detected": self.detect_anomaly(),
            "energy_consumed": self.get_energy_consumption(self.get_traversed_path()),
        }
        return report

    def heatmap(self, dimensions=3):
        """Generate a heatmap based on historical data for a specified number of dimensions."""
        heatmap = {}
        for pos in self.history:
            key = pos if dimensions == 3 else pos[:dimensions]
            heatmap[key] = heatmap.get(key, 0) + 1
        return heatmap

    def similarity_with(self, other_sequence):
        """Compare path with another using Dynamic Time Warping and provide a normalized score."""
        distance, _ = fastdtw(self.history, other_sequence, dist=math.dist)
        max_possible_distance = math.dist(
            (0, 0, 0),
            (
                max(self.history, key=lambda x: x[0])[0],
                max(self.history, key=lambda x: x[1])[1],
                max(self.history, key=lambda x: x[2])[2],
            ),
        ) * len(self.history)
        similarity_score = 1 - (distance / max_possible_distance)
        return similarity_score

    def register_gravity_well(self, position: Coordinate, strength: float):
        """
        Register a gravity well in the system.

        :param position: The coordinate where the gravity well exists.
        :param strength: Strength of the gravity well.
        """
        self.gravity_wells.append((position, strength))

    def unregister_gravity_well(self, position: Coordinate):
        """
        Remove an existing gravity well based on its position.

        :param position: The coordinate of the gravity well to be removed.
        """
        self.gravity_wells = [
            well for well in self.gravity_wells if well[0] != position
        ]

    def extract_moving_pattern(self) -> List[str]:
        """
        Analyze movement patterns based on history. For simplicity, we'll extract patterns
        of increased, decreased, or stagnant movement on all axes.

        :return: List of detected patterns.
        """
        patterns = []
        for i in range(1, len(self.history)):
            pattern = {
                "x": "increase"
                if self.history[i][0] > self.history[i - 1][0]
                else "decrease"
                if self.history[i][0] < self.history[i - 1][0]
                else "stagnant",
                "y": "increase"
                if self.history[i][1] > self.history[i - 1][1]
                else "decrease"
                if self.history[i][1] < self.history[i - 1][1]
                else "stagnant",
                "z": "increase"
                if self.history[i][2] > self.history[i - 1][2]
                else "decrease"
                if self.history[i][2] < self.history[i - 1][2]
                else "stagnant",
            }
            patterns.append(pattern)

        return patterns

    def apply_external_forces(self, forces: Dict[Coordinate, float]):
        """
        Apply external forces to adjust the coordinate. This method will adjust the
        next predicted move based on these forces.

        :param forces: Dictionary of external forces with their position and strength.
        """
        for force_position, force_strength in forces.items():
            direction = self.get_direction_factor(self.coordinate, force_position)
            self.coordinate.x += direction["x"] * force_strength
            self.coordinate.y += direction["y"] * force_strength
            self.coordinate.z += direction["z"] * force_strength
