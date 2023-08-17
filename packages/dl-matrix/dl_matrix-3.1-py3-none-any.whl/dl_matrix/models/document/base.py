from typing import Type, List, Optional, Dict, Any, Union, Set, Iterator
from dl_matrix.type import NodeRelationship
from pydantic import BaseModel, Field
import pandas as pd
import sqlite3
import uuid
import json
from uuid import uuid4


def get_new_id(d: Set) -> str:
    """Get a new ID."""
    while True:
        new_id = str(uuid.uuid4())
        if new_id not in d:
            break
    return new_id


class ChainDocument(BaseModel):

    """

    Base document.

    Generic abstract interfaces that captures both index structs
    as well as documents.

    """

    doc_id: Optional[str] = Field(
        default_factory=lambda: str(uuid4()),
        description="The ID of the document.",
    )

    text: Optional[Any] = Field(
        default=None,
        description="The text of the document.",
    )

    author: Optional[str] = Field(
        default=None,
        description="The author of the document.",
    )

    children: Optional[List[object]] = Field(
        default_factory=list,
        description="Child nodes of this document in the document tree.",
    )

    coordinate: Optional[object] or Dict[str, Any] = Field(
        default=None,
        description="Coordinate of the document in the embedding space. This could be useful in visualization or for spatial querying.",
    )

    sub_graph: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="The graph representation of the document. This could be useful for constructing graphs of documents.",
    )

    umap_embeddings: Optional[Any] = Field(
        default=None,
        description="UMAP embeddings of the document. This could be useful for visualization or dimension reduction.",
    )

    embedding: Optional[Any] = Field(
        default=None,
        description="Embedding of the document. This could be useful for similarity search.",
    )
    cluster_label: Optional[int] = Field(
        default=None,
        description="The label of the cluster this document belongs to. Useful for cluster-based analysis or navigation.",
    )
    n_neighbors: Optional[Any] = Field(
        default=None,
        description="The number of nearest neighbors for this document. Useful for constructing graphs of documents.",
    )

    relationships: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Relationships between this document and other documents. Useful for constructing graphs of documents.",
    )

    create_time: Optional[str] = Field(
        default_factory=lambda: str(pd.Timestamp.now()),
        description="The time of creation of the document.",
    )

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "text": "Hello World!",
                "doc_id": "doc1",
                "children": [],
                "coordinate": {},
                "umap_embeddings": [],
                "cluster_label": 0,
                "n_neighbors": 1,
                "relationships": {},
                "sub_graph": {},
            }
        }

    @classmethod
    def from_text(cls, text: str, doc_id: Optional[str] = None) -> "ChainDocument":
        """Create a document from text."""
        return cls(text=text, doc_id=doc_id)

    @classmethod
    def from_dataframe(
        cls, df: pd.DataFrame, doc_id: Optional[str] = None
    ) -> "ChainDocument":
        """Create a document from a dataframe."""
        return cls(text=df.to_dict(), doc_id=doc_id)


class ChainDocumentStore(BaseModel):
    """Document store."""

    docs: Dict[str, ChainDocument] = Field(
        default_factory=dict,
        description="The documents in the document store.",
    )

    relationships: Dict[str, NodeRelationship] = Field(
        default_factory=dict,
        description="The relationships between documents in the document store.",
    )

    @classmethod
    def get_value(
        cls, data: Dict, key: str, expected_type: Union[Type, Any], default=None
    ) -> Any:
        """Helper function to get a value from a dictionary, with error handling."""
        value = data.get(key, default)
        if value is not None and not isinstance(value, expected_type):
            raise TypeError(
                f"Expected type {expected_type} for key {key}, but got type {type(value)}"
            )
        return value

    @classmethod
    def from_dict(cls, data: Dict) -> "ChainDocumentStore":
        """Create a ChainDocumentStore from a dictionary."""
        docs = {}
        for doc_id, doc_data in data.items():
            text = cls.get_value(doc_data, "text", str)
            doc = ChainDocument(text=text, doc_id=doc_id)
            doc.children = []
            doc.coordinate = cls.get_value(doc_data, "coordinate", object)
            doc.n_neighbors = cls.get_value(doc_data, "n_neighbors", int)
            doc.sub_graph = cls.get_value(doc_data, "sub_graph", dict)
            doc.cluster_label = cls.get_value(doc_data, "cluster_label", int)
            doc.umap_embeddings = cls.get_value(doc_data, "umap_embeddings", list)
            doc.relationships = cls.get_value(doc_data, "relationships", dict)
            children = cls.get_value(doc_data, "children", list)
            for child in children:
                doc.children.append(child)
            docs[doc_id] = doc

        obj = cls()
        obj.docs = docs
        return obj

    @classmethod
    def from_csv(
        cls, csv_path: str, doc_id_col: str, text_col: str
    ) -> "ChainDocumentStore":
        """Create a ChainDocumentStore from a CSV file."""
        df = pd.read_csv(csv_path)
        docs = {}
        for _, row in df.iterrows():
            doc_id = row[doc_id_col]
            text = row[text_col]
            doc = ChainDocument(text=text, doc_id=doc_id)
            doc.children = []
            docs[doc_id] = doc

        obj = cls()
        obj.docs = docs
        return obj

    @classmethod
    def from_mongo(cls, mongo_client, db: str, collection: str) -> "ChainDocumentStore":
        """Create a ChainDocumentStore from a MongoDB collection."""
        docs = {}
        for doc in mongo_client[db][collection].find():
            doc_id = doc["_id"]
            text = doc["text"]
            doc = ChainDocument(text=text, doc_id=doc_id)
            doc.children = []
            docs[doc_id] = doc

        obj = cls()
        obj.docs = docs
        return obj

    @classmethod
    def from_sqlite(
        cls, db_path: str, table: str, doc_id_col: str, text_col: str
    ) -> "ChainDocumentStore":
        """Create a ChainDocumentStore from a SQLite table."""
        conn = sqlite3.connect(db_path)
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        docs = {}
        for _, row in df.iterrows():
            doc_id = row[doc_id_col]
            text = row[text_col]
            doc = ChainDocument(text=text, doc_id=doc_id)
            doc.children = []
            docs[doc_id] = doc

        obj = cls()
        obj.docs = docs
        return obj

    @classmethod
    def from_jsonl(cls, jsonl_path: str) -> "ChainDocumentStore":
        """Create a ChainDocumentStore from a JSONL file."""
        docs = {}
        with open(jsonl_path, "r") as f:
            for line in f:
                doc = json.loads(line)
                doc_id = doc["doc_id"]
                text = doc["text"]
                doc = ChainDocument(text=text, doc_id=doc_id)
                doc.children = []
                docs[doc_id] = doc

        obj = cls()
        obj.docs = docs
        return obj

    @classmethod
    def from_documents(cls, docs: List[ChainDocument]) -> "ChainDocumentStore":
        """Create from documents."""
        obj = cls()
        obj.add_documents(docs)
        return obj

    def get_new_id(self) -> str:
        """Get a new ID."""
        return get_new_id(set(self.docs.keys()))

    def update_docstore(self, other: "ChainDocumentStore") -> None:
        """Update docstore."""
        self.docs.update(other.docs)

    def write_documents(self, docs: List[ChainDocument]) -> None:
        """Write documents to the store."""
        self.add_documents(docs)

    def get_all_documents(self) -> List[ChainDocument]:
        """Get all documents."""
        return list(self.docs.values())

    def add_documents(
        self, docs: List[ChainDocument], generate_id: bool = False
    ) -> None:
        """Add a document to the store.

        If generate_id = True, then generate id for doc if doc_id doesn't exist.

        """
        for doc in docs:
            if doc.doc_id is None and generate_id:
                doc.doc_id = self.get_new_id()
            self.docs[doc.doc_id] = doc

    def __len__(self) -> int:
        """Get length."""
        return len(self.docs.keys())

    def delete_document(
        self, doc_id: str, raise_error: bool = True
    ) -> Optional[ChainDocument]:
        """Delete a document from the store."""
        doc = self.docs.pop(doc_id, None)
        if doc is None and raise_error:
            raise ValueError(f"doc_id {doc_id} not found.")
        return doc

    def get_document(
        self, doc_id: str, raise_error: bool = True
    ) -> Optional[ChainDocument]:
        """Get a document from the store."""
        doc = self.docs.get(doc_id, None)
        if doc is None and raise_error:
            raise ValueError(f"doc_id {doc_id} not found.")
        return doc

    def get_document_by_text(
        self, text: str, raise_error: bool = True
    ) -> Optional[ChainDocument]:
        """Get a document from the store."""
        for doc in self.docs.values():
            if doc.text == text:
                return doc
        if raise_error:
            raise ValueError(f"text {text} not found.")
        return None

    def get_document_by_embedding(
        self, embedding: List[float], raise_error: bool = True
    ) -> Optional[ChainDocument]:
        """Get a document from the store."""
        for doc in self.docs.values():
            if doc.embedding == embedding:
                return doc
        if raise_error:
            raise ValueError(f"embedding {embedding} not found.")
        return None

    def get_document_by_umap_embedding(
        self, umap_embedding: List[float], raise_error: bool = True
    ) -> Optional[ChainDocument]:
        """Get a document from the store."""
        for doc in self.docs.values():
            if doc.umap_embeddings == umap_embedding:
                return doc
        if raise_error:
            raise ValueError(f"umap_embedding {umap_embedding} not found.")
        return None

    def get_document_by_coordinate(
        self, coordinate: Dict[str, float], raise_error: bool = True
    ) -> Optional[ChainDocument]:
        """Get a document from the store."""
        for doc in self.docs.values():
            if doc.coordinate == coordinate:
                return doc
        if raise_error:
            raise ValueError(f"coordinate {coordinate} not found.")
        return None

    def get_documents(
        self, doc_ids: List[str], raise_error: bool = True
    ) -> List[ChainDocument]:
        """Get a list of documents from the store."""
        docs = []
        for doc_id in doc_ids:
            doc = self.docs.get(doc_id, None)
            if doc is None and raise_error:
                raise ValueError(f"doc_id {doc_id} not found.")
            docs.append(doc)
        return docs

    def to_dict(self) -> Dict[str, Any]:
        """Convert the document store to a dictionary."""
        return {doc_id: doc.dict() for doc_id, doc in self.docs.items()}

    def to_dataframe(self) -> pd.DataFrame:
        """Convert the document store to a dataframe."""
        return pd.DataFrame.from_dict(self.to_dict(), orient="index")


class TimeSeriesChainDocument(ChainDocumentStore):
    docs: List[ChainDocument] = []

    def __init__(self, docs: List[ChainDocument] = []) -> None:
        """Initialize."""
        self.docs = docs

    def add_document(self, doc: ChainDocument) -> None:
        """Add a document."""
        self.docs.append(doc)

    def add_documents(self, docs: List[ChainDocument]) -> None:
        """Add a list of documents."""
        self.docs.extend(docs)

    def get_all_documents(self) -> List[ChainDocument]:
        """Get all documents."""
        return self.docs

    def __iter__(self) -> Iterator[ChainDocument]:
        """Iterate over documents."""
        return iter(self.docs)

    def __len__(self) -> int:
        """Get length."""
        return len(self.docs)

    def __getitem__(self, index: int) -> ChainDocument:
        """Get item."""
        return self.docs[index]

    def __setitem__(self, index: int, value: ChainDocument) -> None:
        """Set item."""
        self.docs[index] = value

    def __delitem__(self, index: int) -> None:
        """Delete item."""
        del self.docs[index]

    def __contains__(self, item: ChainDocument) -> bool:
        """Check if item is in docs."""
        return item in self.docs

    def __add__(self, other: "TimeSeriesChainDocument") -> "TimeSeriesChainDocument":
        """Add two TimeSeriesChainDocument objects."""
        return TimeSeriesChainDocument(self.docs + other.docs)

    def __iadd__(self, other: "TimeSeriesChainDocument") -> "TimeSeriesChainDocument":
        """Add two TimeSeriesChainDocument objects."""
        self.docs += other.docs
        return self

    def create_representation(self) -> List[Dict[str, Any]]:
        """
        Creates a list of messages ordered by their creation time:

        [
            {
                "create_time": <create time>,
                "message": {
                    "text": <message text>,
                    "id": <message id>,
                    "author": <message author>
                }

            },

            ...

        ]

        """

        return [
            {
                "create_time": doc.create_time,
                "message": {"text": doc.text, "id": doc.id_, "author": doc.author},
            }
            for doc in self.docs
        ]

    def create_representation_with_embeddings(self) -> List[Dict[str, Any]]:
        """
        Creates a list of messages ordered by their creation time:

        [
            {
                "create_time": <create time>,
                "message": {
                    "text": <message text>,
                    "id": <message id>,
                    "author": <message author>,
                    "embedding": <message embedding>
                }

            },

            ...

        ]

        """

        return [
            {
                "create_time": doc.create_time,
                "message": {
                    "text": doc.text,
                    "id": doc.id_,
                    "author": doc.author,
                    "embedding": doc.embedding,
                },
            }
            for doc in self.docs
        ]

    def get_document_by_id(
        self, doc_id: str, raise_error: bool = True
    ) -> Optional[ChainDocument]:
        """Get a document from the store."""
        for doc in self.docs:
            if doc.id_ == doc_id:
                return doc
        if raise_error:
            raise ValueError(f"doc_id {doc_id} not found.")
        return None
