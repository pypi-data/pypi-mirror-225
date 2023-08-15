from pydantic import BaseModel
from typing import Dict, Any, Optional
from pydantic.fields import Field
from dl_matrix.type import RoleType


class Author(BaseModel):
    """
    Represents an author in the conversation.
    """

    role: RoleType = Field(..., description="The role of the author.")
    id: Optional[str] = Field(None, description="The ID of the author.")

    entity_name: Optional[str] = Field(None, description="The name of the author.")
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="The metadata of the author."
    )
    type: Optional[str] = Field(None, description="The type of the role.")
    description: Optional[str] = Field(None, description="The description of the role.")
    metadata: Optional[Dict[str, Any]] or object = Field(
        None, description="Additional metadata about the author."
    )

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "role": "user",
                "id": "123456789",
                "entity_name": "John Doe",
                "description": "The user of the conversation. This is the default role.",
                "metadata": {},
            }
        }
