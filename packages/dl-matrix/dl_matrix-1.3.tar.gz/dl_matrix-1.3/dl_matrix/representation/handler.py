from typing import List, Dict
from dl_matrix.coordinate import Coordinate
from dl_matrix.context import MultiLevelContext, DataFrameStore, JsonStore
from dl_matrix.embedding.spatial import SpatialSimilarity
from dl_matrix.models import ChainDocument, ChainDocumentStore
from pydantic import BaseModel
import pandas as pd


class ChainHandler(BaseModel):
    chain_documents: List[ChainDocument] = []
    flattened_dict_id_coord: Dict[str, Coordinate] = {}
    semantic_similarity_model = SpatialSimilarity()
    docstore = ChainDocumentStore()

    class Config:
        arbitrary_types_allowed = True

    def add_local_embeddings(self, docs: List[ChainDocument]) -> None:
        for doc in docs:
            if doc is None:
                continue
            self.chain_documents.append(doc)
            self.docstore.add_documents([doc])  # Add single document
            self.flattened_dict_id_coord[doc.doc_id] = doc.coordinate

    def create_dataframe(self) -> pd.DataFrame:
        """
        Create a DataFrame from the chain documents.
        """
        data = [
            {
                "doc_id": doc.doc_id if doc.doc_id else "",
                "text": doc.text,
                "author": doc.author,
                "sub_graph": doc.sub_graph,
                "n_neighbors": doc.n_neighbors,
                "relationships": doc.relationships,
                "create_time": doc.create_time,
                "embedding": doc.embedding,
                "umap_embeddings": doc.umap_embeddings,
                "cluster_label": doc.cluster_label,
            }
            for doc in self.chain_documents
        ]

        main_df = pd.DataFrame(data)
        return main_df

    def add_documents_and_create_dataframe(
        self, docs: List[ChainDocument]
    ) -> pd.DataFrame:
        """
        Adds local embeddings and creates a DataFrame from the documents.
        """
        self.add_local_embeddings(docs)
        return self.create_dataframe()

    def add_coordinates_to_dataframe(self, storage_context: MultiLevelContext):
        # Add the 'coordinate' column
        storage_context.main_df_store.df[
            "coordinate"
        ] = storage_context.main_df_store.df["doc_id"].apply(
            lambda x: self.flattened_dict_id_coord[x]
        )

        # Split 'coordinate' column into multiple columns
        storage_context.main_df_store.df[
            Coordinate.get_coordinate_names()
        ] = pd.DataFrame(
            storage_context.main_df_store.df["coordinate"].tolist(),
            index=storage_context.main_df_store.df.index,
        )

        # Optionally, drop the 'coordinate' column if no longer needed
        storage_context.main_df_store.df.drop("coordinate", axis=1, inplace=True)

        # Split 'umap_embeddings' column into multiple columns for x, y, z
        storage_context.main_df_store.df[["x", "y", "z"]] = pd.DataFrame(
            storage_context.main_df_store.df["umap_embeddings"].tolist(),
            index=storage_context.main_df_store.df.index,
        )

        # Optionally, drop the 'umap_embeddings' column if no longer needed
        storage_context.main_df_store.df.drop("umap_embeddings", axis=1, inplace=True)

    def initialize_storage_context(
        self, main_df: pd.DataFrame, conversation_tree: dict
    ):
        return MultiLevelContext.from_defaults(
            main_df_store=DataFrameStore(main_df),
            conversation_tree_store=JsonStore(conversation_tree),
        )

    def create_and_persist_dataframes(
        self,
        persist_dir,
        main_df_name,
        global_embedding_name,
        conversation_tree_name,
        conversation_tree,
        tree_docs,
    ):
        try:
            # Create the main_df DataFrame
            main_df = self.add_documents_and_create_dataframe(tree_docs)

            # Initialize storage context with main_df
            storage_context = self.initialize_storage_context(
                main_df, conversation_tree
            )

            # Add coordinates to the DataFramekkkk
            self.add_coordinates_to_dataframe(storage_context)

            # Persist the storage context
            storage_context.persist(
                persist_dir=persist_dir,
                main_df_fname=main_df_name,
                global_embedding_fname=global_embedding_name,
                conversation_tree_fname=conversation_tree_name,
            )
            return main_df

        except Exception as e:
            # Handle any exceptions that might occur and return None
            print("An error occurred while creating and persisting dataframes:", str(e))
            return None
