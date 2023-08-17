from typing import List
from dl_matrix.models import Coordinate
from pydantic import BaseModel
from collections import deque
from collections import defaultdict
import math
from functools import lru_cache
from datetime import datetime


class Operations(BaseModel):
    coordinate: Coordinate
    parent: "Operations" = None
    children: List["Operations"] = []
    annotations: dict = {}
    history: list = deque(maxlen=10)  # To keep the last 10 positions.
    subscribers: list = []

    class Config:
        arbitrary_types_allowed = True

    def to_human_readable(self) -> str:
        """
        Provide a human-readable representation of the coordinate.

        Returns:
            str: A description of the coordinate.
        """
        return f"Depth: {self.coordinate.x}, Sibling Position: {self.coordinate.y}, Child Position: {self.coordinate.z}, Timestamp: {self.coordinate.t}"

    def is_deeper_than(self, other: Coordinate) -> bool:
        """
        Check if the current coordinate is deeper than another.

        Args:
            other (Coordinate): Another coordinate object.

        Returns:
            bool: True if deeper, False otherwise.
        """
        return self.coordinate.x > other.x

    def is_shallower_than(self, other: Coordinate) -> bool:
        """
        Check if the current coordinate is shallower than another.

        Args:
            other (Coordinate): Another coordinate object.

        Returns:
            bool: True if shallower, False otherwise.
        """
        return self.coordinate.x < other.x

    def is_same_depth_as(self, other: Coordinate) -> bool:
        """
        Check if the current coordinate is at the same depth as another.

        Args:
            other (Coordinate): Another coordinate object.

        Returns:
            bool: True if same depth, False otherwise.
        """
        return self.coordinate.x == other.x

    def is_before(self, other: Coordinate) -> bool:
        """
        Check if the current message/node was created before another based on timestamp.

        Args:
            other (Coordinate): Another coordinate object.

        Returns:
            bool: True if created before, False otherwise.
        """
        return self.coordinate.t < other.t

    def is_after(self, other: Coordinate) -> bool:
        """
        Check if the current message/node was created after another based on timestamp.

        Args:
            other (Coordinate): Another coordinate object.

        Returns:
            bool: True if created after, False otherwise.
        """
        return self.coordinate.t > other.t

    def is_next_sibling_of(self, other: Coordinate) -> bool:
        """
        Check if the current coordinate is the immediate next sibling of another.

        Args:
            other (Coordinate): Another coordinate object.

        Returns:
            bool: True if next sibling, False otherwise.
        """
        return self.is_same_depth_as(other) and (self.coordinate.y == other.y + 1)

    def is_previous_sibling_of(self, other: Coordinate) -> bool:
        """
        Check if the current coordinate is the immediate previous sibling of another.

        Args:
            other (Coordinate): Another coordinate object.

        Returns:
            bool: True if previous sibling, False otherwise.
        """
        return self.is_same_depth_as(other) and (self.coordinate.y == other.y - 1)

    def annotate(self, key: str, value: any):
        """Add an annotation to this coordinate."""
        self.annotations[key] = value

    def get_annotation(self, key: str):
        """Retrieve a previously added annotation."""
        return self.annotations.get(key, None)

    def query_region(self, min_depth: int, max_depth: int) -> list:
        """Return nodes that fall within a certain depth region."""
        results = []

        if min_depth <= self.coordinate.x <= max_depth:
            results.append(self)

        for child in self.children:
            results.extend(child.query_region(min_depth, max_depth))

        return results

    def is_similar_to(self, other: Coordinate) -> bool:
        """
        Compare two nodes to see if they're similar based on a set of pre-defined conditions.
        Here, we'll simply compare their depths, but this can be extended with more complex conditions.
        """
        return self.coordinate.x == other.x

    @staticmethod
    def flatten(coordinate: Coordinate) -> List[float]:
        return [coordinate.x, coordinate.y, coordinate.z, coordinate.t]

    @staticmethod
    def calculate_distance(coord1: Coordinate, coord2: Coordinate) -> float:
        """Calculate the Euclidean distance between two coordinates."""
        distance = (
            (coord1.x - coord2.x) ** 2
            + (coord1.y - coord2.y) ** 2
            + (coord1.z - coord2.z) ** 2
            + (coord1.t - coord2.t) ** 2
        ) ** 0.5
        return distance

    @staticmethod
    def merge_coordinates(coords: List[Coordinate]) -> Coordinate:
        """Merge a list of coordinates, calculating average values for each dimension."""
        avg_x = sum([coord.x for coord in coords]) / len(coords)
        avg_y = sum([coord.y for coord in coords]) / len(coords)
        avg_z = sum([coord.z for coord in coords]) / len(coords)
        avg_t = sum([coord.t for coord in coords]) / len(coords)

        return Coordinate(x=avg_x, y=avg_y, z=avg_z, t=avg_t)

    @staticmethod
    def determine_conversation_branching(
        coordinates: List[Coordinate], current_coord: Coordinate
    ) -> str:
        """
        Determine the type of branching in the conversation based on the given coordinate and the list of previous coordinates.
        """

        siblings = [coord for coord in coordinates if coord.x == current_coord.x]
        children = [coord for coord in coordinates if coord.x == current_coord.x + 1]

        # Check if there's a loopback or circular conversation pattern
        if any(coord for coord in siblings if coord.t < current_coord.t):
            return "circular"

        # Check for converging pattern
        if len(siblings) > len(children) and len(children) == 1:
            return "converging"

        # Based on depth, sibling count and overall children
        if current_coord.x == 0:
            return "linear"
        elif 0 < current_coord.y < 3 and len(children) <= 3:
            return "branching"
        elif len(children) > 3:
            return "deep_branching"

        return "unknown"

    @staticmethod
    def is_conversation_progressing(
        coord_old: Coordinate, coord_new: Coordinate
    ) -> bool:
        """
        Determine if the conversation is progressing based on comparing two coordinates in time.
        """
        return coord_new.t > coord_old.t

    @staticmethod
    def get_relative_depth(coord1: Coordinate, coord2: Coordinate) -> int:
        """
        Get the relative depth difference between two conversation nodes.
        """
        return coord1.x - coord2.x

    @staticmethod
    def is_sibling(coord1: Coordinate, coord2: Coordinate) -> bool:
        """
        Determine if two coordinates/nodes are siblings.
        """
        return coord1.x == coord2.x and abs(coord1.y - coord2.y) == 1

    @staticmethod
    def is_parent_child_relation(parent: Coordinate, child: Coordinate) -> bool:
        """
        Determine if there's a parent-child relationship between two nodes.
        """
        return parent.x == child.x - 1 and parent.y == child.y

    @staticmethod
    def conversation_temporal_gap(coord1: Coordinate, coord2: Coordinate) -> float:
        """
        Calculate the temporal gap between two messages in a conversation.
        """
        return abs(coord1.t - coord2.t)

    @staticmethod
    def assess_conversation_density(coordinates: List[Coordinate]) -> float:
        """
        Assess the density of a conversation based on how close the coordinates/nodes are.
        The lower the value, the denser (or more intense) the conversation.
        """
        if not coordinates:
            return 0

        distances = []
        for i in range(len(coordinates) - 1):
            distances.append(
                Operations.calculate_distance(coordinates[i], coordinates[i + 1])
            )
        return sum(distances) / len(distances)

    @staticmethod
    def find_critical_conversation_junctions(
        coordinates: List[Coordinate],
    ) -> List[Coordinate]:
        """
        Identify critical junctions (or decision points) in a conversation based on the branching factor.
        """
        junctions = [
            coord
            for coord in coordinates
            if Operations.determine_conversation_branching(coord) == "deep_branching"
        ]
        return junctions

    def record_change(self, change: str):
        """Record a historical change for this coordinate."""
        self.history.append({"create_time": datetime.now(), "change": change})

    def get_change_history(self) -> list:
        """Return the change history for this coordinate."""
        return self.history

    def on_reach_depth(self, target_depth: int, callback: callable):
        """
        Trigger an event when the coordinate reaches a certain depth.
        """
        if self.coordinate.x == target_depth:
            callback(self)

    def visualize_tree(self, level=0, prefix="--> ") -> str:
        """
        Enhanced tree visualization using ASCII characters.
        """
        tree_str = "|   " * (level - 1) + prefix + str(self.coordinate) + "\n"
        for child in self.children:
            tree_str += child.visualize_tree(level + 1)
        return tree_str

    def move(self, delta_x=0, delta_y=0, delta_z=0, delta_t=0):
        """Simulate movement by adjusting the coordinate."""
        self.coordinate.x += delta_x
        self.coordinate.y += delta_y
        self.coordinate.z += delta_z
        self.coordinate.t += delta_t

        self.history.append(
            (self.coordinate.x, self.coordinate.y, self.coordinate.z, self.coordinate.t)
        )
        self.broadcast_movement()

    def get_traversed_path(self):
        """Get the path traversed using historical data."""
        return list(self.history)

    def path_length(self):
        """Calculate the length of the path traversed."""
        length = 0
        for i in range(1, len(self.history)):
            length += math.dist(self.history[i], self.history[i - 1])

        return length

    def detect_collision(self, other: Coordinate) -> bool:
        """Detect collision with another coordinate. Returns True if they occupy the same position."""
        return (
            self.coordinate.x == other.x
            and self.coordinate.y == other.y
            and self.coordinate.z == other.z
        )

    def path_curvature(self):
        """Compute the curvature of the path traversed."""
        straight_distance = math.dist(self.history[0], self.history[-1])
        traversed_distance = self.path_length()
        curvature = (traversed_distance - straight_distance) / traversed_distance
        return curvature

    def subscribe(self, subscriber):
        """Allow an object to subscribe to movement events."""
        self.subscribers.append(subscriber)

    def broadcast_movement(self):
        """Notify all subscribers of a movement event."""
        for subscriber in self.subscribers:
            subscriber.notify_movement(self.coordinate)

    @lru_cache(maxsize=256)
    def tree_distance(self, other: Coordinate) -> int:
        """
        Calculate the tree distance between two nodes.

        Args:
            other (Coordinate): Another coordinate object.

        Returns:
            int: Distance in the tree structure.
        """
        if self.coordinate == other:
            return 0

        if self.is_same_depth_as(other):
            return abs(self.coordinate.y - other.y)

        # If not on the same level, navigate upwards
        distance_to_root = self.coordinate.x
        other_distance_to_root = other.x

        # Align depths
        while self.coordinate.x > other.x:
            self = self.parent
            distance_to_root -= 1

        while other.x > self.coordinate.x:
            other = other.parent
            other_distance_to_root -= 1

        # Now traverse to the common ancestor
        while self.coordinate != other:
            self = self.parent
            other = other.parent
            distance_to_root += 1
            other_distance_to_root += 1

        return distance_to_root + other_distance_to_root

    def depth_summary(self) -> dict:
        """
        Get a summary of nodes at each depth of the tree.

        Returns:
            dict: A summary of the tree depths.
        """
        summary = defaultdict(int)
        summary[self.coordinate.x] = 1
        for child in self.children:
            child_summary = child.depth_summary()
            for depth, count in child_summary.items():
                summary[depth] += count
        return dict(summary)
