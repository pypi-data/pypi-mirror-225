from typing import List, Tuple, TypeVar, Optional, Dict, Any, Type
from dl_matrix.base import IChainFactory, Coordinate, Content, Chain, IChainTree
from dl_matrix.type import NodeRelationship
from concurrent.futures import ProcessPoolExecutor
from abc import ABC, ABCMeta, abstractmethod
from uuid import uuid4
from datetime import datetime
import hashlib
import weakref
import numpy as np
import os

T = TypeVar("T")


class IdDescriptor:
    _ids = set()

    def __get__(self, instance, owner):
        return instance.__dict__["_id"]

    def __set__(self, instance, value):
        if value in self._ids:
            raise ValueError(f"Id '{value}' is already in use.")
        self._ids.add(value)
        instance.__dict__["_id"] = value

    def __delete__(self, instance):
        self._ids.remove(instance.__dict__["_id"])
        del instance.__dict__["_id"]

    def generate_id(self) -> str:
        return str(uuid4())


class TimestampMeta(type):
    def __new__(cls, name, bases, dct):
        dct["timestamp"] = datetime.utcnow()
        return super().__new__(cls, name, bases, dct)


class CombinedMeta(TimestampMeta, ABCMeta):
    pass


class NodeComponent(ABC):
    def __init__(self):
        self.parent = None
        self.children = []

    @abstractmethod
    def accept(self, visitor):
        pass

    @abstractmethod
    def get_ancestors(self) -> List["NodeComponent"]:
        pass

    @abstractmethod
    def get_descendants(self) -> List["NodeComponent"]:
        pass

    def set_parent(self, parent: "NodeComponent"):
        self.parent = parent

    def get_parent(self) -> Optional["NodeComponent"]:
        return self.parent

    def add_child(self, child: "NodeComponent"):
        self.children.append(child)

    def get_children(self) -> List["NodeComponent"]:
        return self.children.copy()

    def remove_child(self, child: "NodeComponent"):
        self.children.remove(child)

    def is_last_child(self, child: "NodeComponent") -> bool:
        return child == self.children[-1]

    def is_first_child(self, child: "NodeComponent") -> bool:
        return child == self.children[0]


class MetadataScheme(ABC):
    @abstractmethod
    def generate_metadata(self, data: Any) -> Type[T]:
        pass

    @abstractmethod
    def verify_metadata(self, data: Any, metadata: Type[T]) -> bool:
        pass


class SignatureScheme(ABC):
    @abstractmethod
    def generate_signature(self, data: Any) -> Type[T]:
        pass

    @abstractmethod
    def verify_signature(self, data: Any, signature: Type[T]) -> bool:
        pass


class SimpleMetadataScheme(MetadataScheme):
    def generate_metadata(self, data: Any) -> str:
        return f"Metadata for {data}"

    def verify_metadata(self, data: Any, metadata: str) -> bool:
        return metadata == f"Metadata for {data}"


class SHA256SignatureScheme(SignatureScheme):
    def generate_signature(self, content_node: Any) -> str:
        return hashlib.sha256(str(content_node).encode()).hexdigest()

    def verify_signature(self, data: Any, signature: str) -> bool:
        return hashlib.sha256(str(data).encode()).hexdigest() == signature


class ChainLink:
    """
    Represents a chain in the ChainTree data structure.
    Each chain is rooted at a node with a specific key and contains all nodes whose key is a prefix of that key.
    """

    def __init__(self, root_node: NodeComponent) -> None:
        self.root_node = root_node
        self.root = root_node

    def get_chain(self) -> List[NodeComponent]:
        # using get_descendants() method of NodeComposite
        # to get all descendants of the root node
        return self.root_node.get_descendants()

    def get_chain_keys(self) -> List[str]:
        # gets keys of all nodes in the chain
        return [node.key for node in self.get_chain()]

    def get_chain_values(self) -> List[Any]:
        # gets values of all nodes in the chain
        return [node.value for node in self.get_chain()]

    def print_chain(self):
        # printing the chain
        print(f"Chain Root: {self.root_node.key}")
        print("Chain Nodes:")
        for node in self.get_chain():
            print(f"Node Key: {node.key}, Node Value: {node.value}")


class NodeComposite(NodeComponent):
    lookup_table = (
        weakref.WeakValueDictionary()
    )  # Use a weak value dictionary to store nodes by their hashes

    def __init__(self, key: Optional[Type] = None, value: Optional[Type] = None):
        self.children = np.array([], dtype=object)
        self.children_hashes = np.array([], dtype=object)
        self.key = key
        self.value = value
        self.id = self._hash_node(self)
        self.left = None
        self.right = None

    def add_child(self, child: NodeComponent):
        if child == self:
            raise ValueError("Cannot add the node as its own child.")
        if child in self.children:
            raise ValueError(f"Child with id '{child.id}' is already added.")
        self.children = np.append(self.children, child)
        child_hash = self._hash_node(child)
        self.children_hashes = np.append(self.children_hashes, child_hash)
        self.lookup_table[child_hash] = child
        print(f"Added child with id '{child}' to node with id '{self}'.")

    def remove_child(self, child: NodeComponent):
        if child not in self.children:
            raise ValueError(f"Child with id '{child.id}' not found.")
        child_idx = np.where(self.children == child)[0][0]
        child_hash = self.children_hashes[child_idx]
        self.children = np.delete(self.children, child_idx)
        self.children_hashes = np.delete(self.children_hashes, child_idx)
        del self.lookup_table[child_hash]

    def _get_child_index(self, child: NodeComponent) -> int:
        if child not in self.children:
            raise ValueError
        return np.where(self.children == child)[0][0]

    def _get_child_hash(self, child: NodeComponent) -> str:
        if child not in self.children:
            raise ValueError
        return self.children_hashes[self._get_child_index(child)]

    def _hash_node(self, node: NodeComponent) -> str:
        signature_scheme = SHA256SignatureScheme()
        return signature_scheme.generate_signature(node)

    def get_child_by_hash(self, node_hash: str) -> Optional[NodeComponent]:
        return self.lookup_table.get(node_hash)

    def get_parent_by_hash(self, node_hash: str) -> Optional[NodeComponent]:
        for node in self.lookup_table.values():
            if isinstance(node, NodeComposite) and node_hash in node.children_hashes:
                return node
        return None

    def get_node_by_hash(self, content_hash: str) -> Optional[NodeComponent]:
        return self.lookup_table.get(content_hash)

    def get_child_by_index(self, index: int) -> NodeComponent:
        return self.children[index]

    def get_child_by_key(self, key: str) -> NodeComponent:
        for child in self.children:
            if child.key == key:
                return child
        raise ValueError(f"Child with key '{key}' not found.")

    def get_child_by_value(self, value: Any) -> NodeComponent:
        for child in self.children:
            if child.value == value:
                return child
        raise ValueError(f"Child with value '{value}' not found.")

    def clear_children(self):
        self.children = np.array([], dtype=object)
        self.children_hashes = np.array([], dtype=object)
        self.lookup_table.clear()

    def generate_chain(self) -> Chain:
        return Chain(self)

    def accept(self, visitor):
        visitor.visit_composite(self)

    def max_children(self) -> int:
        return 2

    def get_ancestors(self) -> List[NodeComponent]:
        ancestors = []
        if not self.parent:
            return ancestors
        ancestors.append(self.parent)
        if isinstance(self.parent, NodeComposite):
            ancestors.extend(self.parent.get_ancestors())
        return ancestors

    def get_descendants(self) -> List[NodeComponent]:
        descendants = []
        for child in self.children:
            descendants.append(child)
            if isinstance(child, NodeComposite):
                descendants.extend(child.get_descendants())
        return descendants


class BaseNode(NodeComponent, metaclass=CombinedMeta):
    id = IdDescriptor().generate_id()

    def __init__(
        self,
        id: Type[T],
        content: Type[T],
        signature_scheme: SignatureScheme,
        metadata_scheme: MetadataScheme,
        label: Optional[str] = None,
    ):
        self.id = id
        self.content = content
        self.label = label
        self.signature_scheme = signature_scheme
        self.metadata_scheme = metadata_scheme
        self.signature = signature_scheme.generate_signature(content)
        self.metadata = metadata_scheme.generate_metadata(content)

    def verify_signature(self) -> bool:
        return self.signature_scheme.verify_signature(self.content, self.signature)

    def verify_metadata(self) -> bool:
        return self.metadata_scheme.verify_metadata(self.content, self.metadata)

    def accept(self, visitor: "NodeVisitor"):
        visitor.visit_leaf(self)

    def get_ancestors(self) -> List[NodeComponent]:
        ancestors = []
        if not self.parent:
            return ancestors
        ancestors.append(self.parent)
        if isinstance(self.parent, NodeComposite):
            ancestors.extend(self.parent.get_ancestors())
        return ancestors

    def get_descendants(self) -> List[NodeComponent]:
        descendants = []
        for child in self.children:
            descendants.append(child)
            if isinstance(child, NodeComposite):
                descendants.extend(child.get_descendants())
        return descendants

    def __str__(self):
        return f"Node(id={self.id}"


class InternalNode(NodeComposite, BaseNode):
    def __init__(
        self,
        id: Type[T],
        content: Type[T],
        signature_scheme: SignatureScheme,
        metadata_scheme: MetadataScheme,
    ):
        super().__init__()
        BaseNode.__init__(self, id, content, signature_scheme, metadata_scheme)
        parent = None

    def accept(self, visitor: "NodeVisitor"):
        visitor.visit_composite(self)


class LeafNode(BaseNode):
    def __init__(
        self,
        id: Type[T],
        content: Type[T],
        signature_scheme: SignatureScheme,
        metadata_scheme: MetadataScheme,
    ):
        super().__init__(id, content, signature_scheme, metadata_scheme)
        self.parent = None
        self.children = []

    def accept(self, visitor: "NodeVisitor"):
        visitor.visit_leaf(self)


class NodeFactory:
    @staticmethod
    def create_leaf_node(
        id: Type[T],
        content: Type[T],
        signature_scheme: SignatureScheme = SHA256SignatureScheme(),
        metadata_scheme: MetadataScheme = SimpleMetadataScheme(),
    ) -> LeafNode:
        return LeafNode(id, content, signature_scheme, metadata_scheme)

    @staticmethod
    def create_internal_node(
        id: Type[T],
        content: Type[T],
        signature_scheme: SignatureScheme = SHA256SignatureScheme(),
        metadata_scheme: MetadataScheme = SimpleMetadataScheme(),
    ) -> InternalNode:
        return InternalNode(id, content, signature_scheme, metadata_scheme)

    @staticmethod
    def create_node(
        id: Type[T],
        content: Type[T],
        signature_scheme: SignatureScheme = SHA256SignatureScheme(),
        metadata_scheme: MetadataScheme = SimpleMetadataScheme(),
    ) -> NodeComponent:
        if isinstance(content, str):
            return NodeFactory.create_leaf_node(
                id, content, signature_scheme, metadata_scheme
            )
        return NodeFactory.create_internal_node(
            id, content, signature_scheme, metadata_scheme
        )


class NodeVisitor(ABC):
    @abstractmethod
    def visit_leaf(self, node: "LeafNode"):
        pass

    @abstractmethod
    def visit_composite(self, node: "InternalNode"):
        pass


class NodePrinter(NodeVisitor):
    def visit_leaf(self, node: LeafNode):
        print(
            f"Leaf node with id {node.id} and content {node.content} was created at {node.timestamp}"
        )

    def visit_composite(self, node: InternalNode):
        print(
            f"Composite node with id {node.id} and content {node.content} was created at {node.timestamp}"
        )
        for child in node.get_children():
            child.accept(self)

    def pirnt_tree_structure(self, node: NodeComponent):
        node.accept(self)
        # print hierarchy of the tree structure use -- for each level
        for child in node.get_children():
            print("--", end="")
            for ancestor in child.get_ancestors():
                print("--", end="")

            self.pirnt_tree_structure(child)


class NodeVerifier(NodeVisitor):
    def visit_leaf(self, node: LeafNode):
        print(
            f"Leaf node with id {node.id} and content {node.content} has valid signature {node.verify_signature()} and valid metadata {node.verify_metadata()}"
        )

    def visit_composite(self, node: InternalNode):
        print(
            f"Composite node with id {node.id} and content {node.content} has valid signature {node.verify_signature()} and valid metadata {node.verify_metadata()}"
        )
        for child in node.get_children():
            child.accept(self)

    def verify_tree_structure(self, node: NodeComponent):
        node.accept(self)
        for child in node.get_children():
            self.verify_tree_structure(child)


class ChainTreeLink(IChainTree):
    """
    Represents a ChainTree data structure.
    """

    def __init__(
        self,
        chain_factory: IChainFactory,
        allow_duplicates: bool = False,
    ):
        self.chain_factory = chain_factory
        self.allow_duplicates = allow_duplicates
        self.chains_links = {}
        self.chains = []
        self.nodes = []
        self.chain_tree_ds = {
            "nodes": [],
            "links": [],
            "root": None,
            "leafs": [],
            "internal_nodes": [],
        }

        self.prompt_map = {
            relationship: (relationship, relationship)
            for relationship in NodeRelationship
        }

        self.relationships = []

    def add_chain(
        self,
        chain_type: str,
        id: str,
        content: Content,
        coordinate: Coordinate,
        parent: Optional[str] = None,
    ) -> None:
        """
        Adds a chain to the ChainTree.
        """
        if not self.allow_duplicates and id in self.chains:
            raise ValueError(f"Duplicate id {id} found in sequence.")

        chain = self.chain_factory.create_chain(
            chain_type, id, content, coordinate, parent
        )
        self.chains.append(chain)

        # Add the chain to the chain with the same id
        if id not in self.chains_links:
            self.chains_links[id] = ChainLink(chain)
        else:
            self.chains_links[id].root_node.add_child(chain)

        # Add the chain to the chains with ids that are prefixes of the chain's id
        for i in range(1, len(id)):
            prefix = id[:i]
            if prefix not in self.chains_links:
                self.chains_links[prefix] = ChainLink(chain)
            else:
                self.chains_links[prefix].root_node.add_child(chain)

    def update_chain(
        self,
        id: str,
        new_content: Optional[Content] = None,
        new_coordinate: Optional[Coordinate] = None,
        new_metadata: Optional[Dict[str, Any]] = None,
    ):
        for chain in self.chains:
            if chain.id == id:
                if new_content is not None:
                    chain.content = new_content
                if new_coordinate is not None:
                    chain.coordinate = new_coordinate
                if new_metadata is not None:
                    chain.metadata = new_metadata
                break

    def add_node(self, key: str, value: int) -> None:
        """
        Adds a node to the ChainTree.
        """
        if not self.allow_duplicates and key in self.chains:
            raise ValueError(f"Duplicate key {key} found in sequence.")

        node = NodeFactory.create_node(key, value)
        # Add the node to the chain with the same key
        if key not in self.chains_links:
            self.chains_links[key] = ChainLink(node)
        else:
            self.chains_links[key].root.add_child(node)

        # Add the node to the chains with keys that are prefixes of the node's key
        for i in range(1, len(key)):
            prefix = key[:i]
            if prefix not in self.chains_links:
                self.chains_links[prefix] = ChainLink(node)
            else:
                self.chains_links[prefix].root.add_child(node)

    def remove_node(self, key: str) -> None:
        """
        Removes a node from the ChainTree.
        """
        node_to_remove = None
        for node in self.nodes:
            if node.key == key:
                node_to_remove = node
                break

        if node_to_remove is None:
            raise ValueError(f"Node with key {key} not found.")

        # Remove the node from the chains with keys that are prefixes of the node's key
        for i in range(len(key)):
            prefix = key[:i]
            if prefix in self.chains_links:
                self.chains_links[prefix].root.remove_child(node_to_remove)

        self.nodes.remove(node_to_remove)

    def accept(self, visitor: NodeVisitor):
        for chain in self.chains.values():
            chain.root.accept(visitor)

    def print_tree_structure(self):
        for chain in self.chains.values():
            NodePrinter().pirnt_tree_structure(chain.root)

    def verify_tree_structure(self):
        for chain in self.chains.values():
            NodeVerifier().verify_tree_structure(chain.root)

    def get_chains_by_coordinate(self, coordinate: Coordinate):
        return [chain for chain in self.chains if chain.coordinate == coordinate]

    def get_chains(self):
        return self.chains

    def get_chain(self, id: str):
        for chain in self.chains:
            if chain.id == id:
                return chain
        return None

    def get_last_chain(self):
        return self.chains[-1]

    def remove_chain(self, id: str):
        self.chains = [chain for chain in self.chains if chain.id != id]

    def add_nodes(self, nodes: List[Tuple[str, int]]) -> None:
        """
        Adds multiple nodes to the ChainTree.
        """
        for node in nodes:
            self.add_node(node[0], node[1])

    def remove_nodes(self, keys: List[str]) -> None:
        """
        Removes multiple nodes from the ChainTree.
        """
        for key in keys:
            self.remove_node(key)

    def get_nodes(self) -> List[NodeComposite]:
        """
        Gets all nodes from the ChainTree.
        """
        return self.nodes

    def get_node(self, key: str) -> NodeComposite:
        """
        Gets a node from the ChainTree.
        """
        if key not in self.chains_links:
            raise ValueError(f"Key {key} not found in sequence.")

        return self.chains_links[key].root

    def _traverse(self, node: NodeComposite, indent: str = "") -> List[str]:
        """
        Helper method for __str__ that recursively traverses the ChainTree and generates a list of strings
        representing the nodes and their relationships in the tree.
        """
        lines = [f"{indent}{node.key}: {node.value}"]
        for child in node.children:
            lines.extend(self._traverse(child, indent + "  "))
        return lines

    def get_chains_by_type(self, chain_type: str):
        return [
            chain for chain in self.chains if isinstance or chain.entity == chain_type
        ]

    def _traverse_chain(
        self, node: NodeComposite, visited: set
    ) -> List[Tuple[str, str]]:
        """
        Helper method for create_partial_sequence_as_simplicial_complex that recursively traverses the ChainTree
        and generates a list of tuples representing the simplicial complex.
        """
        simplicial_complex = []
        for child in node.children:
            simplicial_complex.append((node.key, child.key))
            simplicial_complex.extend(self._traverse_chain(child, visited))
        return simplicial_complex

    def create_chain_tree(
        self,
        partial_sequences: List[List[Tuple[str, int]]],
        parallel: bool = False,
        num_workers: Optional[int] = None,
        use_nested_tree_structure: bool = False,
    ) -> Dict[str, Any]:
        """
        Generate a chain tree from the given partial sequences. It can process the sequences either in parallel or sequentially based on the flag passed.
        Also, it can use a nested tree structure if use_nested_tree_structure is True.
        """
        if not isinstance(partial_sequences, list) or not all(
            isinstance(i, list) for i in partial_sequences
        ):
            raise ValueError("Partial sequences should be a list of lists")
        if not all(
            isinstance(i, tuple) and len(i) == 2
            for sublist in partial_sequences
            for i in sublist
        ):
            raise ValueError(
                "Each item in the partial sequences should be a tuple of length 2"
            )

        if use_nested_tree_structure:
            chain_tree = {"type": "branch", "children": []}
            if parallel:
                num_workers = num_workers or min(
                    len(partial_sequences), os.cpu_count() or 1
                )
                with ProcessPoolExecutor(max_workers=num_workers) as executor:
                    executor.map(
                        self.insert_sequence_into_tree, chain_tree, partial_sequences
                    )
            else:
                for partial_sequence in partial_sequences:
                    self.insert_sequence_into_tree(chain_tree, partial_sequence)
            return chain_tree
        else:
            chain_tree = {"type": "branch", "children": []}
            if parallel:
                num_workers = num_workers or min(
                    len(partial_sequences), os.cpu_count() or 1
                )
                with ProcessPoolExecutor(max_workers=num_workers) as executor:
                    executor.map(
                        self.insert_sequence_into_tree, chain_tree, partial_sequences
                    )
            else:
                for partial_sequence in partial_sequences:
                    self.insert_sequence_into_tree(chain_tree, partial_sequence)
            return chain_tree

    def insert_sequence_into_tree(
        self, chain_tree: Dict[str, Any], partial_sequence: List[Tuple[str, int]]
    ) -> None:
        """
        Insert a partial sequence into the chain tree.
        """
        current_node = chain_tree
        for i, leaf in enumerate(partial_sequence):
            if leaf[0] not in current_node:
                if i == len(partial_sequence) - 1:
                    current_node[leaf[0]] = leaf[1]
                else:
                    current_node[leaf[0]] = {"type": "branch", "children": {}}
            current_node = current_node[leaf[0]]

    def flatten_chain_tree(
        self,
        tree: Dict[str, Any],
        nodes: List[Dict[str, Any]],
        links: List[Dict[str, Any]],
        leafs: List[int],
        internal_nodes: List[int],
    ) -> None:
        if tree["type"] == "branch":
            for child in tree["children"]:
                if child["type"] == "branch":
                    internal_nodes.append(id(child))
                elif child["type"] == "leaf":
                    leafs.append(id(child))
                nodes.append(
                    {"id": id(child), "key": child["key"], "type": child["type"]}
                )
                links.append({"source": id(tree), "target": id(child)})
                self.flatten_chain_tree(child, nodes, links, leafs, internal_nodes)

    def add_leaf_to_tree(self, branch: Dict[str, Any], leaf: Tuple[str, int]) -> None:
        leaf_node = {
            "type": "leaf",
            "key": leaf[0],
            "level": leaf[1],
            "children": [],
        }
        branch["children"].append(leaf_node)
        branch_id = id(branch)
        leaf_id = id(leaf_node)
        self.chain_tree_ds["nodes"].append(
            {"id": leaf_id, "key": leaf_node["key"], "type": "leaf"}
        )
        self.chain_tree_ds["links"].append({"source": branch_id, "target": leaf_id})
        self.chain_tree_ds["leafs"].append(leaf_id)
        self.chain_tree_ds["internal_nodes"].append(branch_id)

    def add_chain_to_tree(self, chain: Chain) -> None:
        """
        Adds a chain to the ChainTree.
        """
        if not self.allow_duplicates and chain.id in self.chains:
            raise ValueError(f"Duplicate key {chain.id} found in sequence.")

        self.chains.append(chain)
        self.chains_links[chain.id] = chain

        # Add the chain to the chain with the same key
        if chain.id not in self.chains_links:
            self.chains_links[chain.id] = ChainLink(chain)
        else:
            self.chains_links[chain.id].root.add_child(chain)

        # Add the chain to the chains with keys that are prefixes of the chain's key
        for i in range(1, len(chain.id)):
            prefix = chain.id[:i]
            if prefix not in self.chains_links:
                self.chains_links[prefix] = ChainLink(chain)
            else:
                self.chains_links[prefix].root.add_child(chain)

    class Config:
        schema_extra = {
            "example": {
                "nodes": [
                    {
                        "content": {
                            "content_type": "text",
                            "parts": ["Hello World!"],
                            "emmbeddings": [0.1, 0.2, 0.3],
                            "metadata": {"key": "value"},
                        },
                        "coordinate": {
                            "x": 0.1,
                            "y": 0.2,
                            "z": 0.3,
                        },
                        "metadata": {"key": "value"},
                    },
                    {
                        "content": {
                            "content_type": "text",
                            "parts": ["Hello World!"],
                            "emmbeddings": [0.1, 0.2, 0.3],
                            "metadata": {"key": "value"},
                        },
                        "coordinate": {
                            "x": 0.1,
                            "y": 0.2,
                            "z": 0.3,
                        },
                        "metadata": {"key": "value"},
                    },
                ],
                "relationships": [
                    {
                        "node": {
                            "content": {
                                "content_type": "text",
                                "parts": ["Hello World!"],
                                "emmbeddings": [0.1, 0.2, 0.3],
                                "metadata": {"key": "value"},
                            },
                            "coordinate": {
                                "x": 0.1,
                                "y": 0.2,
                                "z": 0.3,
                            },
                            "metadata": {"key": "value"},
                        },
                        "metadata": {"key": "value"},
                    },
                    {
                        "node": {
                            "content": {
                                "content_type": "text",
                                "parts": ["Hello World!"],
                                "emmbeddings": [0.1, 0.2, 0.3],
                                "metadata": {"key": "value"},
                            },
                            "coordinate": {
                                "x": 0.1,
                                "y": 0.2,
                                "z": 0.3,
                            },
                            "metadata": {"key": "value"},
                        },
                        "metadata": {"key": "value"},
                    },
                ],
                "metadata": {"key": "value"},
            }
        }

    def dict(self, *args, **kwargs):
        return super().dict(*args, **kwargs)
