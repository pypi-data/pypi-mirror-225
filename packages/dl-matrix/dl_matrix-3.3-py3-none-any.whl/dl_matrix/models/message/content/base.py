from typing import List, Optional, Any
from pydantic import BaseModel, Field
from dl_matrix.type import ContentType


class Content(BaseModel):
    """
    The base class for all content types.
    """

    text: Optional[str] = Field(
        None, description="The text content of the message (if any)."
    )

    content_type: ContentType = Field(
        ContentType.TEXT, description="The type of content (text, image, audio, etc.)"
    )
    parts: Optional[List[str]] = Field(
        None, description="The parts of the content (text, image, audio, etc.)"
    )

    part_lengths: Optional[Any] = Field(
        None, description="The lengths of the parts of the content."
    )

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"
        json_schema_extra = {
            "example": {
                "content_type": "text",
                "parts": ["Hello, how are you?"],
            }
        }

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.parts:
            self.text = self.parts[0]
            self.part_lengths = len(self.text.split("\n\n")) if self.text else []
        else:
            self.part_lengths = 0  # If parts are not provided, set part_lengths to 0.

    @classmethod
    def from_text(cls, text: str):
        """Creates a Content object from text."""
        return cls(content_type=ContentType.TEXT, parts=[text])

    @classmethod
    def from_content_type(cls, content_type: ContentType, parts: List[str]):
        """Creates a Content object from content type and parts."""
        return cls(content_type=content_type, parts=parts)

    @classmethod
    def from_message(cls, message):
        """
        Create a Content object from a Message object.

        Args:
            message: A Message object.

        Returns:
            A Content object.
        """
        return cls(content_type="text", parts=[message.content])
