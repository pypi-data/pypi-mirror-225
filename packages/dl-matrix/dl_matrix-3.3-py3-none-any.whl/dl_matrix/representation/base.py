from typing import Any, Dict, List, Optional, Tuple, Union, Callable
import networkx as nx
from dl_matrix.transformation import Coordinate
from dl_matrix.models import ChainTreeIndex, Message, Content
from dl_matrix.relationship import Relationship
from dl_matrix.type import NodeRelationship
import numpy as np
import logging


class Representation(Relationship):
    RELATIONSHIP_WEIGHTS = {
        "siblings": 1,
        "cousins": 2,
        "uncles_aunts": 3,
        "nephews_nieces": 3,
        "grandparents": 4,
        "ancestors": 5,
        "descendants": 5,
        NodeRelationship.PARENT: 1,
        NodeRelationship.CHILD: 1,
        NodeRelationship.PREVIOUS: 1,
        NodeRelationship.NEXT: 1,
        NodeRelationship.SOURCE: 1,
    }

    def __init__(
        self,
        conversation_tree: ChainTreeIndex,
        message_dict: Dict[str, Message] = None,
        tetra_dict: Dict[str, Tuple[float, float, float, float]] = None,
        root_component_values: Dict[str, Any] = None,
    ):
        self.conversation = conversation_tree
        self.mapping = conversation_tree.conversation.mapping
        self.message_dict = message_dict
        self.tetra_dict = tetra_dict
        self.conversation_dict = self._conversation_representation()
        self.relationships = {}
        self.default_root_component_values = {
            "depth_args": [0],
            "sibling_args": [0],
            "sibling_count_args": [0],
            "time_args": [0],
        }

        # If root component values are provided, update the default ones
        if root_component_values:
            self.default_root_component_values.update(root_component_values)

        # Construct root coordinate with updated component values
        self.root_coordinate = Coordinate.create(**self.default_root_component_values)

    @property
    def depth(self) -> int:
        """
        Returns the maximum depth of the conversation tree.

        Returns:
            depth: The maximum depth of the conversation tree.
        """
        return self.get_message_depth(self.root_message_id)

    @property
    def root_message_id(self) -> Union[Message, None]:
        """Returns the root message of the conversation, or None if it doesn't exist."""
        for message in self.mapping.values():
            if message.parent is None:
                return self.message_dict[message.id].id if self.message_dict else None
        return None

    def _create_graph(self) -> nx.Graph:
        """
        Creates a networkx Graph representation of the conversation tree.
        """
        G = nx.Graph()
        for node in self.mapping.values():
            G.add_node(node.id, message=node.message)
            if node.parent:
                G.add_edge(node.parent, node.id)

        return G

    def _create_representation(self) -> nx.DiGraph:
        """
        Creates a NetworkX directed graph representation of the conversation tree.
        Each node in the graph is a message, and each edge indicates a response
        relationship between messages. Nodes are annotated with message content
        and authors, and edges are annotated with the response time between
        messages.
        """
        graph = nx.DiGraph()
        prev_node = None

        for mapping_id, mapping in self.mapping.items():
            if mapping.message is None:
                raise ValueError(f"Mapping {mapping_id} does not contain a message")

            # Add the node to the graph
            graph.add_node(mapping_id, **mapping.message.dict())

            # If this isn't the first node, create an edge from the previous node
            if prev_node is not None:
                graph.add_edge(prev_node, mapping_id)

            # If the mapping has a parent, create an edge from the parent
            if mapping.parent is not None:
                graph.add_edge(mapping.parent, mapping_id)

            # Add edges to all references
            for ref_id in mapping.references:
                if ref_id in self.mapping:
                    graph.add_edge(mapping_id, ref_id)

            # Update the previous node
            prev_node = mapping_id

        return graph

    def create_representation(
        self,
        node_ids: Optional[List[str]] = None,
        attribute_filter: Optional[Dict[str, Any]] = None,
    ) -> nx.DiGraph:
        """
        Creates a NetworkX directed graph representation of the conversation tree.
        Each node in the graph is a message, and each edge indicates a response
        relationship between messages. Nodes are annotated with message content
        and authors, and edges are annotated with the response time between
        messages.

        Args:
            node_ids: A list of node IDs to include in the graph.
            attribute_filter: A dictionary of attributes to filter nodes by.

        Returns:
            A NetworkX directed graph representation of the conversation tree.

        """
        # Get the full graph representation
        graph = self._create_representation()

        # If node_ids are provided, use them to create the subgraph
        if node_ids is not None:
            subgraph = graph.subgraph(node_ids)

        # If attribute_filter is provided, select nodes based on attributes
        elif attribute_filter is not None:
            selected_nodes = [
                node
                for node, data in graph.nodes(data=True)
                if all(item in data.items() for item in attribute_filter.items())
            ]
            subgraph = graph.subgraph(selected_nodes)
        # If neither are provided, return the full graph
        else:
            subgraph = graph

        return subgraph

    def initialize_representation(
        self,
        use_graph: bool = False,
        node_ids: Optional[List[str]] = None,
        attribute_filter: Optional[Dict[str, Any]] = None,
        RELATIONSHIP_TYPE=NodeRelationship,
    ) -> Tuple[str, Callable]:
        """
        This method initializes the graph for the conversation. It either creates the conversation graph or uses the provided graph.

        :param use_graph: A boolean indicating whether to create a new conversation graph or use the existing one.
        :return: The root ID of the graph as a string, and a function to get the children IDs for a given node.
        """
        relationships = {}

        if use_graph:
            # Create the conversation graph
            G = self.create_representation(
                node_ids=node_ids, attribute_filter=attribute_filter
            )
            if G.number_of_nodes() == 0:
                return "", None

            # Get the root node
            root_id = list(nx.topological_sort(G))[0]

            # Get the children IDs for a given node
            get_children_ids = lambda node_id: list(G.successors(node_id))

            # Get the tetra dict
            relationships[root_id] = {RELATIONSHIP_TYPE.SOURCE: root_id}

        else:
            if len(self.conversation_dict) == 0:
                return "", None

            root_id = list(self.conversation_dict)[0]
            get_children_ids = self.get_children_ids
            relationships[root_id] = {RELATIONSHIP_TYPE.SOURCE: root_id}

        tetra_dict = {}
        tetra_dict[root_id] = self.root_coordinate.flatten(self.root_coordinate)

        return (
            relationships,
            get_children_ids,
            tetra_dict,
            root_id,
            self.root_coordinate,
        )

    def _sibling_graph(self, children_ids: List[str]) -> nx.Graph:
        """
        Creates a graph from the sibling relationships of a given message.
        """
        G = nx.Graph()
        G.add_nodes_from(children_ids)
        for child_id in children_ids:
            siblings = self._get_message_siblings(child_id)
            for sibling in siblings:
                G.add_edge(child_id, sibling.id)
        return G

    def get_message_attribute(self, message_id: str, *attributes: str):
        """
        Get a specific attribute of a message given its id.

        Args:
            message_id: The id of the message.
            attributes: The sequence of attributes to fetch (e.g., "content", "text").

        Returns:
            The desired attribute of the message.
        """
        try:
            value = self.message_dict[message_id].message
            for attribute in attributes:
                if hasattr(value, attribute):
                    value = getattr(value, attribute)
                else:
                    raise AttributeError(f"Attribute {attribute} not found in message.")
            return value
        except KeyError:
            raise ValueError(f"Message with id {message_id} not found.")

    def _assign_relationships(
        self,
        message_id: str,
        child_id: str,
        children_ids: List[str],
        i: int,
        relationships: Dict[str, Dict[str, str]],
        RELATIONSHIP_TYPE=NodeRelationship,
    ) -> Dict[str, Dict[str, str]]:
        child_relationships = {
            RELATIONSHIP_TYPE.PARENT: message_id,
            RELATIONSHIP_TYPE.CHILD: [],
            RELATIONSHIP_TYPE.PREVIOUS: children_ids[i - 1] if i > 0 else None,
            RELATIONSHIP_TYPE.NEXT: children_ids[i + 1]
            if (i >= 0 and i < len(children_ids) - 1)
            else None,
        }

        extended_relationships = self.get_relationship_ids(child_id)

        # Merge the two dictionaries together
        relationships[child_id] = {**child_relationships, **extended_relationships}

        return relationships

    def _get_message_attributes(self, child_id):
        author = self.get_message_attribute(child_id, "author")
        text = self.get_message_attribute(child_id, "content", "text")
        return author, text

    def _calculate_coordinates(self, i, children_ids, depth, mapping):
        x_coord = depth
        y_coord = i + 1
        z_coord = 0 if len(children_ids) == 1 else -0.5 * (len(children_ids) - 1)
        t_coord = mapping.message.create_time
        n_parts = len(mapping.message.content.text.split("\n\n"))
        return x_coord, y_coord, z_coord, t_coord, n_parts

    def _calculate_part_weight(self, n_parts):
        return round(1.0 / n_parts, 2) if n_parts > 0 else 0

    def _get_mapping(self, child_id):
        mapping = self.message_dict[child_id]
        if not mapping:
            raise ValueError(f"Message {child_id} not found in message_dict")
        return mapping

    def _assign_coordinates(
        self, child_id, i, children_ids, depth, create_children=False
    ):
        mapping = self._get_mapping(child_id)

        x_coord, y_coord, z_coord, create_time, n_parts = self._calculate_coordinates(
            i, children_ids, depth, mapping
        )

        part_weight = self._calculate_part_weight(n_parts)
        author, text = self._get_message_attributes(child_id)
        content_parts = self.split_content_into_parts(text, n_parts)

        child_messages = []
        if create_children:
            child_messages = self._create_child_nodes(
                child_id,
                x_coord,
                y_coord,
                z_coord,
                create_time,
                author,
                part_weight,
                content_parts,
            )

        # Update the original message, if necessary
        mapping.message.children = child_messages

        child_coordinate = Coordinate(
            x=x_coord,
            y=y_coord,
            z=z_coord,
            t=create_time,
            n_parts=n_parts,
        )

        flattened_coordinate = child_coordinate.flatten(child_coordinate)

        return flattened_coordinate

    def _create_child_nodes(
        self,
        child_id,
        x_coord,
        y_coord,
        z_coord,
        create_time,
        author,
        part_weight,
        content_parts,
    ):
        """Encapsulated method to create child nodes for a given message."""
        child_messages = []
        prev_child_id = None

        for index, part in enumerate(content_parts):
            children_coordinate = Coordinate(
                x=x_coord,
                y=y_coord,
                z=z_coord,
                t=create_time,
                n_parts=index,
            )
            new_child_id = (
                f"{child_id}_{index}"  # Create a unique ID for the child message
            )
            child_message = self.create_child_message(
                new_child_id,
                part,
                create_time,
                author,
                part_weight,
                children_coordinate,
            )

            # Add relationship to the previous child message
            if prev_child_id:
                self.add_relationship(
                    prev_child_id, new_child_id, NodeRelationship.NEXT
                )
                self.add_relationship(
                    new_child_id, prev_child_id, NodeRelationship.PREVIOUS
                )

            # Add relationship to the parent message
            self.add_relationship(child_id, new_child_id, NodeRelationship.PARENT)
            self.add_relationship(new_child_id, child_id, NodeRelationship.CHILD)

            child_messages.append(child_message)
            prev_child_id = new_child_id

        return child_messages

    def create_child_message(
        self,
        message_id: str,
        content_part: str,
        create_time: float,
        author: str,
        weight,
        coordinate: Coordinate,
    ):
        # Create a new message object for the content part
        child_message = Message(
            id=message_id,
            author=author,
            create_time=create_time,
            content=Content(parts=[content_part]),
            weight=weight,
            coordinate=coordinate,
        )
        return child_message

    def add_relationship(
        self, from_id: str, to_id: str, relationship: NodeRelationship
    ):
        """
        Add a relationship between two message IDs.
        """
        if from_id not in self.relationships:
            self.relationships[from_id] = {}

        self.relationships[from_id][to_id] = relationship
