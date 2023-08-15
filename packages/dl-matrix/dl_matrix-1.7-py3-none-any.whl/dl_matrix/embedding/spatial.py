from typing import List, Tuple, Dict, Any, Union, Optional
from sentence_transformers import SentenceTransformer
from dl_matrix.embedding.utils import apply_umap
from sklearn.cluster import DBSCAN
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
            clusters = self.cluster_terms(list(message_embeddings.items()))

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

    def cluster_terms(
        self, terms: List[Tuple[str, List[float]]]
    ) -> Dict[int, List[Tuple[str, List[float]]]]:
        try:
            if not terms:
                print("No terms provided for grouping")
                return {}

            # Extract the embeddings from the terms
            embeddings = np.array([embedding for _, embedding in terms])

            # Apply weights if available
            for i, (term, _) in enumerate(terms):
                if term in self.weights:
                    embeddings[i] *= self.weights[term]

            clustering = DBSCAN(
                eps=0.5,
                min_samples=5,
                metric="euclidean",
            ).fit(embeddings)
            # Assign each term to a cluster
            clusters = {i: [] for i in set(clustering.labels_)}
            for i, label in enumerate(clustering.labels_):
                clusters[label].append(terms[i])

            return clusters

        except Exception as e:
            print(f"Error in cluster_terms: {e}")
            return {}
