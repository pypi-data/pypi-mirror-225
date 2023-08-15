from typing import Dict, List, Optional, Tuple, Union
from dl_matrix.representation.compute import CoordinateRepresentation
from dl_matrix.representation.filters import ChainFilter
from dl_matrix.embedding.temporal import Semanticimilarity
from dl_matrix.builder import ChainTreeBuilder
from dl_matrix.context import DEFAULT_PERSIST_DIR, get_file_paths
import pandas as pd


class ChainCombiner:
    def __init__(
        self,
        target_number: int = 6,
        builder: Optional[ChainTreeBuilder] = None,
        chain_filter: Optional[ChainFilter] = None,
    ):
        self.builder = builder if builder else ChainTreeBuilder()
        self.chain_filter = chain_filter if chain_filter else ChainFilter()
        self.conversations = self.builder.conversations
        self.conversation_trees = self.builder.create_conversation_trees(target_number)
        self.semantic_similarity = Semanticimilarity()

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
        use_graph: bool = False,
        use_graph_index: Optional[int] = None,
        tree_range: Optional[Tuple[int, int]] = (0, None),
        skip_indexes: Optional[List[int]] = None,
        base_persist_dir: str = DEFAULT_PERSIST_DIR,
        combine_conversation_trees: bool = False,
    ):
        self._validate_use_graph_index(use_graph_index)
        start, end = self._process_tree_range(tree_range)
        tree_count = end - start
        filtered_trees = self._filter_conversation_trees(start, end, skip_indexes)

        if combine_conversation_trees:
            combined_tree = self.builder.combine_conversations(filtered_trees)
            # Process the combined tree with specific parameters
            processed_combined_tree = self._process_single_conversation_tree(
                tree_count=tree_count,
                conversation_tree=combined_tree,
                use_graph=use_graph,
                base_persist_dir=base_persist_dir,
                animate=True,
                local_embedding=False,
            )
            return processed_combined_tree

        main_dfs = []
        for start_count, conversation_tree in enumerate(filtered_trees, start=start):
            main_df = self._process_single_conversation_tree(
                conversation_tree, use_graph, base_persist_dir
            )
            main_dfs.append(main_df)

        return main_dfs

    def _process_single_conversation_tree(
        self,
        tree_count: int,
        conversation_tree: CoordinateRepresentation,
        use_graph: bool,
        base_persist_dir: str,
        animate: bool = False,
        local_embedding: bool = True,
    ) -> Union[Dict[str, Tuple[float, float, float, float, int]], pd.DataFrame]:
        """Process a single conversation tree based on given parameters."""

        tetra = CoordinateRepresentation(conversation_tree)
        title = tetra.conversation.conversation.title
        print(f"Processing conversation {title}.")
        tree_docs = tetra._procces_coordnates(
            use_graph, animate=animate, local_embedding=local_embedding
        )
        file_paths = get_file_paths(base_persist_dir, title)

        (
            persist_dir,
            main_df_name,
            global_embedding_name,
            conversation_tree_name,
        ) = file_paths

        # If animate is True, use the get_message_coord_map method
        if animate:
            main_df = self.get_message_coord_map(
                tree_count, [conversation_tree], tree_docs
            )
            tetra.handler.persist_dataframes(
                main_df,
                persist_dir,
                main_df_name,
                global_embedding_name,
                conversation_tree_name,
                conversation_tree.conversation.dict(),
            )
            return main_df

        self._update_mappings(tetra, tree_docs)

        mapping_dict = tetra.conversation.conversation.dict()

        main_df = tetra.handler.create_dataframe(tree_docs, conversation_tree)
        tetra.handler.persist_dataframes(
            main_df,
            persist_dir,
            main_df_name,
            global_embedding_name,
            conversation_tree_name,
            mapping_dict,
        )
        return main_df

    def _update_mappings(self, tetra: CoordinateRepresentation, tree_docs):
        """Update the mappings for each doc in tree_docs."""
        for doc in tree_docs:
            mapping = tetra.conversation.conversation.mapping[doc.id]
            attributes = [
                "umap_embeddings",
                "cluster_label",
                "n_neighbors",
                "coordinate",
            ]
            for attr in attributes:
                setattr(mapping, attr, getattr(doc, attr))

    def get_message_coord_map(
        self,
        tree_count: int,
        trees: Optional[List[CoordinateRepresentation]] = None,
        tree_docs: Dict[str, Tuple[float, float, float, float, int]] = None,
        exclude_columns=None,
        use_embeddings: bool = False,
    ) -> pd.DataFrame:
        """Generate a DataFrame from the given trees and tree_docs.

        Parameters:
        - trees (Optional[List[ChainTreeIndex]]): List of conversation trees to process.
        - tree_docs (Dict): Dictionary with message data.
        - exclude_columns: Columns to exclude from the final DataFrame.
        - use_embeddings (bool): Flag to indicate use of embeddings.
        - use_basic (bool): Flag to indicate use of basic embeddings.

        Returns:
        - pd.DataFrame: Processed DataFrame.
        """

        try:
            # Passing the trees parameter to create_message_map
            message_coord_map = self.builder.create_message_map(trees=trees)

            if not isinstance(message_coord_map, dict):
                raise ValueError("Unexpected data format in message_coord_map.")

            main_df = pd.DataFrame.from_dict(message_coord_map, orient="index")
            main_df = self.builder.format_dataframe(main_df, exclude_columns)

            # If tree_docs are provided, integrate them into the main_df
            if tree_docs:
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
                main_df = main_df.merge(
                    tree_df, left_index=True, right_index=True, how="left"
                )
                main_df["coordinates"] = main_df.apply(
                    lambda row: (
                        row["depth_x"],
                        row["sibling_y"],
                        row["sibling_count_z"],
                        row["time_t"],
                    ),
                    axis=1,
                )
                main_df = main_df.drop(columns=column_names)

            main_df = self.semantic_similarity.compute_message_embeddings(
                main_df, trees, use_embeddings, tree_count
            )

            return main_df
        except Exception as e:
            print(
                f"An error occurred while processing the message coordinates: {str(e)}"
            )
            return pd.DataFrame()
