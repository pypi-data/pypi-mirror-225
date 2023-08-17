"""Common schema objects."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, Union, Set
from dl_matrix.models import (
    Content,
    Chain,
    Metadata,
    Message,
    User,
    Assistant,
    System,
    UserChain,
    AssistantChain,
    SystemChain,
)
from dl_matrix.transformation import Coordinate
from pydantic import BaseModel, root_validator, Field
import uuid
import time

Data = Union[Dict[str, Any], List[Dict[str, Any]]]


class SynthesisTechnique(ABC):
    def __init__(
        self,
        epithet: str,
        name: str,
        technique_name: str,
        imperative: str,
        prompts: Dict[str, Any],
    ):
        self.epithet = epithet
        self.name = name
        self.technique_name = technique_name
        self.imperative = imperative
        self.prompts = prompts

    @abstractmethod
    def execute(self, *args, **kwargs) -> None:
        pass

    def get_options(self) -> Dict[str, Any]:
        return {
            "epithet": self.epithet,
            "name": self.name,
            "technique_name": self.technique_name,
            "imperative": self.imperative,
            "prompts": self.prompts,
        }


class BaseMessage(BaseModel):
    """Message object."""

    content: str
    additional_kwargs: dict = Field(default_factory=dict)

    @property
    @abstractmethod
    def type(self) -> str:
        """Type of the message, used for serialization."""


class Generation(BaseModel):
    """Output of a single generation."""

    text: str
    """Generated text output."""

    generation_info: Optional[Dict[str, Any]] = None
    """Raw generation info response from the provider"""
    """May include things like reason for finishing (e.g. in OpenAI)"""
    # TODO: add log probs


class ChatGeneration(Generation):
    """Output of a single generation."""

    text = ""
    message: Chain

    @root_validator
    def set_text(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        values["text"] = values["message"].content
        return values


class ChatResult(BaseModel):
    """Class that contains all relevant information for a Chat Result."""

    generations: List[ChatGeneration]
    """List of the things generated."""
    llm_output: Optional[dict] = None
    """For arbitrary LLM provider specific output."""


class LLMResult(BaseModel):
    """Class that contains all relevant information for an LLM Result."""

    generations: List[List[Generation]]
    """List of the things generated. This is List[List[]] because
    each input could have multiple generations."""
    llm_output: Optional[dict] = None
    """For arbitrary LLM provider specific output."""


class PromptValue(BaseModel, ABC):
    @abstractmethod
    def to_string(self) -> str:
        """Return prompt as string."""

    @abstractmethod
    def to_chain(self) -> List[Chain]:
        """Return prompt as messages."""


def get_buffer_string(
    messages: List[Dict[str, Any]], human_prefix: str = "Human", ai_prefix: str = "AI"
) -> str:
    """Get buffer string of messages."""
    string_messages = []
    for m in messages:
        if "role" in m and "content" in m:
            if m["role"] == "user":
                role = human_prefix
            elif m["role"] == "assistant":
                role = ai_prefix
            elif m["role"] == "system":
                role = "System"
            else:
                raise ValueError(f"Got unsupported message type: {m}")

            string_messages.append(f"{role}: {m['content']}")
        else:
            raise ValueError(f"Invalid message format: {m}")

    return "\n".join(string_messages)


class ChainBuilder(ABC):
    @abstractmethod
    def build_system_chain(self, content: Content, coordinate: Coordinate):
        pass

    @abstractmethod
    def build_assistant_chain(self, content: Content, coordinate: Coordinate):
        pass

    @abstractmethod
    def build_user_chain(self, content: Content, coordinate: Coordinate):
        pass

    def get_result(self):
        return self.chain_tree


class IChainTree(ABC):
    @abstractmethod
    def add_chain(
        self,
        chain_type: Type[Chain],
        id: str,
        content: Content,
        coordinate: Coordinate,
        metadata: Optional[Dict[str, Any]],
    ):
        pass

    @abstractmethod
    def get_chains(self):
        pass

    @abstractmethod
    def get_chain(self, id: str):
        pass

    @abstractmethod
    def get_last_chain(self):
        pass

    @abstractmethod
    def get_chains_by_type(self, chain_type: str):
        pass

    @abstractmethod
    def get_chains_by_coordinate(self, coordinate: Coordinate):
        pass

    @abstractmethod
    def remove_chain(self, id: str):
        pass

    @abstractmethod
    def update_chain(
        self,
        id: str,
        new_content: Optional[Content] = None,
        new_coordinate: Optional[Coordinate] = None,
        new_metadata: Optional[Dict[str, Any]] = None,
    ):
        pass

    def add_link(self, link: dict):
        pass


class IChainFactory(ABC):
    @abstractmethod
    def create_chain(
        self,
        chain_type: str,
        id: str,
        content: Content,
        coordinate: Coordinate,
        metadata: Optional[Dict[str, Any]],
    ) -> Chain:
        pass


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


class BaseConversation(ABC):
    @abstractmethod
    def get_history(self) -> List[Chain]:
        pass


def create_system_message() -> Message:
    """
    Create a System message.

    Returns:
        Message: The System message object.
    """
    content_data = {
        "content_type": "text",
        "parts": [],
    }
    system = System()
    return Message(
        id=str(uuid.uuid4()),
        create_time=time.time(),
        content=Content(**content_data),
        author=system,
    )


def create_user_message(
    message_id: str,
    text: str,
    metadata: Optional[Metadata] = None,
    user_embeddings: List[float] = None,
) -> Message:
    """
    Create a User message.

    Args:
        message_id (str): The unique identifier for the User message.
        text (str): The content of the User message.
        metadata (Optional[Metadata]): The metadata associated with the User message. Defaults to None.

    Returns:
        Message: The User message object.
    """
    content_data = {
        "content_type": "text",
        "parts": [text],
        "embedding": user_embeddings,
    }

    user = User()
    return Message(
        id=message_id,
        create_time=time.time(),
        content=Content(**content_data),
        author=user,
        metadata=metadata,
    )


def create_assistant_message(
    text: str, assistant_embeddings: List[float] = None
) -> Message:
    """
    Create an Assistant message.

    Args:
        text (str): The generated content for the Assistant message.

    Returns:
        Message: The Assistant message object.
    """
    assistant = Assistant()
    return Message(
        id=str(uuid.uuid4()),
        create_time=time.time(),
        content=Content(
            content_type="text",
            parts=[text],
            embedding=assistant_embeddings,
        ),
        author=assistant,
        end_turn=True,
    )


class ChatMessage(Chain):
    """Type of message with arbitrary speaker."""

    role: str

    @property
    def type(self) -> str:
        """Type of the message, used for serialization."""
        return "chat"


def _get_token_ids_default_method(text: str) -> List[int]:
    try:
        from transformers import GPT2TokenizerFast
    except ImportError:
        raise ValueError(
            "Could not import transformers python package. "
            "This is needed in order to calculate get_token_ids. "
            "Please install it with `pip install transformers`."
        )
    # create a GPT-2 tokenizer instance
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

    # tokenize the text using the GPT-2 tokenizer
    return tokenizer.encode(text)


class BaseLanguageModel(BaseModel, ABC):
    @abstractmethod
    def generate_prompt(
        self,
        prompts: List[PromptValue],
        stop: Optional[List[str]] = None,
        callbacks: object = None,
    ) -> LLMResult:
        """Take in a list of prompt values and return an LLMResult."""

    @abstractmethod
    async def agenerate_prompt(
        self,
        prompts: List[PromptValue],
        stop: Optional[List[str]] = None,
        callbacks: object = None,
    ) -> LLMResult:
        """Take in a list of prompt values and return an LLMResult."""

    def get_token_ids(self, text: str) -> List[int]:
        """Get the token present in the text."""
        return _get_token_ids_default_method(text)

    def get_num_tokens(self, text: str) -> int:
        """Get the number of tokens present in the text."""
        return len(self.get_token_ids(text))

    def get_num_tokens_from_messages(self, messages: List[BaseMessage]) -> int:
        """Get the number of tokens in the message."""
        return sum([self.get_num_tokens(get_buffer_string([m])) for m in messages])

    @classmethod
    def all_required_field_names(cls) -> Set:
        all_required_field_names = set()
        for field in cls.__fields__.values():
            all_required_field_names.add(field.name)
            if field.has_alias:
                all_required_field_names.add(field.alias)
        return all_required_field_names
