from typing import Dict, List, Optional, Tuple
from dl_matrix.representation.compute import CoordinateRepresentation
from dl_matrix.representation.filters import ChainFilter
from dl_matrix.builder import ChainTreeBuilder
from dl_matrix.context import DEFAULT_PERSIST_DIR, get_file_paths
import logging
import pandas as pd


class ChainCombiner:
    def __init__(
        self,
        builder: Optional[ChainTreeBuilder] = None,
        chain_filter: Optional[ChainFilter] = None,
    ):
        self.builder = builder if builder else ChainTreeBuilder()
        self.chain_filter = chain_filter if chain_filter else ChainFilter()
        self.conversations = self.builder.conversations
        self.logger = logging.getLogger(self.__class__.__name__)
        self.conversation_trees = self.builder.create_conversation_trees()

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
    ):
        self._validate_use_graph_index(use_graph_index)
        start, end = self._process_tree_range(tree_range)
        filtered_trees = self._filter_conversation_trees(start, end, skip_indexes)

        main_dfs = []

        for start_count, conversation_tree in enumerate(filtered_trees, start=start):
            tetra = CoordinateRepresentation(conversation_tree)
            title = tetra.conversation.conversation.title
            print(f"Processing conversation {title}.")
            tree_docs = tetra._procces_coordnates(use_graph)

            for doc in tree_docs:
                tetra.conversation.conversation.mapping[
                    doc.doc_id
                ].message.umap_embeddings = doc.umap_embeddings

                tetra.conversation.conversation.mapping[
                    doc.doc_id
                ].message.cluster_label = doc.cluster_label

                tetra.conversation.conversation.mapping[
                    doc.doc_id
                ].message.n_neighbors = doc.n_neighbors

                tetra.conversation.conversation.mapping[
                    doc.doc_id
                ].message.coordinate = doc.coordinate

            mapping_dict = tetra.conversation.conversation.dict()

            (
                persist_dir,
                main_df_name,
                global_embedding_name,
                conversation_tree_name,
            ) = get_file_paths(base_persist_dir, title)

            main_df = tetra.handler.create_and_persist_dataframes(
                persist_dir,
                main_df_name,
                global_embedding_name,
                conversation_tree_name,
                mapping_dict,
                tree_docs,
            )
            main_dfs.append(main_df)

        return mapping_dict

    def get_message_coord_map(
        self,
        semantic_similarity_model=None,
        exclude_columns=None,
        use_embeddings: bool = False,
        use_basic: bool = False,
    ):
        try:
            message_coord_map = self.builder.create_message_map()
            if not isinstance(message_coord_map, dict):
                raise ValueError("Unexpected data format in message_coord_map.")

            main_df = pd.DataFrame.from_dict(message_coord_map, orient="index")
            main_df = self.builder.format_dataframe(main_df, exclude_columns)

            if semantic_similarity_model:
                main_df = self.builder.apply_embeddings(
                    main_df, semantic_similarity_model, use_embeddings, use_basic
                )

            return main_df

        except Exception as e:
            print(
                f"An error occurred while processing the message coordinates: {str(e)}"
            )
            # Handle the error as needed, possibly by returning an empty DataFrame or None
            return pd.DataFrame()
