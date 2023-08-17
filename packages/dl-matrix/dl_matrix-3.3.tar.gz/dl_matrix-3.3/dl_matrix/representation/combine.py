from typing import Dict, List, Optional, Tuple, Callable
from dl_matrix.representation.base import Representation
from dl_matrix.representation.compute import CoordinateRepresentation
from dl_matrix.representation.handler import ChainHandler
from dl_matrix.representation.filters import ChainFilter
from dl_matrix.embedding.utils import apply_cluster
from dl_matrix.embedding.spatial import SpatialSimilarity
from dl_matrix.builder import ChainTreeBuilder
from dl_matrix.context import DEFAULT_PERSIST_DIR, get_file_paths

import pandas as pd


class ChainCombiner:
    def __init__(
        self,
        target_number: int = 6,
        builder: Optional[ChainTreeBuilder] = None,
        chain_filter: Optional[ChainFilter] = None,
        chain_handler: Optional[ChainHandler] = None,
    ):
        self.builder = builder if builder else ChainTreeBuilder()
        self.chain_filter = chain_filter if chain_filter else ChainFilter()
        self.chain_handler = chain_handler if chain_handler else ChainHandler()
        self.conversations = self.builder.conversations
        self.conversation_trees = self.builder.create_conversation_trees(target_number)
        self.semantic_similarity = SpatialSimilarity()

    def _validate_use_graph_index(self, use_graph_index):
        if use_graph_index is not None and not isinstance(use_graph_index, int):
            raise ValueError("use_graph_index should be an integer or None.")

    def _process_tree_range(self, tree_range):
        start, end = tree_range
        if end is None:
            end = len(self.conversation_trees)
        return start, end

    def _filter_conversation_trees(self, start, end, skip_indexes):
        if skip_indexes is not None:
            filtered_trees = [
                ct
                for i, ct in enumerate(self.conversation_trees[start:end])
                if i not in skip_indexes
            ]
        else:
            filtered_trees = self.conversation_trees[start:end]
        return filtered_trees

    def process_conversation_trees(
        self,
        n_neighbors=15,
        use_graph: bool = False,
        use_graph_index: Optional[int] = None,
        tree_range: Optional[Tuple[int, int]] = (0, None),
        skip_indexes: Optional[List[int]] = None,
        base_persist_dir: str = DEFAULT_PERSIST_DIR,
    ):
        self._validate_use_graph_index(use_graph_index)
        start, end = self._process_tree_range(tree_range)
        filtered_trees = self._filter_conversation_trees(start, end, skip_indexes)

        combined_tree = self.builder.combine_conversations(filtered_trees)

        processed_combined_tree = self._process_single_conversation_tree(
            n_neighbors=n_neighbors,
            conversation_tree=combined_tree,
            use_graph=use_graph,
            base_persist_dir=base_persist_dir,
        )
        return processed_combined_tree

    def _process_single_conversation_tree(
        self,
        n_neighbors: int,
        conversation_tree: Representation,
        use_graph: bool,
        base_persist_dir: str,
    ) -> pd.DataFrame:
        """Process a single conversation tree based on given parameters."""

        tetra = CoordinateRepresentation(conversation_tree)
        title = tetra.conversation.conversation.title
        print(f"Processing conversation {title}.")
        tree_docs, relationships = tetra._create_coordinates_graph(use_graph=use_graph)

        file_paths = get_file_paths(base_persist_dir, title)

        (
            persist_dir,
            main_df_name,
            global_embedding_name,
            conversation_tree_name,
        ) = file_paths

        main_df = self.get_message_coord_map(
            n_neighbors=n_neighbors,
            trees=[conversation_tree],
            tree_docs=tree_docs,
            relationships=relationships,
            builder=self.builder,
            semantic_similarity=self.semantic_similarity,
            clustering_func=apply_cluster,
        )

        self.chain_handler.persist_dataframes(
            main_df,
            persist_dir,
            main_df_name,
            global_embedding_name,
            conversation_tree_name,
            conversation_tree.conversation.dict(),
        )

        return main_df

    def _create_message_map(
        self, builder: ChainTreeBuilder, trees: List[Representation]
    ):
        try:
            message_coord_map = builder.create_message_map(trees=trees)
            if not isinstance(message_coord_map, dict):
                raise ValueError("Unexpected data format in message_coord_map.")
            return pd.DataFrame.from_dict(message_coord_map, orient="index")
        except ValueError as ve:
            print(f"Error in create_message_map: {ve}")
            raise ve

    def integrate_docs_relationships(
        self, main_df: pd.DataFrame, tree_docs: Dict, relationships: Dict
    ) -> pd.DataFrame:
        """Integrate tree_docs and relationships into the main DataFrame.

        Parameters:
        - main_df (pd.DataFrame): The main dataframe.
        - tree_docs (Dict): Dictionary of tree documents.
        - relationships (Dict): Dictionary of relationships.

        Returns:
        - pd.DataFrame: Updated main dataframe.
        """

        try:
            column_names = [
                "depth_x",
                "sibling_y",
                "sibling_count_z",
                "time_t",
                "n_parts",
            ]

            tree_df = pd.DataFrame.from_dict(
                tree_docs, orient="index", columns=column_names
            )

            # Integrate tree_docs into main_df
            main_df = main_df.merge(
                tree_df, left_index=True, right_index=True, how="left"
            )

            # Integrate relationships into main_df
            relationship_df = pd.DataFrame.from_dict(relationships, orient="index")
            main_df = main_df.join(relationship_df, rsuffix="_relation")
            main_df.columns = [col.lower() for col in main_df.columns]

            return main_df

        except Exception as e:
            print(f"Error in integrate_docs_relationships: {e}")
            raise e

    def compute_embeddings(
        self, df, semantic_similarity: SpatialSimilarity, use_embeddings
    ):
        try:
            global_embedding, df = semantic_similarity.get_global_embedding(
                df, use_embeddings
            )
            return global_embedding, df
        except Exception as e:
            print(f"Error in compute_embeddings: {e}")
            raise e

    def umap_clustering_operations(
        self,
        df,
        n_neighbors,
        semantic_similarity: SpatialSimilarity,
        global_embedding: pd.DataFrame,
        clustering_func: Callable,
    ):
        try:
            umap_embeddings = semantic_similarity.create_umap_embeddings(
                global_embedding, n_neighbors
            )

            df = df.assign(
                umap_embeddings=umap_embeddings, labels=clustering_func(umap_embeddings)
            )
            df[["x", "y", "z"]] = pd.DataFrame(
                df["umap_embeddings"].tolist(), index=df.index
            )
            df.drop("umap_embeddings", axis=1, inplace=True)
            return df
        except Exception as e:
            print(f"Error in umap_clustering_operations: {e}")
            raise e

    def format_dataframe(
        self, builder: ChainTreeBuilder, df: pd.DataFrame, exclude_columns: List
    ):
        try:
            return builder.format_dataframe(df, exclude_columns)
        except Exception as e:
            print(f"Error in format_dataframe: {e}")
            raise e

    def get_message_coord_map(
        self,
        n_neighbors: int,
        trees: Optional[List[Representation]] = None,
        tree_docs: Dict[str, Tuple[float, float, float, float, int]] = None,
        relationships: Dict[str, Dict[str, str]] = None,
        exclude_columns=None,
        use_embeddings: bool = False,
        clustering_func: Callable = None,
        builder=None,
        semantic_similarity=None,
    ) -> pd.DataFrame:
        try:
            main_df = self._create_message_map(builder, trees)
            if tree_docs:
                main_df = self.integrate_docs_relationships(
                    main_df, tree_docs, relationships
                )
            global_embedding, main_df = self.compute_embeddings(
                main_df, semantic_similarity, use_embeddings
            )
            main_df = self.umap_clustering_operations(
                main_df,
                n_neighbors,
                semantic_similarity,
                global_embedding,
                clustering_func,
            )
            main_df = self.format_dataframe(builder, main_df, exclude_columns)
        except Exception as e:
            print(f"Error in get_message_coord_map: {e}")
            raise e
        return main_df
