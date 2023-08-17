from typing import List, Tuple, Dict
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from hdbscan import HDBSCAN
import warnings

with warnings.catch_warnings():
    from numba.core.errors import NumbaWarning

    warnings.simplefilter("ignore", category=NumbaWarning)
    from umap import UMAP

model = SentenceTransformer("all-mpnet-base-v2")


def apply_umap(
    combined_features: np.ndarray,
    n_neighbors: int,
    n_components: int,
):
    # Check if n_neighbors is larger than the dataset size
    if n_neighbors > len(combined_features):
        # You can either set n_neighbors to the dataset size or another sensible value
        n_neighbors = len(combined_features)
        # You might want to log or print a warning here
        print(
            f"Warning: n_neighbors was larger than the dataset size; truncating to {n_neighbors}"
        )

    umap_embedding = UMAP(
        n_neighbors=int(n_neighbors),
        n_components=n_components,
        n_epochs=10000,
        min_dist=0.0,
        low_memory=False,
        learning_rate=0.5,
        verbose=False,
        metric="cosine",
        init="random",  # use random initialization instead of spectral
    ).fit_transform(combined_features)

    return umap_embedding


def apply_hdbscan(
    embeddings: np.ndarray,
    min_samples: int,
):
    cluster = HDBSCAN(
        metric="euclidean",
        min_samples=min_samples,
        core_dist_n_jobs=1,
        cluster_selection_epsilon=0.1,
        cluster_selection_method="leaf",
        leaf_size=40,
        algorithm="best",
    ).fit(embeddings)

    return cluster.labels_


def apply_dbscan(
    embeddings: np.ndarray,
    min_samples: int,
):
    dbscan = DBSCAN(
        eps=0.2,
        min_samples=min_samples,
        metric="euclidean",
        n_jobs=-1,
    ).fit(embeddings)

    return dbscan.labels_


def apply_cluster(
    embeddings: np.ndarray,
    method: str = "hdbscan",
    min_samples: int = 5,
):
    if method == "hdbscan":
        return apply_hdbscan(embeddings, min_samples)
    elif method == "dbscan":
        return apply_dbscan(embeddings, min_samples)


def group_terms(
    terms: List[Tuple[str, List[float]]],
) -> Dict[int, List[Tuple[str, List[float]]]]:
    try:
        if not terms:
            print("No terms provided for grouping")
            return {}

        # Extract the embeddings from the terms
        embeddings = np.array([embedding for _, embedding in terms])

        # Cluster the embeddings
        clustering = apply_cluster(embeddings)

        # Assign each term to a cluster
        clusters = {i: [] for i in set(clustering)}
        for i, cluster in enumerate(clustering):
            clusters[cluster].append(terms[i])

        return clusters

    except Exception as e:
        print(f"Error in cluster_terms: {e}")
        return {}


def calculate_similarity(embeddings1: List[float], embeddings2: List[float]) -> float:
    """
    Calculate semantic similarity between two sets of embeddings using cosine similarity.

    Args:
        embeddings1 (List[float]): Embeddings of the first message.
        embeddings2 (List[float]): Embeddings of the second message.

    Returns:
        float: Semantic similarity score between the two sets of embeddings.
    """
    # Convert the embeddings lists to numpy arrays
    embeddings1_array = np.array(embeddings1).reshape(1, -1)
    embeddings2_array = np.array(embeddings2).reshape(1, -1)

    # Calculate cosine similarity between the embeddings
    similarity_matrix = cosine_similarity(embeddings1_array, embeddings2_array)

    # The similarity score is the value in the similarity matrix
    similarity_score = similarity_matrix[0][0]

    return similarity_score
