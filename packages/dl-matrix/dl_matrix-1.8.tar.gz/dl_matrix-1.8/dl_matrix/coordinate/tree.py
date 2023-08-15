from typing import List, Dict, Any, Optional, Callable, Tuple, Union
from dl_matrix.coordinate.base import Coordinate
from pydantic import BaseModel, Field
from uuid import uuid4
import numpy as np


class CoordinateTree(BaseModel):
    coordinate_node: Union[Coordinate, Dict[str, np.ndarray]]

    children: List["CoordinateTree"] = []

    tree_structure: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="The tree structure representing the messages.",
    )

    coordinates: Dict[str, Coordinate] = Field(
        default_factory=dict, description="The coordinates representing each message."
    )

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    def _get_value(self, field: str) -> float:
        """Utility to get the correct value from coordinate, be it a Coordinate object or np.ndarray"""
        if isinstance(self.coordinate_node, Coordinate):
            return getattr(self.coordinate_node, field, 0)
        else:
            indices = {
                "x": 0,
                "y": 1,
                "z": 2,
                "t": 3,
                "n_parts": 4,
            }
            return self.coordinate_node.get(indices.get(field, 0), 0)

    def __iter__(self):
        yield self
        for child in self.children:
            yield from child

    def __len__(self):
        return sum(1 for _ in self)

    def __getitem__(self, index):
        return list(self)[index]

    def __str__(self):
        return str(self.coordinate_node)

    def add_child(self, parent_id: str, child_node: Union[Coordinate, np.ndarray]):
        if parent_id not in self.coordinates:
            raise ValueError(f"No parent coordinate with id: {parent_id}")

        child_id = str(uuid4())
        self.tree_structure.setdefault(parent_id, []).append(child_id)

        if isinstance(child_node, Coordinate):
            self.coordinates[child_id] = child_node
        else:
            self.coordinates[child_id] = Coordinate.unflatten(child_node)

        self.children.append(CoordinateTree(node=child_node))

    def remove_node(self, node_id: str):
        if node_id not in self.coordinates:
            raise ValueError(f"No node with id: {node_id}")

        del self.coordinates[node_id]
        for children in self.tree_structure.values():
            if node_id in children:
                children.remove(node_id)

    def delete_branch(self, branch_id: str):
        if branch_id not in self.tree_structure:
            raise ValueError(f"No branch with id: {branch_id}")

        children = self.tree_structure[branch_id]
        for child_id in children:
            self.delete_branch(child_id)

        self.remove_node(branch_id)
        del self.tree_structure[branch_id]

    def classify_by_depth(self) -> Dict[float, List["CoordinateTree"]]:
        """Classify the nodes by their depth."""
        nodes_by_depth = {}
        for node in self:
            depth = node._get_value("x")
            if depth not in nodes_by_depth:
                nodes_by_depth[depth] = []
            nodes_by_depth[depth].append(node)
        return nodes_by_depth

    def compute_sibling_sequences(
        self, nodes: List["CoordinateTree"]
    ) -> List[List["CoordinateTree"]]:
        """Compute sequences of uninterrupted siblings."""
        nodes.sort(key=lambda node: node._get_value("y"))
        sequences = [[nodes[0]]]
        for i in range(1, len(nodes)):
            if nodes[i]._get_value("y") == nodes[i - 1]._get_value("y") + 1:
                sequences[-1].append(nodes[i])
            else:
                sequences.append([nodes[i]])
        return sequences

    def check_homogeneity(
        self, sequence: List["CoordinateTree"]
    ) -> List[List["CoordinateTree"]]:
        """Check homogeneity within a sequence."""
        homogeneous_groups = [[sequence[0]]]
        for i in range(1, len(sequence)):
            if sequence[i]._get_value("z") == sequence[i - 1]._get_value("z"):
                homogeneous_groups[-1].append(sequence[i])
            else:
                homogeneous_groups.append([sequence[i]])
        return homogeneous_groups

    def compute_group_sizes(self) -> Dict[float, int]:
        """Compute the size of each homogeneous group in the tree."""

        # Create a dictionary to keep track of counts
        group_sizes = {}

        # Iterate through the entire tree
        for node in self:
            z_value = node._get_value("z")

            # Increment the count for the z_value or initialize if not present
            group_sizes[z_value] = group_sizes.get(z_value, 0) + 1

        return group_sizes

    def get_group_sizes(
        self, groups: List[List["CoordinateTree"]]
    ) -> List[Tuple[int, List["CoordinateTree"]]]:
        """Compute the sizes of the groups."""
        return [(len(group), group) for group in groups]

    def find_maximus_triangle(self) -> List["CoordinateTree"]:
        """Find the Maximus Triangle."""
        nodes_by_depth = self.classify_by_depth()
        maximus_triangle = []
        max_size = 0
        for nodes in nodes_by_depth.values():
            sequences = self.compute_sibling_sequences(nodes)
            for sequence in sequences:
                homogeneous_groups = self.check_homogeneity(sequence)
                for group in homogeneous_groups:
                    group_sizes = self.get_group_sizes(group)
                    for size, group in group_sizes:
                        if size > max_size:
                            max_size = size
                            maximus_triangle = group
        return maximus_triangle

    @classmethod
    def build_from_dict(cls, d: Dict[str, Any]) -> "CoordinateTree":
        return cls(
            coordinate=Coordinate.build_from_dict(d["coordinate"]),
            children=[cls.build_from_dict(child) for child in d["children"]],
        )

    @classmethod
    def build_from_list(cls, l: List[Dict[str, Any]]) -> "CoordinateTree":
        return cls(
            coordinate=Coordinate.build_from_dict(l[0]["coordinate"]),
            children=[cls.build_from_dict(child) for child in l[0]["children"]],
        )

    @classmethod
    def build_from_matrix(cls, matrix: np.ndarray) -> "CoordinateTree":
        return cls(
            coordinate=Coordinate.build_from_matrix(matrix),
            children=[cls.build_from_matrix(child) for child in matrix[0]["children"]],
        )

    @staticmethod
    def depth_first_search(
        tree: "CoordinateTree", predicate: Callable[[Coordinate], bool]
    ) -> Optional[Coordinate]:
        if predicate(tree.coordinate_node):
            return tree.coordinate_node
        else:
            for child in tree.children:
                result = CoordinateTree.depth_first_search(child, predicate)
                if result is not None:
                    return result
            return None

    @staticmethod
    def breadth_first_search(
        tree: "CoordinateTree", predicate: Callable[[Coordinate], bool]
    ) -> Optional[Coordinate]:
        queue = [tree]
        while queue:
            node = queue.pop(0)
            if predicate(node.coordinate_node):
                return node.coordinate_node
            else:
                queue.extend(node.children)
        return None

    @staticmethod
    def depth_first_search_all(
        tree: "CoordinateTree", predicate: Callable[[Coordinate], bool]
    ) -> List[Coordinate]:
        results = []
        if predicate(tree.coordinate_node):
            results.append(tree.coordinate_node)
        for child in tree.children:
            results.extend(CoordinateTree.depth_first_search_all(child, predicate))
        return results


class CoordinateTreeTraverser:
    def __init__(self, tree: CoordinateTree):
        self.tree = tree

    def traverse_depth_first(
        self, predicate: Callable[[Coordinate], bool]
    ) -> Coordinate:
        return CoordinateTree.depth_first_search(self.tree, predicate)

    def traverse_breadth_first(
        self, predicate: Callable[[Coordinate], bool]
    ) -> Coordinate:
        return CoordinateTree.breadth_first_search(self.tree, predicate)

    def traverse_depth_first_all(
        self, predicate: Callable[[Coordinate], bool]
    ) -> List[Coordinate]:
        return CoordinateTree.depth_first_search_all(self.tree, predicate)
