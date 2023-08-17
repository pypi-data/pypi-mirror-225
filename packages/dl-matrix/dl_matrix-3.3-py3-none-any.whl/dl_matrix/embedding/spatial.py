from typing import List, Tuple, Dict, Any, Union, Optional
from sentence_transformers import SentenceTransformer
from dl_matrix.embedding.utils import apply_umap, group_terms
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np


class SpatialSimilarity:
    def __init__(
        self,
        reduce_dimensions=True,
        batch_size=100,
        n_components=3,
        weights=None,
        model_name="all-mpnet-base-v2",
    ):
        """Initialize a SemanticSimilarity."""
        self._model_name = model_name
        self._semantic_vectors = []
        self.keywords = []
        self._model = SentenceTransformer(self._model_name)  # Initialize model here
        self.weights = weights if weights is not None else {}
        self.default_options = {
            "n_components": n_components,
            "reduce_dimensions": reduce_dimensions,
            "n_neighbors": None,
        }
        self.batch_size = batch_size
        self._semantic_vectors = []
        self.keywords = []

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

    def process_message_dict(
        self, message_dict: Dict[str, Any]
    ) -> Tuple[List[str], List[str]]:
        """
        Extract the message text and ID from the message dictionary.
        """
        message_texts = []
        message_ids = []
        for message_id, message in message_dict.items():
            if isinstance(message, str):
                message_texts.append(message)
                message_ids.append(message_id)
            elif message.message and message.message.author.role != "system":
                message_texts.append(message.message.content.parts[0])
                message_ids.append(message.id)
        return message_texts, message_ids

    def generate_message_to_embedding_dict(
        self, message_ids: List[str], embeddings: List[np.array]
    ) -> Dict[str, np.array]:
        """
        Generate a dictionary mapping message IDs to embeddings.
        """
        return {message_ids[i]: embeddings[i] for i in range(len(message_ids))}

    def compute_neighbors(self, grid, message_dict: Dict[str, Any]) -> Dict[str, int]:
        """
        For each message, determine the number of neighbors.
        """
        n_neighbors_dict = {}
        for message_id in message_dict:
            n_neighbors_dict[message_id] = grid.determine_n_neighbors(message_id)
        return n_neighbors_dict

    def generate_message_embeddings(
        self,
        grid,
        message_dict: Dict[str, Any],
        options: dict = None,
    ) -> Dict[str, Union[np.array, Tuple[str, str]]]:
        """
        Generate semantic embeddings for the messages in the conversation tree using a sentence transformer.
        """
        # Update default options with user-specified options
        if options is not None:
            self.default_options.update(options)

        # Extract the message text and ID from the message dictionary
        message_texts, message_ids = self.process_message_dict(message_dict)

        # Encode the message texts to obtain their embeddings
        embeddings = self.encode_texts(message_texts)

        # Create a dictionary mapping message IDs to embeddings
        message_embeddings = self.generate_message_to_embedding_dict(
            message_ids, embeddings
        )

        if len(message_dict) > 1:
            n_neighbors_dict = self.compute_neighbors(grid, message_dict)
            self.default_options["n_neighbors"] = np.mean(
                list(n_neighbors_dict.values())
            )
            reduced_embeddings = self.generate_reduced_embeddings(
                embeddings, self.default_options
            )

            message_embeddings = self.generate_message_to_embedding_dict(
                message_ids, reduced_embeddings
            )
            clusters = group_terms(list(message_embeddings.items()))

            # Assign each message id to a cluster label
            clustered_messages = {}
            for cluster_label, terms in clusters.items():
                for term in terms:
                    # Assuming term is a tuple with more than 2 elements, we only take the first one
                    term_id = term[0]
                    clustered_messages[term_id] = (
                        message_embeddings[term_id],
                        cluster_label,
                        embeddings,
                        n_neighbors_dict[
                            term_id
                        ],  # Add the count of neighbors to the dictionary
                    )

            return clustered_messages

    def generate_reduced_embeddings(
        self, embeddings: np.ndarray, options: dict = None
    ) -> np.ndarray:
        """
        Reduce the dimensionality of the embeddings if necessary.
        """
        # convert embeddings dictionary to numpy array
        if isinstance(embeddings, dict):
            embeddings = np.array(list(embeddings.values()))

        # Update default options with user-specified options
        if options is not None:
            self.default_options.update(options)

        if self.default_options["reduce_dimensions"]:
            embeddings = apply_umap(
                embeddings,
                self.default_options["n_neighbors"],
                self.default_options["n_components"],
            )

        return embeddings

    def get_global_embedding(
        self, main_df: pd.DataFrame, use_embeddings: bool = False
    ) -> List:
        if use_embeddings:
            return main_df["embeddings"].tolist()
        else:
            embeddings = self.encode_texts(main_df["text"].tolist())
            main_df["embeddings"] = embeddings.tolist()
            main_df.reset_index(drop=True, inplace=True)
            return embeddings, main_df

    def create_umap_embeddings(
        self, global_embedding: List, mean_n_neighbors: int
    ) -> List:
        return apply_umap(global_embedding, mean_n_neighbors, 3).tolist()

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
                    keywords, embeddings, use_argmax, num_keywords
                )

        return similarity_scores

    def _compute_similar_keywords_global(
        self,
        keywords: List[str],
        embeddings: List[List[float]],
        use_argmax: bool,
        num_keywords: int,
    ) -> List[Tuple[str, float]]:
        """
        Compute similarity scores for keywords against a global embedding.

        Args:
            keywords (List[str]): List of keywords to compute similarity for.
            embeddings (List[List[float]]): List of embeddings for the keywords.
            use_argmax (bool): Whether to use argmax for similarity scores.
            num_keywords (int): Number of similar keywords to return.

        Returns:
            List[Tuple[str, float]]: List of tuples containing keyword and similarity score.
        """
        similarity_scores = cosine_similarity(embeddings, embeddings)
        similarity_scores = np.triu(similarity_scores, k=1)
        similarity_scores = similarity_scores.flatten()
        similarity_scores = similarity_scores[similarity_scores != 0]
        similarity_scores = np.sort(similarity_scores)[::-1]

        if use_argmax:
            similarity_scores = similarity_scores[:num_keywords]
        else:
            similarity_scores = similarity_scores[: num_keywords * len(keywords)]

        similarity_scores = similarity_scores.reshape(len(keywords), num_keywords)

        similar_keywords = []

        for i, keyword in enumerate(keywords):
            keyword_scores = similarity_scores[i]
            similar_keywords.append(
                [keywords[j] for j in np.argsort(keyword_scores)[::-1][:num_keywords]]
            )

        return similar_keywords

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
