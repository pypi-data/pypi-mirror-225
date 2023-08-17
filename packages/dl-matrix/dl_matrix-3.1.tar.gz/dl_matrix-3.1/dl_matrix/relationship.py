from typing import Dict, Any, Union, List
from dl_matrix.models import ChainMap
import networkx as nx
import collections


class Relationship:
    """
    Abstract class for representing relationships between messages.
    """

    RELATIONSHIP_TYPES = {
        "siblings": "_get_message_siblings",
        "cousins": "_get_message_cousins",
        "uncles_aunts": "uncles_aunts",
        "nephews_nieces": "nephews_nieces",
        "grandparents": "grandparents",
        "ancestors": "_get_message_ancestors",
        "descendants": "_get_message_descendants",
    }

    def __init__(self, mapping: Dict[str, ChainMap]):
        """
        Initializes the MessageGraph.

        Args:
            mapping: A dictionary mapping message IDs to their corresponding Mapping objects.
        """

        self.mapping = mapping
        self.message_dict = self._message_representation()
        self.conversation_dict = self._conversation_representation()
        self.relationship_dict = self._create_relationship_dict()

    def split_content_into_parts(self, content, n_parts):
        """
        Split the content of a message into parts.

        Args:
            content: The content of the message.
            n_parts: The number of parts to split the content into.

        Returns:
            A list of content parts.
        """
        # Split the content of the message into parts
        content_parts = content.split("\n\n")
        if len(content_parts) < n_parts:
            content_parts = content.split("\n")
        return content_parts

    def get_message_content(self, message_id: str) -> str:
        """
        Get the content of a message with a given id.

        Args:
            message_id: The id of the message.

        Returns:
            The content of the message.
        """
        return self.message_dict[message_id].message.content.text

    def get_message_author_role(self, message_id: str) -> str:
        """
        Get the author role of a message with a given id.

        Args:
            message_id: The id of the message.

        Returns:
            The author role of the message.
        """
        return self.message_dict[message_id].message.author.role

    def get_message_create_time(self, message_id: str) -> str:
        """
        Get the creation time of a message with a given id.

        Args:
            message_id: The id of the message.

        Returns:
            The creation time of the message.
        """
        return self.message_dict[message_id].message.create_time

    def _get_message_tree(self) -> nx.DiGraph:
        """
        Creates a networkx DiGraph representation of the conversation tree.

        Returns:
            A networkx DiGraph representation of the conversation tree.
        """
        tree = nx.DiGraph()
        for message_id, (parent_id, children_ids) in self.conversation_dict.items():
            tree.add_node(message_id, weight=self.message_dict[message_id])
            if parent_id is not None:
                tree.add_edge(parent_id, message_id)
        return tree

    @property
    def graph(self):
        if self._message_tree is None:
            self._message_tree = self._get_message_tree()
        return self._message_tree

    def graph(self) -> nx.DiGraph:
        """Returns the tree of messages as a networkx DiGraph"""
        tree = nx.DiGraph()
        for message_id, (parent_id, children_ids) in self.conversation_dict.items():
            tree.add_node(message_id, weight=self.message_dict[message_id])
            if parent_id is not None:
                tree.add_edge(parent_id, message_id)
        return tree

    def _message_representation(self) -> Dict[str, Dict[str, Any]]:
        """
        Creates a dictionary representation of the conversation tree.
        The keys are the message IDs and the values are the corresponding Message of the form:

        Returns:
            A dictionary representation of the conversation tree.
        """
        message_dict = {}
        for message in self.mapping.values():
            message_dict[message.id] = message
        return message_dict

    def _conversation_representation(self) -> Dict[str, List[Any]]:
        """
        Creates a dictionary representation of the conversation tree.

        The keys are the message IDs and the values are a list of the form [parent, children].
        The parent is the ID of the parent message, or None if the message is the root.
        The children is a list of the IDs of the children messages, or an empty list if the message has no children.

        Returns:
            A dictionary representation of the conversation tree.
        """
        conversation_dict = {}
        for mapping in self.mapping.values():
            conversation_dict[mapping.id] = [mapping.parent, mapping.children]
        return conversation_dict

    def _create_relationship_dict(self) -> Dict[str, Dict[str, int]]:
        """Creates a dictionary of relationships between messages"""
        relationship_dict = collections.defaultdict(
            lambda: collections.defaultdict(int)
        )

        for message_id, (parent_id, children_ids) in self.conversation_dict.items():
            # Add parent relationship
            if parent_id:
                relationship_dict[message_id][parent_id] += 1

            # Add child relationship
            for child_id in children_ids:
                relationship_dict[message_id][child_id] += 1

        return relationship_dict

    def get_relationship(
        self, message_id: str
    ) -> Dict[str, Union[List[Dict[str, Any]], int, None]]:
        """Returns all relationships for the message with the given ID in a dictionary."""
        if message_id not in self.message_dict:
            return None

        relationship_dict = {}

        for relationship_type, method in self.RELATIONSHIP_TYPES.items():
            try:
                relationship_dict[relationship_type] = getattr(self, method)(message_id)
            except ValueError as e:
                print(f"An error occurred: {str(e)}")

        return relationship_dict

    def _get_message_relationship_ids(
        self, message_id: str, relationship_type: str
    ) -> List[str]:
        relationships = self.get_message_reference(message_id, relationship_type)
        if relationships is None:
            return []
        return [rel.id for rel in relationships]

    def get_relationship_ids(self, message_id: str) -> Dict[str, List[str]]:
        """Returns a list of all message IDs that are related to the message with the given ID."""
        result = {}
        # exclude the descendants, ancestors, and siblings
        for relationship_type in [
            "cousins",
            "uncles_aunts",
            "nephews_nieces",
            "grandparents",
        ]:
            result[relationship_type] = self._get_message_relationship_ids(
                message_id, relationship_type
            )

        return result

    def _get_previous_sibling_id(self, message_id: str) -> Union[str, None]:
        """Returns the ID of the previous sibling of the message with the given ID, or None if the message is the first child or doesn't exist"""
        parent_id = self.get_parent_id(message_id)
        if parent_id is None:
            return None
        siblings_ids = self.get_children_ids(parent_id)
        try:
            index = siblings_ids.index(message_id)
        except ValueError:
            return None
        return siblings_ids[index - 1] if index > 0 else None

    def _get_next_sibling_id(self, message_id: str) -> Union[str, None]:
        """Returns the ID of the next sibling of the message with the given ID, or None if the message is the last child or doesn't exist"""
        parent_id = self.get_parent_id(message_id)
        if parent_id is None:
            return None
        siblings_ids = self.get_children_ids(parent_id)
        try:
            index = siblings_ids.index(message_id)
        except ValueError:
            return None
        return siblings_ids[index + 1] if index < len(siblings_ids) - 1 else None

    def get_message_reference(
        self, message_id: str, relationship_type: str
    ) -> Union[List[Dict[str, Any]], int, None]:
        """Returns the requested relationship for the message with the given ID."""
        if message_id not in self.message_dict:
            return None

        if relationship_type in self.RELATIONSHIP_TYPES:
            return getattr(self, self.RELATIONSHIP_TYPES[relationship_type])(message_id)
        else:
            raise ValueError(f"Unsupported relationship type: {relationship_type}")

    def get_parent_id(self, message_id: str) -> Union[str, None]:
        """Returns the ID of the parent of the message with the given ID, or None if the message doesn't exist or is the root"""
        if message_id not in self.message_dict:
            return None
        return self.conversation_dict[message_id][0]

    def get_children_ids(self, message_id: str) -> Union[List[str], None]:
        """Returns a list of the IDs of the children of the message with the given ID, or None if the message doesn't exist"""
        if message_id not in self.message_dict:
            return None
        return self.conversation_dict[message_id][1]

    def get_message_parent(self, message_id: str) -> Union[Dict[str, Any], None]:
        """Returns the parent of the message with the given ID, or None if the message doesn't exist or is the root"""
        if message_id not in self.message_dict:
            return None
        parent_id = self.conversation_dict[message_id][0]
        if parent_id is None:
            return None
        return self.message_dict[parent_id]

    def get_message_children(
        self, message_id: str
    ) -> Union[List[Dict[str, Any]], None]:
        """Returns a list of the children of the message with the given ID, or None if the message doesn't exist"""
        if message_id not in self.message_dict:
            return None
        children_ids = self.conversation_dict[message_id][1]
        children = [self.message_dict[child_id] for child_id in children_ids]
        return children

    def _get_message_ancestors(self, message_id: str) -> List[Dict[str, Any]]:
        parent = self.get_message_parent(message_id)
        return (
            [self.message_dict[message_id]] + self._get_message_ancestors(parent.id)
            if parent is not None
            else [self.message_dict[message_id]]
        )

    def _get_message_descendants(self, message_id: str) -> List[Dict[str, Any]]:
        children = self.get_message_children(message_id) or []
        return children + [
            descendant
            for child in children
            for descendant in self._get_message_descendants(child.id)
        ]

    def _get_message_siblings(self, message_id: str) -> List[Dict[str, Any]]:
        parent = self.get_message_parent(message_id)
        if parent is None:
            return []
        siblings = self.get_message_children(parent.id)
        siblings = [sibling for sibling in siblings if sibling.id != message_id]
        return siblings

    def _get_message_cousins(self, message_id: str) -> List[Dict[str, Any]]:
        parent = self.get_message_parent(message_id)
        if parent is None:
            return []
        uncles_and_aunts = self._get_message_siblings(parent.id)
        cousins = []
        for uncle_or_aunt in uncles_and_aunts:
            cousins.extend(self.get_message_children(uncle_or_aunt.id))
        return cousins

    def uncles_aunts(self, message_id: str) -> List[Dict[str, Any]]:
        """Returns a list of the uncles and aunts of the message with the given ID"""
        parent = self.get_message_parent(message_id)
        if parent is None:
            return []
        return self._get_message_siblings(parent.id)

    def nephews_nieces(self, message_id: str) -> List[Dict[str, Any]]:
        """Returns a list of the nephews and nieces of the message with the given ID"""
        uncles_and_aunts = self.uncles_aunts(message_id)
        nephews_nieces = []
        for uncle_or_aunt in uncles_and_aunts:
            nephews_nieces.extend(self.get_message_children(uncle_or_aunt.id))
        return nephews_nieces

    def grandparents(self, message_id: str) -> List[Dict[str, Any]]:
        """Returns a list of the grandparents of the message with the given ID"""
        parent = self.get_message_parent(message_id)
        if parent is None:
            return []
        return self._get_message_ancestors(parent.id)

    def get_message_depth(self, message_id: str) -> int:
        """Returns the depth of the message with the given ID"""
        return self._get_message_depth(message_id, 0)

    def _get_message_depth(self, message_id: str, depth: int) -> int:
        """Returns the depth of the message with the given ID"""
        parent = self.get_message_parent(message_id)
        if parent is None:
            return depth
        return self._get_message_depth(parent.id, depth + 1)
