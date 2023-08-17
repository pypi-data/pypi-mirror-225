from typing import Dict, List, Optional, Tuple, Callable
from dl_matrix.representation.base import Representation
import pandas as pd


class MessageCoordProcessor:
    @staticmethod
    def create_message_map(builder, trees):
        try:
            message_coord_map = builder.create_message_map(trees=trees)
            if not isinstance(message_coord_map, dict):
                raise ValueError("Unexpected data format in message_coord_map.")
            return pd.DataFrame.from_dict(message_coord_map, orient="index")
        except ValueError as ve:
            print(f"Error in create_message_map: {ve}")
            raise ve

    @staticmethod
    def integrate_tree_docs(main_df, tree_docs):
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
            return main_df.merge(tree_df, left_index=True, right_index=True, how="left")
        except Exception as e:
            print(f"Error in integrate_tree_docs: {e}")
            raise e

    @staticmethod
    def compute_embeddings(df, semantic_similarity, use_embeddings):
        try:
            global_embedding, df = semantic_similarity.get_global_embedding(
                df, use_embeddings
            )
            return global_embedding, df
        except Exception as e:
            print(f"Error in compute_embeddings: {e}")
            raise e

    @staticmethod
    def umap_clustering_operations(
        df, trees, semantic_similarity, global_embedding, tree_count, clustering_func
    ):
        try:
            mean_n_neighbors = semantic_similarity.calculate_mean_neighbors(
                trees, tree_count
            )
            umap_embeddings = semantic_similarity.create_umap_embeddings(
                global_embedding, mean_n_neighbors
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

    @staticmethod
    def format_dataframe(builder, df, exclude_columns):
        try:
            return builder.format_dataframe(df, exclude_columns)
        except Exception as e:
            print(f"Error in format_dataframe: {e}")
            raise e

    def get_message_coord_map(
        self,
        tree_count: int,
        trees: Optional[List[Representation]] = None,
        tree_docs: Dict[str, Tuple[float, float, float, float, int]] = None,
        exclude_columns=None,
        use_embeddings: bool = False,
        clustering_func: Callable = None,
        builder=None,
        semantic_similarity=None,
    ) -> pd.DataFrame:
        try:
            main_df = self.create_message_map(builder, trees)
            if tree_docs:
                main_df = self.integrate_tree_docs(main_df, tree_docs)
            global_embedding, main_df = self.compute_embeddings(
                main_df, semantic_similarity, use_embeddings
            )
            main_df = self.umap_clustering_operations(
                main_df,
                trees,
                semantic_similarity,
                global_embedding,
                tree_count,
                clustering_func,
            )
            main_df = self.format_dataframe(builder, main_df, exclude_columns)
        except Exception as e:
            print(f"Error in get_message_coord_map: {e}")
            raise e
        return main_df
