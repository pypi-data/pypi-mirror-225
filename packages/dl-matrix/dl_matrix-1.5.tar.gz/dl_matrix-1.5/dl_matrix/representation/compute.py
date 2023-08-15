from typing import Dict, Tuple, Any, Optional, List, Union, TypeVar
from dl_matrix.models import ChainTreeIndex, ChainMap
from dl_matrix.coordinate import Coordinate
from dl_matrix.models import ChainDocument
from dl_matrix.type import NodeRelationship
from dl_matrix.representation.base import Representation
from dl_matrix.representation.estimator import Estimator
from dl_matrix.representation.handler import ChainHandler
import plotly.graph_objects as go
from collections import defaultdict
from networkx.readwrite import json_graph
import plotly.express as px
import logging
import networkx as nx
import numpy as np

T = TypeVar("T")  # TypeVar for generalizing the function returns


class CoordinateRepresentation(Representation):
    RELATIONSHIP_WEIGHTS = {
        "siblings": 1,
        "cousins": 2,
        "uncles_aunts": 3,
        "nephews_nieces": 3,
        "grandparents": 4,
        "ancestors": 5,
        "descendants": 5,
        NodeRelationship.PARENT: 1,
        NodeRelationship.CHILD: 1,
        NodeRelationship.PREVIOUS: 1,
        NodeRelationship.NEXT: 1,
        NodeRelationship.SOURCE: 1,
    }

    def __init__(
        self,
        conversation_tree: ChainTreeIndex,
        message_dict: Optional[Dict[str, Coordinate if Coordinate else Any]] = None,
        conversation_dict: Optional[
            Dict[str, Coordinate if Coordinate else Any]
        ] = None,
    ):
        super().__init__(conversation_tree)
        self.message_dict = (
            self._message_representation() if message_dict is None else message_dict
        )
        self.conversation_dict = (
            self._conversation_representation()
            if conversation_dict is None
            else conversation_dict
        )
        self.estimator = Estimator(self.message_dict, self.conversation_dict)

        self.handler = ChainHandler()

    def count_system_messages(self):
        system_message_count = sum(
            1
            for msg in self.message_dict.values()
            if msg.message.author.role == "system"
        )
        return system_message_count

    def _procces_coordnates(
        self,
        use_graph: bool = False,
        local_embedding: bool = True,
        animate: bool = False,
    ) -> Optional[
        Union[Dict[str, Tuple[float, float, float, float, int]], List[ChainMap]]
    ]:
        # Create coordinates and relationships
        tetra_dict, relationships = self._create_coordinates_graph(use_graph)
        if not tetra_dict:
            # skip if no coordinates were created
            return None

        # Animate the conversation tree, if specified
        if animate:
            self.animate_conversation_tree(
                coordinates=list(tetra_dict.values()),
            )

        # Update the coordinates with local embeddings, if specified
        if local_embedding:
            # Generate local embeddings for messages
            message_embeddings = (
                self.handler.semantic_similarity_model.generate_message_embeddings(
                    self.estimator, self.message_dict
                )
            )

            # Update representation with local embeddings
            updated_tree_doc = self._construct_representation(
                message_embeddings, tetra_dict, relationships
            )
            return updated_tree_doc
        else:
            return tetra_dict

    def animate_conversation_tree(
        self, coordinates: List[Coordinate], name: str = "Tree"
    ):
        hovertext = [
            f"Depth: {coord[0]}<br>Sibling: {coord[1]}<br>Sibling Count: {coord[2]}"
            for coord in coordinates
        ]

        rainbow_scale = px.colors.sequential.Rainbow
        system_colors = [
            rainbow_scale[int(i)]
            for i in np.linspace(0, len(rainbow_scale) - 1, len(coordinates))
        ]

        frames = [
            go.Frame(
                data=[
                    go.Scatter3d(
                        x=[coord[0] for coord in coordinates[:i]],  # self.depth.x
                        y=[coord[1] for coord in coordinates[:i]],  # self.sibling.y
                        z=[
                            coord[2] for coord in coordinates[:i]
                        ],  # self.sibling_count.z
                        mode="markers",
                        marker=dict(
                            size=5,
                            color=system_colors[:i],
                            colorscale="rainbow",
                            colorbar=dict(
                                title="Labels",
                                x=-0.1,
                                xanchor="left",
                            ),
                            line=dict(color="powderblue", width=2),
                            opacity=0.9,
                            symbol="circle",
                            sizemode="diameter",
                        ),
                        hoverinfo="text",
                        hovertext=hovertext,
                        name="Coordinates",
                    ),
                    go.Scatter3d(
                        x=[coord[0] for coord in coordinates[:i]],  # self.depth.x
                        y=[coord[1] for coord in coordinates[:i]],  # self.sibling.y
                        z=[
                            coord[2] for coord in coordinates[:i]
                        ],  # self.sibling_count.z
                        mode="lines",
                        line=dict(color="white", width=1),
                        hoverinfo="none",
                    ),
                ]
            )
            for i in range(1, len(coordinates) + 1)
        ]

        fig = go.Figure(
            data=[
                go.Scatter3d(
                    x=[coord[0] for coord in coordinates],  # self.depth.x
                    y=[coord[1] for coord in coordinates],  # self.sibling.y
                    z=[coord[2] for coord in coordinates],  # self.sibling_count.z
                    mode="markers",
                    marker=dict(
                        size=5,
                        color=system_colors,
                        colorscale="rainbow",
                        colorbar=dict(
                            title="Labels",
                            x=-0.1,
                            xanchor="left",
                        ),
                        line=dict(color="powderblue", width=2),
                        opacity=0.9,
                        symbol="circle",
                        sizemode="diameter",
                    ),
                    hoverinfo="text",
                    name="Coordinates",
                ),
                go.Scatter3d(
                    x=[coord[0] for coord in coordinates],  # self.depth.x
                    y=[coord[1] for coord in coordinates],  # self.sibling.y
                    z=[coord[2] for coord in coordinates],  # self.sibling_count.z
                    mode="lines",
                    line=dict(color="white", width=1),
                    hoverinfo="none",
                ),
            ],
            layout=go.Layout(
                title=name,
                scene=dict(
                    xaxis=dict(showbackground=False, gridcolor="Black"),
                    yaxis=dict(showbackground=False, gridcolor="Black"),
                    zaxis=dict(showbackground=False, gridcolor="Black"),
                    camera=dict(
                        up=dict(x=0, y=0, z=1),
                        eye=dict(x=-1.5, y=-1.5, z=1.5),
                        center=dict(x=0, y=0, z=0),
                    ),
                    dragmode="turntable",
                ),
                font_family="Arial",
                font_color="White",
                title_font_family="Arial",
                title_font_color="White",
                legend_title_font_color="White",
                paper_bgcolor="Black",
                plot_bgcolor="Black",
                hoverlabel=dict(bgcolor="Black", font_color="White"),
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        buttons=[
                            dict(
                                label="Play",
                                method="animate",
                                args=[
                                    None,
                                    dict(frame=dict(duration=500, redraw=True)),
                                ],
                            )
                        ],
                    )
                ],
            ),
            frames=frames,
        )
        fig.show()

    def add_node_to_graph(
        self,
        graph: nx.DiGraph,
        message_id: str,
        safe_tetra_dict: Dict[str, Any],
        failed_nodes: List[str],
    ) -> None:
        """
        Attempt to add a node to the graph.

        This function checks if the provided message_id is not already in the graph, if there exists a corresponding
        entry in safe_tetra_dict, and if it hasn't previously failed to be added. If all these conditions pass,
        it attempts to add the node, catching and logging any exceptions that occur in the process.

        Args:
            graph: The current graph.
            message_id: The id of the message.
            failed_nodes: The list of nodes that failed to be added.
        """
        # Validate before attempting to add node
        if (
            message_id not in graph
            and safe_tetra_dict[message_id] is not None
            and message_id not in failed_nodes
        ):
            try:
                graph.add_node(
                    message_id, message=self.message_dict[message_id].message.children
                )
            except Exception as e:
                logging.warning(f"Failed to add node for message {message_id}: {e}")
                failed_nodes.append(message_id)
        else:
            logging.warning(
                f"Invalid conditions for adding node {message_id}. Adding the node anyway."
            )
            graph.add_node(message_id)

    def add_edge_to_graph(
        self,
        graph: nx.DiGraph,
        message_id: str,
        relationship: Dict[str, str],
        failed_edges: List[Tuple[str, str]],
    ):
        """
        Add an edge to the graph if necessary.

        Args:
            graph: The current graph.
            message_id: The id of the message.
            relationship: The relationships of the message.
            failed_edges: The list of edges that failed to be added.
        """
        for relationship_type, relationship_id in relationship.items():
            if (
                relationship_id is not None
                and relationship_id in graph
                and message_id in graph
                and (message_id, relationship_id) not in graph.edges
                and (relationship_id, message_id) not in graph.edges
                and (message_id, relationship_id) not in failed_edges
                and (relationship_id, message_id) not in failed_edges
            ):
                try:
                    graph.add_edge(
                        message_id,
                        relationship_id,
                        relationship_type=relationship_type,
                        weight=self.RELATIONSHIP_WEIGHTS[relationship_type],
                    )
                except Exception as e:
                    logging.warning(
                        f"Failed to add edge between {message_id} and {relationship_id}: {e}"
                    )
                    failed_edges.append((message_id, relationship_id))
                    failed_edges.append((relationship_id, message_id))

    def create_subgraph(self, graph: nx.DiGraph, message_id: str) -> nx.DiGraph:
        """
        Create a subgraph centered at the given message node, which includes all nodes within a radius of 1.

        This method follows the below steps:
        1. Use the `nx.ego_graph` method from the NetworkX package to generate the ego graph (subgraph) of the main graph.
        The ego graph is centered at `message_id` and includes all nodes that are reachable from the center within a
        given radius (1 in this case).
        2. Convert the labels of nodes in the subgraph to integer labels starting from 0, which is a common practice when
        working with graph algorithms since many of them are designed to work with such graphs.

        Args:
            graph: The original graph from which the subgraph will be created.
            message_id: The id of the message at the center of the subgraph.

        Returns:
            The subgraph centered at the given message node, with node labels converted to integers.
        """
        # Check if the node exists in the graph

        if message_id not in graph:
            logging.warning(f"Node {message_id} is not in the graph. Adding the node.")
            graph.add_node(message_id)
            # Add any necessary attributes or relationships for this node if required

        # Generate the ego graph (subgraph) centered at `message_id` and including all nodes within a radius of 1
        subgraph = nx.ego_graph(graph, message_id, radius=1, center=True)

        # Convert the labels of nodes in the subgraph to integer labels starting from 0
        subgraph = nx.convert_node_labels_to_integers(subgraph, first_label=0)

        return subgraph

    def create_chain_document(
        self,
        message_id: str,
        embedding_data: Any,
        tetra_dict: Dict[str, Tuple[float, float, float, float, int]],
        relationship: Dict[str, str],
        subgraph: nx.DiGraph,
    ) -> ChainDocument:
        """
        Create a ChainDocument for a given message id.

        Args:
            message_id: The id of the message.
            embedding_data: The embedding data of the message.
            tetra_dict: The dictionary containing the tetrahedron coordinates.
            relationship: The relationships of the message.
            subgraph: The subgraph of the graph.

        Returns:
            A ChainDocument object for the given message id.
        """
        if message_id not in tetra_dict:
            # skip if message_id is not in tetra_dict
            return None

        sub_graph = json_graph.node_link_data(G=subgraph)
        chain_document_parameters = self.get_chain_document_parameters(
            message_id, embedding_data, tetra_dict[message_id], relationship, sub_graph
        )

        return ChainDocument(**chain_document_parameters)

    def get_chain_document_parameters(
        self, message_id, embedding_data, coordinate, relationship, sub_graph
    ):
        """
        Extract the parameters for a ChainDocument from the given inputs.

        Args:
            message: The message object.
            message_id: The id of the message.
            embedding_data: The embedding data of the message.
            coordinate: The tetrahedron coordinate of the message.
            relationship: The relationships of the message.
            sub_graph: The subgraph of the graph in json format.

        Returns:
            A dictionary containing the parameters for a ChainDocument.
        """
        message_content = self.get_message_content(message_id)
        author_role = self.get_message_author_role(message_id)
        create_time = self.get_message_create_time(message_id)

        return {
            "doc_id": message_id,
            "text": message_content,
            "children": relationship.get(NodeRelationship.CHILD, []),
            "author": author_role,
            "coordinate": coordinate.tolist(),
            "sub_graph": sub_graph,
            "umap_embeddings": embedding_data[0].tolist(),
            "cluster_label": int(embedding_data[1]),
            "embedding": embedding_data[2],
            "n_neighbors": embedding_data[3],
            "relationships": relationship,
            "create_time": create_time,
        }

    def _construct_representation(
        self,
        message_embeddings: Dict[str, Any],
        tetra_dict: Dict[str, Tuple[float, float, float, float, int]],
        relationships: Dict[str, Dict[str, str]],
    ) -> List[ChainDocument]:
        # Initialize a new directed graph
        graph = nx.DiGraph()

        # Create a defaultdict to avoid KeyError exceptions
        safe_relationships = defaultdict(lambda: {}, relationships)
        safe_tetra_dict = defaultdict(lambda: None, tetra_dict)

        # Variables to keep track of failed node and edge additions
        failed_nodes = []
        failed_edges = []
        chain_documents = []

        # Iterate over each message in the conversation
        for message_id, embedding_data in message_embeddings.items():
            # Add a node for each message
            self.add_node_to_graph(graph, message_id, safe_tetra_dict, failed_nodes)

            # Extract and merge relationships
            relationship = safe_relationships[message_id]
            grid_relationships = self.estimator.get_relationship_ids(message_id)
            relationship.update(grid_relationships)

            # Add edges to the graph
            self.add_edge_to_graph(graph, message_id, relationship, failed_edges)

            # Create the subgraph and the ChainDocument
            subgraph = self.create_subgraph(graph, message_id)
            chain_document = self.create_chain_document(
                message_id, embedding_data, tetra_dict, relationship, subgraph
            )

            chain_documents.append(chain_document)

        return chain_documents
