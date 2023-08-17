from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Generic
from dl_matrix.models import ChainMap
from pydantic import BaseModel, Field, PrivateAttr, create_model
from typing import Optional, Any, Dict, List, Type
from pydantic.generics import GenericModel, TypeVar

T = TypeVar("T")


# Define a base message processing class
class BaseMessageProcessing(ABC):
    @abstractmethod
    def __init__(self, message_data: List[ChainMap]):
        self.message_data = message_data

    @abstractmethod
    def filter_messages_by_condition(
        self, condition_func: Callable[[ChainMap], bool]
    ) -> List[ChainMap]:
        pass


# Define interfaces
class IMessageExtractor(BaseMessageProcessing):
    @abstractmethod
    def retrieve_all_conversation_messages(self) -> List[ChainMap]:
        pass


class IMessageSearcher(BaseMessageProcessing):
    @abstractmethod
    def find_messages_by_author(self, author: str) -> List[ChainMap]:
        pass

    @abstractmethod
    def find_similar(self, message_id: str, top_k: int = 5) -> List[ChainMap]:
        pass


class IMessageAnalyzer(BaseMessageProcessing):
    @abstractmethod
    def count_messages_by_author(self) -> Dict[str, int]:
        pass


class AbstractMessageFilter(ABC):
    @abstractmethod
    def filter(self, messages: List[ChainMap], *args, **kwargs) -> List[int]:
        pass


class FilterHandler:
    def __init__(self, message_filter: AbstractMessageFilter):
        self.message_filter = message_filter

    def filter_messages(self, messages: List[ChainMap], *args, **kwargs) -> List[int]:
        return self.message_filter.filter(messages, *args, **kwargs)

    def apply(self, messages: List[ChainMap], *args, **kwargs) -> List[int]:
        return self.filter_messages(messages, *args, **kwargs)


class FilterHandler:
    def __init__(
        self,
        exception_handler: Optional[Callable] = None,
        decorator: Optional[Callable] = None,
    ):
        self.exception_handler = exception_handler
        self.decorator = decorator

    def apply(self, callback: Callable, *args, **kwargs):
        if self.exception_handler:
            try:
                result = callback(*args, **kwargs)
            except Exception as e:
                result = self.exception_handler(e)
        else:
            result = callback(*args, **kwargs)

        if self.decorator:
            return self.decorator(result)
        else:
            return result


class Filter:
    def __init__(self, callback: Callable[[ChainMap], bool], negate: bool = False):
        self.callback = callback
        self.negate = negate

    def matches(self, message: ChainMap) -> bool:
        match = self.callback(message)
        return not match if self.negate else match


class Component(Generic[T]):
    dimensions: Dict[str, Optional[int]] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True

    _model: Any = PrivateAttr(default=None)

    def __init__(self, name: str, dimensions: List[str], **data: Optional[int]) -> None:
        super().__init__(
            name=name,
            dimensions={
                f"dim_{dim}": data.get(f"dim_{dim}", None) for dim in dimensions
            },
        )
        self._model = self.__create_model__(name, dimensions=dimensions, **data)

    @staticmethod
    def __create_model__(
        name: str, dimensions: List[str], **data: Optional[int]
    ) -> Type[BaseModel]:
        # Create a new Pydantic model with the specified dimensions
        return create_model(
            name,
            **{
                f"dim_{dim}": (Optional[int], data.get(f"dim_{dim}", None))
                for dim in dimensions
            },
        )

    def __call__(self, **data: Optional[int]) -> BaseModel:
        return self._model(**data)

    def flatten(self, **data: Optional[int]) -> Dict[str, Optional[int]]:
        return self(**data).dict()


class Attribute(GenericModel, BaseModel):
    _model: Any = PrivateAttr(default=None)

    def __init__(self, name: str, attributes: List[str], **data: Any) -> None:
        super().__init__(
            name=name, attributes={attr: data.get(attr, None) for attr in attributes}
        )

    def __new__(cls, name: str, attributes: List[str], **data: Any):
        # Dynamically create a new Pydantic model with the specified attributes
        model = cls.__create_model__(name, attributes=attributes, **data)
        object.__setattr__(cls, "_model", model)
        return model

    @classmethod
    def __create_model__(
        cls, name: str, attributes: List[str], **data: Any
    ) -> Type[BaseModel]:
        # Create a new Pydantic model with the specified attributes
        return create_model(
            name, **{attr: (Optional[Any], data.get(attr, None)) for attr in attributes}
        )

    def __call__(self, **data: Any) -> BaseModel:
        return self._model(**data)

    def flatten(self, **data: Any) -> Dict[str, Any]:
        return self(**data).dict()
