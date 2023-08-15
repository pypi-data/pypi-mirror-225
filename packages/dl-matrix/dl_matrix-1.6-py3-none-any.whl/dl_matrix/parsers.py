from dl_matrix.models import (
    ChainTree,
    ChainTreeIndex,
    ChainMap,
    Message,
    Content,
    Author,
    Metadata,
    ChainQuery,
)
from typing import Any, Dict, List, Union

Data = Union[Dict[str, Any], List[Dict[str, Any]]]


class ChainTreeParser:
    @staticmethod
    def parse_chain_tree(
        data: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> Union[ChainTree, List[ChainTree]]:
        if isinstance(data, dict):
            return ChainTree(**data)
        elif isinstance(data, list):
            return [ChainTree(**chain_tree) for chain_tree in data]
        else:
            raise ValueError("Invalid data type, should be dict or list of dicts.")


class ChainTreeIndexParser:
    @staticmethod
    def parse_conversation_tree(
        data: Data,
    ) -> Union[ChainTreeIndex, List[ChainTreeIndex]]:
        if isinstance(data, dict):
            return ChainTreeIndex(**data)
        elif isinstance(data, list):
            return [ChainTreeIndex(**conversation) for conversation in data]
        else:
            raise TypeError(
                "Invalid data type. Data should be a dictionary or a list of dictionaries."
            )


class ChainMapParser:
    @staticmethod
    def parse_mapping(data: Data) -> Union[ChainMap, List[ChainMap]]:
        if isinstance(data, dict):
            return ChainMap(**data)
        elif isinstance(data, list):
            return [ChainMap(**mapping) for mapping in data]
        else:
            raise TypeError(
                "Invalid data type. Data should be a dictionary or a list of dictionaries."
            )

    @staticmethod
    def parse_message(data: Data) -> Union[Message, List[Message]]:
        if isinstance(data, dict):
            return Message(**data)
        elif isinstance(data, list):
            return [Message(**message) for message in data]
        else:
            raise TypeError(
                "Invalid data type. Data should be a dictionary or a list of dictionaries."
            )

    @staticmethod
    def parse_content(data: Data) -> Union[Content, List[Content]]:
        if isinstance(data, dict):
            return Content(**data)
        elif isinstance(data, list):
            return [Content(**content) for content in data]
        else:
            raise TypeError(
                "Invalid data type. Data should be a dictionary or a list of dictionaries."
            )

    @staticmethod
    def parse_author(data: Data) -> Union[Author, List[Author]]:
        if isinstance(data, dict):
            return Author(**data)
        elif isinstance(data, list):
            return [Author(**author) for author in data]
        else:
            raise TypeError(
                "Invalid data type. Data should be a dictionary or a list of dictionaries."
            )

    @staticmethod
    def parse_metadata(data: Data) -> Union[Metadata, List[Metadata]]:
        if isinstance(data, dict):
            return Metadata(**data)
        elif isinstance(data, list):
            return [Metadata(**metadata) for metadata in data]
        else:
            raise TypeError(
                "Invalid data type. Data should be a dictionary or a list of dictionaries."
            )


class ChainQueryParser:
    @staticmethod
    def parse_conversation_tree_query(
        data: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> Union[ChainQuery, List[ChainQuery]]:
        if isinstance(data, dict):
            return ChainQuery(**data)
        elif isinstance(data, list):
            return [
                ChainQuery(**conversation_tree_query)
                for conversation_tree_query in data
            ]
        else:
            raise TypeError(
                "Invalid data type. Data should be a dictionary or a list of dictionaries."
            )


class Parser:
    @staticmethod
    def parse_chain_tree(
        data: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> Union[ChainTree, List[ChainTree]]:
        return ChainTreeParser.parse_chain_tree(data)

    @staticmethod
    def parse_conversation_tree(
        data: Data,
    ) -> Union[ChainTreeIndex, List[ChainTreeIndex]]:
        return ChainTreeIndexParser.parse_conversation_tree(data)

    @staticmethod
    def parse_mapping(data: Data) -> Union[ChainMap, List[ChainMap]]:
        return ChainMapParser.parse_mapping(data)

    @staticmethod
    def parse_message(data: Data) -> Union[Message, List[Message]]:
        return ChainMapParser.parse_message(data)

    @staticmethod
    def parse_content(data: Data) -> Union[Content, List[Content]]:
        return ChainMapParser.parse_content(data)

    @staticmethod
    def parse_author(data: Data) -> Union[Author, List[Author]]:
        return ChainMapParser.parse_author(data)

    @staticmethod
    def parse_metadata(data: Data) -> Union[Metadata, List[Metadata]]:
        return ChainMapParser.parse_metadata(data)

    @staticmethod
    def parse_conversation_tree_query(
        data: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> Union[ChainQuery, List[ChainQuery]]:
        return ChainQueryParser.parse_conversation_tree_query(data)
