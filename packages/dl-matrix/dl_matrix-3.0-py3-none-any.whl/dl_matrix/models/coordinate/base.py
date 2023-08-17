import numpy as np
import torch
from pydantic import BaseModel, Field, validator, ValidationError
from typing import List, Dict, Union, Any
from uuid import uuid4
from math import sqrt


class Coordinate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    x: float = Field(0, description="The depth of the coordinate.")
    y: float = Field(0, description="The sibling of the coordinate.")
    z: float = Field(0, description="The sibling count of the coordinate.")
    t: float = Field(0, description="The time of the coordinate.")
    n_parts: float = Field(0, description="The number of parts of the coordinate.")

    @classmethod
    def create(
        cls,
        depth_args: Union[int, list] = 0,
        sibling_args: Union[int, list] = 0,
        sibling_count_args: Union[int, list] = 0,
        time_args: Union[int, list] = 0,
        n_parts_args: Union[int, list] = 0,
    ):
        return cls(
            x=depth_args[0]
            if isinstance(depth_args, list) and len(depth_args) > 0
            else depth_args,
            y=sibling_args[0]
            if isinstance(sibling_args, list) and len(sibling_args) > 0
            else sibling_args,
            z=sibling_count_args[0]
            if isinstance(sibling_count_args, list) and len(sibling_count_args) > 0
            else sibling_count_args,
            t=time_args[0]
            if isinstance(time_args, list) and len(time_args) > 0
            else time_args,
            n_parts=n_parts_args[0]
            if isinstance(n_parts_args, list) and len(n_parts_args) > 0
            else n_parts_args,
        )

    def __iter__(self):
        return iter(self.dict().values())

    class Config:
        title = "Coordinate Representation"
        description = "A model to represent coordinates with enhanced properties suitable for neural network operations."

    @validator("n_parts", pre=True, always=True)
    def validate_n_parts(cls, value: Any) -> float:
        if not isinstance(value, (int, float)):
            raise ValidationError(
                f"Expected n_parts to be numeric, received: {type(value)}"
            )
        return max(0, value)

    @staticmethod
    def get_coordinate_names() -> List[str]:
        """Return names of the coordinate dimensions."""
        return [
            "depth_x",
            "sibling_y",
            "sibling_count_z",
            "time_t",
            "n_parts",
        ]

    @staticmethod
    def unflatten(values: np.ndarray) -> "Coordinate":
        """Convert a flattened array back into a Coordinate."""
        assert values.shape[0] == 5, "Invalid shape for unflattening"
        return Coordinate(
            x=values[0],
            y=values[1],
            z=values[2],
            t=values[3],
            n_parts=values[4],
        )

    @classmethod
    def from_tensor(cls, tensor: torch.Tensor) -> "Coordinate":
        """Initialize Coordinate from a PyTorch tensor."""
        return cls.unflatten(tensor.cpu().numpy())

    def to_reduced_array(self) -> np.array:
        """
        Convert the Coordinate object into a reduced numpy array representation, excluding n_parts.

        Returns:
            A numpy array representation without n_parts.
        """
        return np.array([self.x, self.y, self.z, self.t])

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
        # Check if the values in the dictionary are Coordinate objects. If they are, use the reduced representation.
        coordinates_list = [
            value.to_reduced_array() if isinstance(value, Coordinate) else value
            for value in coordinates_dict.values()
        ]

        # Ensure the array values are of the expected shape (i.e., length 4). This will handle cases where np.arrays are provided directly.
        coordinates_list = [coords[:4] for coords in coordinates_list]

        # Stack them into a 2D numpy array
        coordinates_array = np.stack(coordinates_list, axis=0)

        # Convert the 2D array to a PyTorch tensor.
        coordinates_tensor = torch.tensor(coordinates_array, dtype=torch.float32)

        return coordinates_tensor

    def __iter__(self) -> iter:
        return iter(self.dict().values())

    @staticmethod
    def flatten(coordinate: "Coordinate") -> np.ndarray:
        """Flatten the Coordinate instance into a numpy array."""
        return np.array(
            [
                coordinate.x,
                coordinate.y,
                coordinate.z,
                coordinate.t,
                coordinate.n_parts,
            ]
        )

    def tuple(self) -> tuple:
        """Convert Coordinate to tuple."""
        return tuple(self.dict().values())

    @staticmethod
    def flatten_list(coordinates: List["Coordinate"]) -> np.ndarray:
        """Flatten a list of Coordinates."""
        return np.array([Coordinate.flatten(c) for c in coordinates])

    @staticmethod
    def flatten_list_of_lists(coordinates: List[List["Coordinate"]]) -> np.ndarray:
        """Flatten a list of list of Coordinates."""
        return np.array([[Coordinate.flatten(c) for c in cs] for cs in coordinates])

    @staticmethod
    def string_to_coordinate(coordinate_str: str) -> "Coordinate":
        """Convert a string representation to Coordinate."""
        coordinate_arr = np.fromstring(coordinate_str, sep=",")
        if coordinate_arr.shape[0] != 5:
            raise ValidationError("Invalid string representation for Coordinate.")
        return Coordinate.unflatten(coordinate_arr)

    @staticmethod
    def stack_coordinates(
        coordinates_dict: Dict[str, Union["Coordinate", np.array]]
    ) -> np.array:
        """Stack coordinates from a dictionary."""
        return np.stack(list(coordinates_dict.values()), axis=0)

    @staticmethod
    def to_tensor_from_dict(
        coordinates_dict: Dict[str, Union["Coordinate", np.array]]
    ) -> torch.Tensor:
        """Convert dictionary of Coordinates to tensor."""
        coordinates_array = Coordinate.stack_coordinates(coordinates_dict)
        return torch.tensor(coordinates_array, dtype=torch.float32)

    # Operator Overloads
    def __add__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
            t=self.t + other.t,
            n_parts=self.n_parts + other.n_parts,
        )

    def __sub__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z,
            t=self.t - other.t,
            n_parts=self.n_parts - other.n_parts,
        )

    @property
    def magnitude(self) -> float:
        """Compute the magnitude (euclidean norm) of the coordinate as a vector."""
        return sqrt(
            self.x**2 + self.y**2 + self.z**2 + self.t**2 + self.n_parts**2
        )

    def distance(self, other: "Coordinate") -> float:
        """Compute the Euclidean distance between two coordinates."""
        return (self - other).magnitude

    def embedding(self, embedding_dim: int) -> torch.Tensor:
        """Transform the Coordinate into an embedding tensor suitable for NN."""
        # This is just a naive example; real embedding would probably utilize a learned embedding layer.
        base_tensor = self.to_tensor()
        return torch.nn.functional.embedding(
            base_tensor.long(), torch.eye(embedding_dim)
        )

    @classmethod
    def batch_to_tensor(cls, batch: List["Coordinate"]) -> torch.Tensor:
        """Convert a batch of Coordinates to a single tensor."""
        return torch.stack([coordinate.to_tensor() for coordinate in batch])

    def serialize(self) -> str:
        """Serialize the Coordinate object to a string."""
        return ",".join([str(x) for x in self])

    @classmethod
    def deserialize(cls, data: str) -> "Coordinate":
        """Deserialize a string to a Coordinate object."""
        values = list(map(float, data.split(",")))
        return cls(
            x=values[0], y=values[1], z=values[2], t=values[3], n_parts=values[4]
        )

    def save(self, filename: str) -> None:
        """Save the serialized Coordinate object to a file."""
        with open(filename, "w") as f:
            f.write(self.serialize())

    @classmethod
    def load(cls, filename: str) -> "Coordinate":
        """Load a Coordinate object from a file."""
        with open(filename, "r") as f:
            data = f.read().strip()
        return cls.deserialize(data)
