"""
clustering.py

Groups sentence vectors into clusters using K-Means. Each cluster is
treated as a distinct topic in the document; the sentence closest to a
cluster's centroid is selected as that topic's representative sentence.
"""

import numpy as np
from sklearn.cluster import KMeans


def cluster_sentences(sentence_vectors: np.ndarray, num_clusters: int) -> np.ndarray:
    """
    Cluster sentence vectors into `num_clusters` groups using K-Means.

    Args:
        sentence_vectors: Matrix of shape (num_sentences, vector_size).
        num_clusters: Number of clusters (topics) to form.

    Returns:
        A trained KMeans model.
    """
    num_clusters = min(num_clusters, len(sentence_vectors))
    model = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    model.fit(sentence_vectors)
    return model


def select_representative_sentences(
    sentences: list[str], sentence_vectors: np.ndarray, num_clusters: int
) -> list[str]:
    """
    Select the most representative sentence from each cluster.

    For each cluster, the sentence whose vector is closest to the
    cluster's centroid is chosen. Results are returned in their
    original document order.

    Args:
        sentences: The original (untokenized) sentences.
        sentence_vectors: Matrix of shape (num_sentences, vector_size),
            aligned index-for-index with `sentences`.
        num_clusters: Number of sentences to select (one per cluster).

    Returns:
        A list of selected sentences, in original document order.
    """
    if not sentences:
        return []

    model = cluster_sentences(sentence_vectors, num_clusters)
    selected_indices = set()

    for cluster_id in range(model.n_clusters):
        cluster_member_indices = np.where(model.labels_ == cluster_id)[0]
        if len(cluster_member_indices) == 0:
            continue

        centroid = model.cluster_centers_[cluster_id]
        member_vectors = sentence_vectors[cluster_member_indices]
        distances = np.linalg.norm(member_vectors - centroid, axis=1)
        closest_index = cluster_member_indices[np.argmin(distances)]
        selected_indices.add(closest_index)

    return [sentences[i] for i in sorted(selected_indices)]