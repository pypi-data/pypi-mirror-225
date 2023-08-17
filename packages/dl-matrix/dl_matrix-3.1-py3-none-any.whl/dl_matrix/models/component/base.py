from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field, validator
from dl_matrix.models import Content, Author, Coordinate, User, Assistant, System
from typing import Optional
from abc import ABC, abstractmethod
import uuid


class ComponentModel(BaseModel):
    # This is the base class for all our static component models
    class Config:
        validate_assignment = True  # Enable field validation on assignment

    def communicate(self, other: "ComponentModel", message: str) -> None:
        """Send a message to another component model."""
        if hasattr(other, "messages"):
            other.messages.append(message)
        else:
            raise AttributeError(
                f"The other model {other.__class__.__name__} does not support messaging."
            )


class DistanceStrategy(ABC):
    @abstractmethod
    def compute(self, chain_a: "Chain", chain_b: "Chain") -> float:
        pass


class EuclideanEmbeddingDistance(DistanceStrategy):
    def compute(self, chain_a: "Chain", chain_b: "Chain") -> float:
        return (
            sum([(a - b) ** 2 for a, b in zip(chain_a.embedding, chain_b.embedding)])
            ** 0.5
        )


class ManhattanEmbeddingDistance(DistanceStrategy):
    def compute(self, chain_a: "Chain", chain_b: "Chain") -> float:
        return sum([abs(a - b) for a, b in zip(chain_a.embedding, chain_b.embedding)])


class CoordinateDistance(DistanceStrategy):
    def compute(self, chain_a: "Chain", chain_b: "Chain") -> float:
        return (
            sum([(a - b) ** 2 for a, b in zip(chain_a.coordinate, chain_b.coordinate)])
            ** 0.5
        )


class Chain(ComponentModel):
    id: str = Field(..., description="Unique identifier for the chain.")
    author: Author = Field(..., description="The author of the chain.")
    content: Content = Field(..., description="The content of the chain.")
    coordinate: Coordinate = Field(
        ..., description="The coordinate of the chain in the conversation tree."
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Any additional metadata about the chain."
    )
    embedding: Optional[List[float]] = Field(
        None, description="Embeddings of the chain."
    )
    children: Optional[List["Chain"]] = Field(
        [], description="The children of the chain in the conversation tree."
    )

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "id": "Chain1",
                "author": {"role": "Role.USER", "metadata": {}},
                "content": {"content_type": "text", "parts": ["Hello"]},
                "coordinate": {"x": 0, "y": 0, "z": 0, "w": 0},
                "metadata": {},
                "embedding": [],
                "children": [],
            }
        }

    @validator("children", pre=True, each_item=True)
    def validate_children(cls, v):
        if not isinstance(v, Chain):
            raise ValueError("Child must be an instance of Chain.")
        return v

    def add_child(self, child: "Chain"):
        """Add a child to the current chain."""
        if not isinstance(child, Chain):
            raise TypeError("Child must be an instance of Chain.")
        self.children.append(child)

    def remove_child(self, child: "Chain"):
        """Remove a child from the current chain."""
        if child in self.children:
            self.children.remove(child)

    def get_children(self) -> List["Chain"]:
        """Retrieve the list of children of the current chain."""
        return self.children

    def get_distance(
        self, other_chain: "Chain", strategy: DistanceStrategy
    ) -> Optional[float]:
        """Calculate the distance between two chains based on a specified strategy.
        Assumes embeddings and coordinates are lists of floats.
        """
        if not self.embedding or not other_chain.embedding:
            print("One or both chains don't have embeddings.")
            return None

        if len(self.embedding) != len(other_chain.embedding):
            print("Embeddings don't have the same dimension.")
            return None

        try:
            return strategy.compute(self, other_chain)

        except TypeError:
            print(
                "One of the properties (embedding/coordinate) contains non-numeric values."
            )
            return None

        except Exception as e:
            print(f"Error computing distance: {str(e)}")
            return None

    def __str__(self):
        return f"{self.author.role} Chain: {self.content.parts[0]}"

    def __len__(self):
        return len(self.children)


class AssistantChain(Chain):
    def __init__(
        self,
        id: str,
        content: Content,
        coordinate: Coordinate,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            id=id,
            author=Assistant(),
            content=content,
            coordinate=coordinate,
            metadata=metadata,
        )


class UserChain(Chain):
    def __init__(
        self,
        id: str,
        content: Content,
        coordinate: Coordinate,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            id=id,
            author=User(),
            content=content,
            coordinate=coordinate,
            metadata=metadata,
        )


class SystemChain(Chain):
    def __init__(
        self,
        id: str,
        content: Content,
        coordinate: Coordinate,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            id=id,
            author=System(),
            content=content,
            coordinate=coordinate,
            metadata=metadata,
        )


def _convert_dict_to_message(message_dict: dict) -> Chain:
    role = message_dict["role"]
    content = Content(raw=message_dict["content"])
    coordinate = Coordinate(x=0, y=0, z=0, t=0)  # Use default coordinates for now

    if role == "user":
        return UserChain(id=str(uuid.uuid4()), content=content, coordinate=coordinate)
    elif role == "assistant":
        return AssistantChain(
            id=str(uuid.uuid4()), content=content, coordinate=coordinate
        )
    elif role == "system":
        return SystemChain(id=str(uuid.uuid4()), content=content, coordinate=coordinate)
    else:
        raise ValueError(f"Got unknown role {role}")
