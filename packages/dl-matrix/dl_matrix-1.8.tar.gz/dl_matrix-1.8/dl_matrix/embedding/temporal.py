from typing import List, Tuple, Optional
from sentence_transformers import SentenceTransformer
from dl_matrix.embedding.utils import apply_umap, apply_hdbscan, group_terms
import logging
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


logger = logging.getLogger(__name__)


class Semanticimilarity:
    def __init__(
        self,
        model_name="all-mpnet-base-v2",
        batch_size=100,
    ):
        """Initialize a SemanticSimilarity."""
        self._model_name = model_name
        self._semantic_vectors = []
        self.keywords = []
        self._model = SentenceTransformer(self._model_name)  # Initialize model here
        self.batch_size = batch_size

    @property
    def model_name(self) -> str:
        return self._model_name

    @model_name.setter
    def model_name(self, model_name: str):
        self._model_name = model_name
        self._model = SentenceTransformer(self._model_name)

    def fit(self, keywords: List[str]) -> None:
        """Fit the model to a list of keywords."""

        # Compute semantic vectors
        self.keywords = keywords
        self._semantic_vectors = self.encode_texts(keywords)
        return self._semantic_vectors

    def encode_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a batch of texts as a list of lists of floats using the SentenceTransformer.
        """
        # Preprocess the texts
        self._model.max_seq_length = 512

        # Get embeddings for preprocessed texts
        embeddings = self._model.encode(
            texts,
            batch_size=self.batch_size,
            convert_to_numpy=True,
            show_progress_bar=True,
        )

        return embeddings

    def get_global_embedding(self, main_df: pd.DataFrame, use_embeddings: bool) -> List:
        if use_embeddings:
            return main_df["embeddings"].tolist()
        else:
            embeddings = self.encode_texts(main_df["text"].tolist())
            main_df["embeddings"] = embeddings.tolist()
            main_df.reset_index(drop=True, inplace=True)
            return embeddings

    def create_umap_embeddings(
        self, global_embedding: List, mean_n_neighbors: int
    ) -> List:
        return apply_umap(global_embedding, mean_n_neighbors, 3)

    def _apply_clustering_common(self, main_df, umap_embeddings, clustering_func):
        main_df["umap_embeddings"] = umap_embeddings.tolist()

        labels = clustering_func(umap_embeddings)

        result3d = pd.DataFrame(umap_embeddings, columns=["x", "y", "z"])
        result3d["content"] = main_df["text"].values.tolist()
        result3d["author"] = main_df["author"].values.tolist()
        result3d["message_id"] = main_df["message_id"].values.tolist()
        result3d["labels"] = labels

        return result3d

    def apply_clustering(
        self, main_df: pd.DataFrame, umap_embeddings: List
    ) -> pd.DataFrame:
        return self._apply_clustering_common(main_df, umap_embeddings, apply_hdbscan)

    def calculate_mean_neighbors(
        self, conversation_trees: List, tree_count: int
    ) -> int:
        total_neighbors = (
            sum(
                len(conversation.conversation.mapping)
                for conversation in conversation_trees
            )
            / tree_count
        )
        # divide
        total_conversations = len(conversation_trees)

        return int(total_neighbors / total_conversations)

    def compute_message_embeddings(
        self,
        main_df: pd.DataFrame,
        conversation_trees: List = None,
        use_embeddings: bool = True,
        tree_count: int = 1,
    ) -> None:
        global_embedding = self.get_global_embedding(main_df, use_embeddings)

        mean_n_neighbors = self.calculate_mean_neighbors(conversation_trees, tree_count)
        print(f"Mean number of neighbors: {mean_n_neighbors}")
        print("Total number of messages:", len(global_embedding))

        umap_embeddings = self.create_umap_embeddings(
            global_embedding, mean_n_neighbors
        )

        result3d = self.apply_clustering(main_df, umap_embeddings)

        return result3d

    def compute_similar_keywords(
        self,
        keywords: List[str],
        num_keywords: int = 10,
        use_argmax: bool = True,
        per_keyword: bool = False,
        query: Optional[str] = None,
    ) -> List[str]:
        """
        Compute similar keywords based on embeddings.

        Args:
            keywords (List[str]): List of keywords for which to find similar keywords.
            num_keywords (int, optional): Number of similar keywords to return. Defaults to 10.
            use_argmax (bool, optional): Whether to use argmax for similarity scores. Defaults to True.
            per_keyword (bool, optional): Whether to compute similar keywords per keyword. Defaults to False.
            query (Optional[str], optional): Query keyword for which to find similar keywords. Defaults to None.

        Returns:
            List[str]: List of similar keywords.
        """
        embeddings = self.fit(keywords)

        if query is not None:
            query_vector = self.fit([query])[0]
            similarity_scores = self._compute_similar_keywords_query(
                keywords, query_vector, use_argmax, query
            )
        else:
            if per_keyword:
                similarity_scores = self._compute_similar_keywords_per_keyword(
                    keywords, embeddings, num_keywords
                )
            else:
                similarity_scores = self._compute_similar_keywords_global(
                    keywords, embeddings, num_keywords
                )

        return similarity_scores

    def _compute_similar_keywords_query(
        self,
        keywords: List[str],
        query_vector: List[float],
        use_argmax: bool,
        query: str,
    ) -> List[Tuple[str, float]]:
        """
        Compute similarity scores for keywords against a query vector.

        Args:
            keywords (List[str]): List of keywords to compute similarity for.
            query_vector (List[float]): Vector representing the query.
            use_argmax (bool): Whether to use argmax for similarity scores.

        Returns:
            List[Tuple[str, float]]: List of tuples containing keyword and similarity score.
        """
        # Remove the query keyword from the list of keywords
        keywords = [
            keyword.strip()
            for keyword in keywords
            if keyword.strip().lower() != query.strip().lower()
        ]

        similarity_scores = []

        for keyword in keywords:
            keyword_vector = self.fit([keyword])[0]
            similarity = cosine_similarity([query_vector], [keyword_vector])[0][0]
            similarity_scores.append((keyword, similarity))

        if use_argmax:
            similarity_scores = sorted(
                similarity_scores, key=lambda x: x[1], reverse=True
            )
            similarity_scores = similarity_scores[: self.default_options["n_neighbors"]]
        else:
            similarity_scores = sorted(similarity_scores, key=lambda x: x[0])

        return similarity_scores

    def semantic_search(
        self, query: str, corpus: List[str], num_results: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Perform semantic search against a corpus of text using the query keyword.

        Args:
            query (str): Query keyword.
            corpus (List[str]): List of text documents to search against.
            num_results (int, optional): Number of search results to return. Defaults to 10.

        Returns:
            List[Tuple[str, float]]: List of tuples containing search results and their similarity scores.
        """
        query_vector = self.fit([query])[0]
        corpus_vectors = self.fit(corpus)

        similarity_scores = cosine_similarity([query_vector], corpus_vectors)[0]
        results_with_scores = [
            (corpus[i], score) for i, score in enumerate(similarity_scores)
        ]
        sorted_results = sorted(results_with_scores, key=lambda x: x[1], reverse=True)

        return sorted_results[:num_results]

    def _compute_similar_keywords_per_keyword(
        self, keywords: List[str], embeddings: List[List[float]], num_keywords: int
    ) -> List[List[str]]:
        similarity_scores_list = [
            cosine_similarity([vector], embeddings)[0] for vector in embeddings
        ]
        similar_keywords_list = [
            [keywords[i] for i in np.argsort(similarity_scores)[::-1][:num_keywords]]
            for similarity_scores in similarity_scores_list
        ]

        return similar_keywords_list

    def _compute_similar_keywords_global(
        self,
        keywords: List[str],
        embeddings: List[List[float]],
        num_keywords: int,
    ) -> List[str]:
        """
        Compute similar keywords globally based on embeddings.

        Args:
            keywords (List[str]): List of keywords to compute similarity for.
            embeddings (List[List[float]]): List of embeddings corresponding to keywords.
            num_keywords (int): Number of similar keywords to return.

        Returns:
            List[str]: List of similar keywords.
        """
        clusters = group_terms(zip(keywords, embeddings))
        sorted_clusters = sorted(clusters.values(), key=len, reverse=True)[
            :num_keywords
        ]
        similarity_scores = [term for cluster in sorted_clusters for term, _ in cluster]

        return similarity_scores
