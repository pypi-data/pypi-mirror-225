from typing import Any, Dict, List, Optional
from .mapping import ChainMap
from pydantic import BaseModel, Field
from uuid import uuid4
from enum import Enum
import pandas as pd
import json
import networkx as nx


class ChainTreeType(str, Enum):
    """
    Represents the type of conversation tree.
    """

    FULL = "full"
    SUBGRAPH = "subgraph"
    NODE_IDS = "node_ids"
    ATTRIBUTE_FILTER = "attribute_filter"


class ChainQuery(BaseModel):
    """
    Represents a conversation tree query.
    Attributes:r
    conversation_tree_type (ConversationTreeType): The type of conversation tree.
    node_ids (List[str]): A list of node IDs to include in the conversation tree.
    attribute_filter (Dict[str, Any]): A dictionary where the key is the node attribute and the value is the desired attribute value.
    """

    conversation_tree_type: ChainTreeType = Field(
        None, description="The type of conversation tree."
    )

    node_ids: Optional[List[str]] = Field(
        None, description="A list of node IDs to include in the conversation tree."
    )

    attribute_filter: Optional[Dict[str, Any]] = Field(
        None,
        description="A dictionary where the key is the node attribute and the value is the desired attribute value.",
    )

    class Config:
        schema_extra = {
            "example": {
                "conversation_tree_type": "full",
                "node_ids": ["node_id_1", "node_id_2"],
                "attribute_filter": {"content": "Hello"},
            }
        }


class ChainTree(BaseModel):
    """

    Represents a conversation as a tree of messages.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))

    title: str = Field(None, description="The title of the conversation.")

    create_time: float = Field(
        None, description="The timestamp for when the conversation was created."
    )
    update_time: float = Field(
        None, description="The timestamp for when the conversation was last updated."
    )
    mapping: Dict[str, ChainMap] = Field(
        None,
        description="A dictionary mapping node IDs to their corresponding message nodes.",
    )

    moderation_results: Optional[List[Dict[str, Any]]] = Field(
        None, description="Moderation results associated with the conversation."
    )
    current_node: Optional[str] = Field(None, description="The ID of the current node.")

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.mapping is None:
            self.mapping = {}
        if self.moderation_results is None:
            self.moderation_results = []
        if self.current_node is None:
            self.current_node = None

    def retrieve_all_conversation_messages(self) -> List[ChainMap]:
        return list(self.mapping.values())

    def retrieve_all_conversation_messages_ids(self) -> List[str]:
        return list(self.mapping.keys())

    def retrieve_all_conversation_messages_contents(self) -> List[str]:
        return [message.message.content for message in self.mapping.values()]

    def retrieve_all_conversation_messages_authors(self) -> List[str]:
        return [message.message.author for message in self.mapping.values()]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChainTree":
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.dict()

    def to_json(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    def to_csv(self, path: str) -> None:
        df = pd.DataFrame.from_dict(self.mapping, orient="index")
        df.to_csv(path, index=False)

    @classmethod
    def from_json(cls, path: str) -> "ChainTree":
        with open(path, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)

    @classmethod
    def from_csv(cls, path: str) -> "ChainTree":
        df = pd.read_csv(path)
        data = df.to_dict(orient="index")
        return cls.from_dict(data)

    def __getitem__(self, key: str) -> ChainMap:
        return self.mapping[key]

    def __setitem__(self, key: str, value: ChainMap) -> None:
        self.mapping[key] = value

    def __delitem__(self, key: str) -> None:
        del self.mapping[key]

    def __iter__(self) -> ChainMap:
        return iter(self.mapping)

    def depth(self) -> int:
        """
        Returns the depth of the conversation tree.
        """
        return nx.dag_longest_path_length(self.to_networkx())

    def to_networkx(self) -> nx.DiGraph:
        """
        Returns the conversation tree as a networkx graph.
        """
        G = nx.DiGraph()
        for node_id, node in self.mapping.items():
            G.add_node(node_id, node=node)
        for node_id, node in self.mapping.items():
            for child_id in node.children:
                G.add_edge(node_id, child_id)
        return G

    def num_nodes(self) -> int:
        """
        Returns the number of nodes in the conversation tree.
        """
        return len(self.mapping)

    def average_branching_factor(self) -> float:
        """
        Returns the average branching factor of the conversation tree.
        """
        return self.num_nodes() / self.depth()

    def combine(self, other: "ChainTree") -> "ChainTree":
        """
        Combines two conversation trees into one.
        """
        mapping = {**self.mapping, **other.mapping}
        return ChainTree(mapping=mapping)

    def isnumeric(self) -> bool:
        """
        Returns True if all node IDs are numeric.
        """
        return all(node_id.isnumeric() for node_id in self.mapping.keys())


class ChainTreeIndex(BaseModel):
    conversation: ChainTree

    def to_dict(self) -> Dict[str, Any]:
        return {"conversation": self.conversation.dict()}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChainTreeIndex":
        return cls(conversation=ChainTree.from_dict(data["conversation"]))
