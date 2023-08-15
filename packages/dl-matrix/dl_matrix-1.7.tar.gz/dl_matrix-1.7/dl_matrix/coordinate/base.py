from typing import Optional, Dict, Any, List, Tuple, Union, Callable
from pydantic import BaseModel, Field
from uuid import uuid4
import numpy as np
import networkx as nx
import torch


class Coordinate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    x: Optional[float] = Field(0, description="The depth of the coordinate.")

    y: Optional[float] = Field(0, description="The sibling of the coordinate.")

    z: Optional[float] = Field(0, description="The sibling count of the coordinate.")

    t: Optional[float] = Field(0, description="The time of the coordinate.")

    n_parts: Optional[float] = Field(
        0, description="The number of parts of the coordinate."
    )

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 0,
                "x": 0,
                "y": 0,
                "z": 0,
                "t": 0,
                "n_parts": 0,
            }
        }

    @staticmethod
    def unflatten(values: np.ndarray):
        return Coordinate(
            x=values[0],
            y=values[1],
            z=values[2],
            t=values[3],
            n_parts=values[4],
        )

    @staticmethod
    def flatten_list(coordinates: List["Coordinate"]):
        return np.array([Coordinate.flatten(c) for c in coordinates])

    @staticmethod
    def get_coordinate_names():
        return [
            "depth_x",
            "sibling_y",
            "sibling_count_z",
            "time_t",
            "n_parts",
        ]

    @classmethod
    def create(
        cls,
        depth_args: list = [],
        sibling_args: list = [],
        sibling_count_args: list = [],
        time_args: list = [],
        n_parts_args: list = [],
    ):
        return cls(
            x=depth_args[0] if len(depth_args) > 0 else 0,
            y=sibling_args[0] if len(sibling_args) > 0 else 0,
            z=sibling_count_args[0] if len(sibling_count_args) > 0 else 0,
            t=time_args[0] if len(time_args) > 0 else 0,
            n_parts=n_parts_args[0] if len(n_parts_args) > 0 else 0,
        )

    @staticmethod
    def flatten(coordinate: "Coordinate"):
        values = [
            coordinate.x,
            coordinate.y,
            coordinate.z,
            coordinate.t,
            coordinate.n_parts,
        ]
        return np.array(values)

    def tuple(self) -> tuple:
        return tuple(self.dict().values())

    @staticmethod
    def flatten_list(coordinates: List["Coordinate"]):
        return np.array([Coordinate.flatten(c) for c in coordinates])

    @staticmethod
    def unflatten_list(values: np.ndarray):
        return [Coordinate.unflatten(v) for v in values]

    @staticmethod
    def flatten_list_of_lists(coordinates: List[List["Coordinate"]]):
        return np.array([[Coordinate.flatten(c) for c in cs] for cs in coordinates])

    @staticmethod
    def unflatten_list_of_lists(values: np.ndarray):
        return [[Coordinate.unflatten(v) for v in vs] for vs in values]

    @staticmethod
    def coordinate_to_string(coordinate: "Coordinate") -> str:
        """
        Convert a Coordinate object into a string.

        Args:
            coordinate: The Coordinate object.

        Returns:
            A string representing the Coordinate object.
        """
        flattened_coordinate = Coordinate.flatten(coordinate)

        # Convert the flattened coordinate to a string
        str_coordinate = np.array2string(flattened_coordinate, separator=",")

        return str_coordinate

    @staticmethod
    def string_to_coordinate(coordinate_str: str) -> "Coordinate":
        """
        Convert a string into a Coordinate object.

        Args:
            coordinate_str: The string representation of the Coordinate object.

        Returns:
            A Coordinate object.
        """
        # Convert string to numpy array
        coordinate_arr = np.fromstring(coordinate_str, sep=",")

        # Unflatten the array to get the coordinate values
        coordinate_values = Coordinate.unflatten(coordinate_arr)

        # Create coordinate object
        coordinate = Coordinate.create(*coordinate_values)

        return coordinate

    @classmethod
    def from_tuple(clx, data: Dict[str, Any]) -> "Coordinate":
        """
        Create a Coordinate object from a tuple.

        Args:
            data: The tuple containing the coordinate values.

        Returns:
            A Coordinate object.
        """
        return Coordinate.create(*data)

    def to_tuple(self) -> Tuple:
        """
        Convert the Coordinate object into a tuple.

        Returns:
            A tuple containing the coordinate values.
        """
        return self.tuple()

    @staticmethod
    def stack_coordinates(
        coordinates_dict: Dict[str, Union["Coordinate", np.array]]
    ) -> np.array:
        """
        Extract the flattened Coordinate arrays from the dictionary and stack them into a 2D array.

        Args:
            coordinates_dict: The dictionary of Coordinate objects or flattened Coordinate arrays.

        Returns:
            A 2D numpy array containing the flattened representations of the Coordinate objects or arrays in the dictionary.
        """
        return np.stack(list(coordinates_dict.values()), axis=0)

    @staticmethod
    def to_tensor(
        coordinates_dict: Dict[str, Union["Coordinate", np.array]]
    ) -> torch.Tensor:
        """
        Converts a dictionary of Coordinate objects or flattened Coordinate arrays into a PyTorch tensor.

        Args:
            coordinates_dict: The dictionary of Coordinate objects or flattened Coordinate arrays.

        Returns:
            A PyTorch tensor representation of the Coordinate objects or their flattened representations in the dictionary.
        """
        # Use the helper method to stack the Coordinate arrays into a 2D array.
        coordinates_array = Coordinate.stack_coordinates(coordinates_dict)

        # Convert the 2D array to a PyTorch tensor.
        coordinates_tensor = torch.tensor(coordinates_array, dtype=torch.float32)

        return coordinates_tensor

    @staticmethod
    def from_tensor(coordinates_tensor: torch.Tensor) -> Dict[str, "Coordinate"]:
        """
        Converts a PyTorch tensor into a dictionary of Coordinate objects.

        Args:
            coordinates_tensor: The PyTorch tensor to convert.

        Returns:
            A dictionary of Coordinate objects.
        """
        # Convert the PyTorch tensor to a numpy array.
        coordinates_array = coordinates_tensor.numpy()

        # Convert the numpy array to a dictionary of Coordinate objects.
        coordinates_dict = Coordinate.from_array(coordinates_array)

        return coordinates_dict

    @staticmethod
    def from_array(coordinates_array: np.array) -> Dict[str, "Coordinate"]:
        """
        Converts a numpy array into a dictionary of Coordinate objects.

        Args:
            coordinates_array: The numpy array to convert.

        Returns:
            A dictionary of Coordinate objects.
        """
        # Convert the numpy array to a list of Coordinate objects.
        coordinates_list = Coordinate.from_list(coordinates_array)

        # Convert the list of Coordinate objects to a dictionary.
        coordinates_dict = Coordinate.from_list(coordinates_list)

        return coordinates_dict

    @staticmethod
    def from_list(coordinates_list: List["Coordinate"]) -> Dict[str, "Coordinate"]:
        """
        Converts a list of Coordinate objects into a dictionary.

        Args:
            coordinates_list: The list of Coordinate objects.

        Returns:
            A dictionary where the keys are the IDs of the Coordinate objects and the values are the Coordinate objects.
        """
        return {coordinate.id: coordinate for coordinate in coordinates_list}

    @staticmethod
    def tree_flatten(
        coordinates_dict: Dict[str, "Coordinate"]
    ) -> Tuple[List[np.ndarray], List[Tuple[Any, ...]]]:
        """
        Flattens a dictionary of Coordinate objects.

        Args:
            coordinates_dict: The dictionary of Coordinate objects.

        Returns:
            A tuple containing a list of flattened Coordinate numpy arrays and a list of auxiliary data needed for unflattening.
        """
        # Get the list of Coordinate objects from the dictionary.
        coordinates_list = list(coordinates_dict.values())

        # Flatten the Coordinate objects.
        flattened_coordinates_list = [
            Coordinate.flatten(coord) for coord in coordinates_list
        ]

        # The auxiliary data needed for unflattening is the keys of the original dictionary.
        aux_data = list(coordinates_dict.keys())

        return flattened_coordinates_list, aux_data

    @staticmethod
    def tree_unflatten(
        flattened_coordinates_list: List[np.ndarray], aux_data: List[Any]
    ) -> Dict[str, "Coordinate"]:
        """
        Unflattens a list of flattened Coordinate numpy arrays.

        Args:
            flattened_coordinates_list: The list of flattened Coordinate numpy arrays.
            aux_data: The auxiliary data needed for unflattening (keys of the original dictionary).

        Returns:
            A dictionary of Coordinate objects.
        """
        # Unflatten the Coordinate numpy arrays.
        coordinates_list = [
            Coordinate.unflatten(coord) for coord in flattened_coordinates_list
        ]

        # Convert the list of Coordinate objects to a dictionary.
        coordinates_dict = dict(zip(aux_data, coordinates_list))

        return coordinates_dict

    @staticmethod
    def create_tree(
        root: str, connections: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """
        Creates a tree structure.

        Args:
            root (str): The root node.
            connections (Dict[str, List[str]]): Dictionary representing the connections between nodes.

        Returns:
            Dict[str, List[str]]: A tree structure.
        """
        tree = {root: []}

        for parent, children in connections.items():
            tree[parent] = children
            for child in children:
                if child not in tree:
                    tree[child] = []

        return tree

    @staticmethod
    def list_to_dict(
        coordinates: List["Coordinate"], flatten: bool = False
    ) -> Dict[str, Union["Coordinate", np.array]]:
        """
        Convert a list of Coordinate objects into a dictionary.

        Args:
            coordinates: The list of Coordinate objects.
            flatten: A flag to determine if the Coordinate objects should be flattened.

        Returns:
            A dictionary where the keys are the IDs of the Coordinate objects and the values are the Coordinate objects
            or their flattened representations.
        """
        if flatten:
            return {
                coordinate.id: Coordinate.flatten(coordinate)
                for coordinate in coordinates
            }
        else:
            return {coordinate.id: coordinate for coordinate in coordinates}

    @staticmethod
    def create_graph(
        root: str,
        connections: Dict[str, List[str]],
        coordinates: List["Coordinate"],
        edges: Optional[List[Tuple[str, str, float]]] = None,
        labels: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        depth: Optional[Dict[str, Any]] = None,
        siblings: Optional[Dict[str, Any]] = None,
    ) -> nx.Graph:
        """
        Creates a NetworkX graph.

        Args:
            root (str): The root node.
            connections (Dict[str, List[str]]): Dictionary representing the connections between nodes.
            coordinates: The list of Coordinate objects.
            edges: A list of edges between the coordinates. Each edge is represented as a tuple (node1, node2, weight).
            labels: A dictionary with node labels.
            metadata: A dictionary with additional metadata for each node.
            depth: A dictionary with depth information for each node.
            siblings: A dictionary with siblings information for each node.

        Returns:
            A NetworkX graph.
        """
        # Create tree
        tree = Coordinate.create_tree(root, connections)

        graph = Coordinate.flatten_coordinates_to_graph(
            coordinates, edges, labels, metadata, depth, siblings
        )
        return graph, tree

    @classmethod
    def flatten_coordinates_to_graph(
        cls,
        coordinates: List["Coordinate"],
        edges: Optional[List[Tuple[str, str, float]]] = None,
        labels: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        depth: Optional[Dict[str, Any]] = None,
        siblings: Optional[Dict[str, Any]] = None,
    ) -> nx.Graph:
        """
        Flatten a list of coordinates and adds each as a node to a NetworkX graph.
        Adds edges, labels, metadata, depth and siblings information between the nodes in the graph.

        Args:
            coordinates: A list of coordinates.
            edges: A list of edges between the coordinates. Each edge is represented as a tuple (node1, node2, weight).
            labels: A dictionary with node labels.
            metadata: A dictionary with additional metadata for each node.
            depth: A dictionary with depth information for each node.
            siblings: A dictionary with siblings information for each node.

        Returns:
            A NetworkX graph with the flattened coordinates as nodes and edges, labels, metadata, depth and siblings information between the nodes.
        """
        # Create graph
        graph = nx.Graph()

        # Add nodes from the flattened coordinates
        for coordinate in coordinates:
            graph.add_node(coordinate.id, coordinate=coordinate)

        # Add edges
        if edges:
            graph.add_weighted_edges_from(edges)

        # Add labels
        if labels:
            nx.set_node_attributes(graph, labels, "label")

        # Add metadata
        if metadata:
            nx.set_node_attributes(graph, metadata, "metadata")

        # Add depth
        if depth:
            nx.set_node_attributes(graph, depth, "depth")

        # Add siblings
        if siblings:
            nx.set_node_attributes(graph, siblings, "siblings")

        return graph

    @staticmethod
    def get_coordinates_from_graph(
        graph: nx.Graph, flatten: bool = False
    ) -> Dict[str, Union["Coordinate", np.array]]:
        """
        Extracts the coordinates from a NetworkX graph.

        Args:
            graph: The NetworkX graph.
            flatten: A flag to determine if the Coordinate objects should be flattened.

        Returns:
            A dictionary where the keys are the IDs of the Coordinate objects and the values are the Coordinate objects
            or their flattened representations.
        """
        coordinates = nx.get_node_attributes(graph, "coordinate")

        if flatten:
            return {
                coordinate.id: Coordinate.flatten(coordinate)
                for coordinate in coordinates.values()
            }
        else:
            return coordinates

    @staticmethod
    def get_edges_from_graph(graph: nx.Graph) -> List[Tuple[str, str, float]]:
        """
        Extracts the edges from a NetworkX graph.

        Args:
            graph: The NetworkX graph.

        Returns:
            A list of edges between the coordinates. Each edge is represented as a tuple (node1, node2, weight).
        """
        return list(graph.edges.data("weight"))

    @classmethod
    def build_from_dict(
        cls,
        coordinates_dict: Dict[str, Union["Coordinate", np.array]],
        flatten: bool = False,
    ) -> List["Coordinate"]:
        """
        Builds a list of Coordinate objects from a dictionary.

        Args:
            coordinates_dict: A dictionary where the keys are the IDs of the Coordinate objects and the values are the
            Coordinate objects or their flattened representations.
            flatten: A flag to determine if the Coordinate objects should be flattened.

        Returns:
            A list of Coordinate objects.
        """
        if flatten:
            return [Coordinate.unflatten(coord) for coord in coordinates_dict.values()]
        else:
            return list(coordinates_dict.values())

    @classmethod
    def build_from_matrix(
        cls, matrix: np.array, flatten: bool = False
    ) -> List["Coordinate"]:
        """
        Builds a list of Coordinate objects from a matrix.

        Args:
            matrix: A matrix where each row represents a Coordinate object or its flattened representation.
            flatten: A flag to determine if the Coordinate objects should be flattened.

        Returns:
            A list of Coordinate objects.
        """
        coordinates = []
        for row in matrix:
            if flatten:
                coordinates.append(Coordinate.unflatten(row))
            else:
                coordinates.append(Coordinate(row))
        return coordinates
