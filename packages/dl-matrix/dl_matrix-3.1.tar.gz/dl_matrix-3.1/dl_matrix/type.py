from enum import Enum, auto


class ContentType(str, Enum):
    """
    Represents the type of  message content.
    Attributes:
        TEXT (str): A text message content..
        IMAGE (str): An image message content..
        AUDIO (str): An audio message content..
        VIDEO (str): A video message content..
        FILE (str): A file message content..
        LOCATION (str): A location message content..
        CONTACT (str): A contact message content..
        LINK (str): A link message content..
        EVENT (str): An event message content..
        OTHER (str): A message content. of another type.
    """

    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    FILE = "file"
    LOCATION = "location"
    CONTACT = "contact"
    MESSAGE = "message"
    LINK = "link"
    EVENT = "event"
    DIRECTORY = "directory"
    OTHER = "other"


class ConnectionType(str, Enum):
    REPLY_TO = "REPLY_TO"
    MENTION = "MENTION"
    QUOTE = "QUOTE"
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"
    SIMILAR_TO = "SIMILAR_TO"
    RESPONSE_TO = "RESPONSE_TO"
    QUESTION_TO = "QUESTION_TO"
    COUNTER = "COUNTER"


class ConnectionStrength(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class RoleType(str, Enum):
    USER = "user"
    CHAT = "chat"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    ADMIN = "admin"
    GUEST = "guest"
    ANONYMOUS = "anonymous"
    MODERATOR = "moderator"
    OWNER = "owner"
    DEVELOPER = "developer"
    CREATOR = "creator"


class NodeRelationship(str, Enum):
    """Node relationships used in `BaseNode` class.

    Attributes:
        SOURCE: The node is the source document.
        PREVIOUS: The node is the previous node in the document.
        NEXT: The node is the next node in the document.
        PARENT: The node is the parent node in the document.
        CHILD: The node is a child node in the document.

    """

    SOURCE = auto()
    PREVIOUS = auto()
    NEXT = auto()
    PARENT = auto()
    CHILD = auto()


class ElementType(Enum):
    STEP = "Step"
    CHAPTER = "Chapter"
    PAGE = "Page"
    SECTION = "Section"
