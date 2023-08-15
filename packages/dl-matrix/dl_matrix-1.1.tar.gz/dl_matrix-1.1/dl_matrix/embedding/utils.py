from typing import List, Tuple, Dict
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import linkage
import numpy as np
import hdbscan
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
        verbose=True,
        metric="cosine",
        init="random",  # use random initialization instead of spectral
    ).fit_transform(combined_features)

    return umap_embedding


def apply_hdbscan(
    embeddings: np.ndarray,
):
    hdbscan.dist_metrics.METRIC_MAPPING
    hdbscan_minimal_cluster_size = 100
    hdbscan_min_samples = 5

    cluster = hdbscan.HDBSCAN(
        min_cluster_size=hdbscan_minimal_cluster_size,
        metric="euclidean",
        min_samples=hdbscan_min_samples,
        core_dist_n_jobs=1,
        cluster_selection_epsilon=0.1,
        cluster_selection_method="leaf",
        leaf_size=40,
        algorithm="best",
    ).fit(embeddings)

    return cluster.labels_


def apply_dbscan(
    embeddings: np.ndarray,
    eps: float,
    min_samples: int,
):
    dbscan = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric="euclidean",
        n_jobs=-1,
    ).fit(embeddings)

    return dbscan.labels_


def apply_agglomerative(
    embeddings: np.ndarray,
    n_clusters: int,
):
    clustering = AgglomerativeClustering(
        n_clusters=n_clusters, affinity="euclidean", linkage="ward"
    ).fit(embeddings)

    return clustering.labels_


def apply_kmeans(
    embeddings: np.ndarray,
    n_clusters: int,
):
    kmeans = KMeans(
        n_clusters=n_clusters,
        init="k-means++",
        n_init=10,
        max_iter=300,
        tol=0.0001,
        verbose=0,
        random_state=42,
        copy_x=True,
        algorithm="auto",
    ).fit(embeddings)

    return kmeans.labels_


def apply_linkage(
    embeddings: np.ndarray,
    method: str,
    metric: str,
):
    Z = linkage(embeddings, method=method, metric=metric)
    return Z


def apply_cluster(
    embeddings: np.ndarray,
    method: str,
    metric: str,
    n_clusters: int,
):
    if method == "hdbscan":
        return apply_hdbscan(embeddings)
    elif method == "dbscan":
        return apply_dbscan(embeddings, 0.5, 5)
    elif method == "agglomerative":
        return apply_agglomerative(embeddings, n_clusters)
    elif method == "kmeans":
        return apply_kmeans(embeddings, n_clusters)
    elif method == "linkage":
        return apply_linkage(embeddings, method, metric)
    else:
        raise ValueError(f"Unknown clustering method: {method}")


def get_cluster_labels(
    embeddings: np.ndarray,
    method: str,
    metric: str,
    n_clusters: int,
):
    cluster_labels = apply_cluster(embeddings, method, metric, n_clusters)
    return cluster_labels


def get_cluster_labels_dict(
    embeddings: np.ndarray,
    method: str,
    metric: str,
    n_clusters: int,
):
    cluster_labels = get_cluster_labels(embeddings, method, metric, n_clusters)
    cluster_labels_dict = {}
    for i, label in enumerate(cluster_labels):
        cluster_labels_dict[i] = label
    return cluster_labels_dict


def group_terms(
    terms: List[Tuple[str, List[float]]], use_dbscan: bool = True
) -> Dict[int, List[Tuple[str, List[float]]]]:
    """
    Group terms based on their embeddings.

    Args:
        terms (List[Tuple[str, List[float]]]): List of terms to group.
        use_dbscan (bool, optional): Whether to use DBSCAN for clustering. Defaults to True.

    Returns:
        Dict[int, List[Tuple[str, List[float]]]]: Dictionary containing clusters of terms.
    """
    if use_dbscan:
        return group_terms_with_dbscan(terms)
    else:
        return group_terms_with_agglomerative(terms)


def group_terms_with_dbscan(
    terms: List[Tuple[str, List[float]]]
) -> Dict[int, List[Tuple[str, List[float]]]]:
    embeddings = np.array([embedding for _, embedding in terms])
    clustering = DBSCAN(eps=0.5, min_samples=5, metric="euclidean").fit(embeddings)
    clusters = {i: [] for i in set(clustering.labels_)}
    for i, label in enumerate(clustering.labels_):
        clusters[label].append(terms[i])
    return clusters


def group_terms_with_agglomerative(
    terms: List[Tuple[str, List[float]]]
) -> Dict[int, List[Tuple[str, List[float]]]]:
    try:
        if not terms:
            print("No terms provided for grouping")
            return {}

        # Extract the embeddings from the terms
        embeddings = [embedding for _, embedding in terms]

        # Reshape the embeddings array to have 2 dimensions
        embeddings = np.array(embeddings).reshape(len(embeddings), -1)

        # Compute the linkage matrix
        Z = linkage(
            embeddings, "ward"
        )  # 'ward' is one of the methods that can be used to calculate the distance between newly formed clusters. 'single', 'complete', 'average' are also popular.

        clustering = AgglomerativeClustering(distance_threshold=0, n_clusters=None)

        # Compute the clusters
        clustering = clustering.fit(embeddings)

        # Assign each term to a cluster
        clusters = {i: [] for i in set(clustering.labels_)}
        for i, label in enumerate(clustering.labels_):
            clusters[label].append(terms[i])

        return clusters

    except Exception as e:
        print(f"Error grouping terms: {e}")
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
