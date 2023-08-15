from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from dl_matrix.models.message import Message
from dl_matrix.type import NodeRelationship


class ChainMap(BaseModel):
    """
    Represents a mapping between a message and its relationships.
    id (str): Unique identifier for the mapping.
    message (Optional[Message]): The message associated with the mapping.
    parent (Optional[str]): The ID of the parent message.
    children (List[str]): The IDs of the child messages.
    """

    id: str = Field(..., description="Unique identifier for the mapping.")

    message: Optional[Message] = Field(
        None, description="The message associated with the mapping."
    )

    parent: Optional[str] = Field(None, description="The ID of the parent message.")

    children: Optional[List[str]] = Field(
        [], description="The IDs of the child messages."
    )

    references: Optional[List[str]] = Field(
        [], description="The IDs of the referenced messages."
    )

    relationships: Dict[NodeRelationship, str] = Field(
        None,
        description="Relationships associated with the message.",
    )

    prev: Optional[str] = Field(None, description="The ID of the previous message.")

    next: Optional[str] = Field(None, description="The ID of the next message.")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "0",
                "message": {
                    "id": "0",
                    "text": "Hello World!",
                    "author": "User1",
                    "create_time": "2023-06-30T13:45:00",
                    "update_time": "2023-06-30T13:45:00",
                    "context_url": "http://example.com/context1",
                    "moderation_results": [
                        {
                            "model": "toxicity",
                            "result": 0.2,
                            "create_time": "2023-06-30T13:45:00",
                        }
                    ],
                },
                "parent": "1",
                "children": ["2", "3"],
                "connections": {
                    "REPLY_TO": {
                        "target_message_id": "Message1",
                        "timestamp": "2023-06-30T13:45:00",
                        "author": "User1",
                        "context_url": "http://example.com/context1",
                    },
                    "MENTION": {
                        "target_message_id": "Message2",
                        "timestamp": "2023-06-30T13:50:00",
                        "author": "User2",
                        "context_url": "http://example.com/context2",
                    },
                    "QUOTE": {
                        "target_message_id": "Message3",
                        "timestamp": "2023-06-30T13:55:00",
                        "author": "User3",
                        "context_url": "http://example.com/context3",
                    },
                    "FORWARD": {
                        "target_message_id": "Message4",
                        "timestamp": "2023-06-30T13:56:00",
                        "author": "User4",
                        "context_url": "http://example.com/context4",
                    },
                    "BACKWARD": {
                        "target_message_id": "Message5",
                        "timestamp": "2023-06-30T13:57:00",
                        "author": "User5",
                        "context_url": "http://example.com/context5",
                    },
                    "SIMILAR_TO": {
                        "target_message_id": "Message6",
                        "timestamp": "2023-06-30T13:58:00",
                        "author": "User6",
                        "context_url": "http://example.com/context6",
                    },
                },
                "coordinate": {
                    "id": "0",
                    "depth": {
                        "x": 0.0,
                        "s_x": 0.0,
                        "c_x": 0.0,
                    },
                    "sibling": {
                        "y": 0.0,
                        "a_y": 0.0,
                    },
                    "sibling_count": {
                        "z": 0.0,
                        "m_z": 0.0,
                    },
                    "time": {
                        "t": 0.0,
                        "p_y": 0.0,
                    },
                },
                "embedding": {
                    "id": "0",
                    "embedding": {
                        "term_id": "Term1",
                        "message_id": "Message1",
                        "cluster_label": 0,
                        "umap_embeddings": [0.0, 0.0, 0.0, 0.0, 0.0],
                        "embedding": [0.0, 0.0, 0.0, 0.0, 0.0],
                        "n_neighbors": 1,
                    },
                },
                "next": "1",
                "prev": "2",
                "network": {
                    "id": "0",
                    "nodes": [],
                    "edges": [],
                },
                "chain_weight": 0.0,
            }
        }

    def to_dict(self):
        return self.dict(by_alias=True, exclude_none=True)

    def to_message(self):
        return self.message

    @classmethod
    def from_mapping(cls, mapping: "ChainMap") -> "Message":
        """
        Creates a Message instance from a Mapping instance.

        Args:
            mapping (Mapping): The Mapping instance to convert.

        Returns:
            A Message instance.
        """
        if mapping.message is None:
            raise ValueError("Mapping does not contain a message")

        return mapping.message
