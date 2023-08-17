import numpy as np
from typing import Any, Dict, List, Tuple, Callable
from sklearn.metrics.pairwise import cosine_similarity


class StableMatching:
    """
    Class for performing stable matching between nodes and responses.
    Supports matching with indifference if specified.
    """

    def __init__(
        self,
        nodes: List[Dict[str, Any]],
        responses: List[Dict[str, Any]],
        variance: float = 0.0,
        similarity_func: Callable = cosine_similarity,
    ):
        """
        Initializes the StableMatching class with nodes and responses.

        Args:
        - nodes (List[Dict]): List of nodes with keys 'id', 'prompt', 'embedding'.
        - responses (List[Dict]): List of responses with keys 'id', 'response', 'embedding'.
        - indifference (bool): If True, will include stable matching with indifference. Default is False.
        - variance (float): The range within which scores are considered indifferent. Default is 0.0.
        - similarity_func (Callable): Function to compute similarity, default is cosine similarity.
        """

        self.nodes = nodes
        self.responses = responses
        self.variance = variance
        self.similarity_func = similarity_func

        # Compute similarity scores
        self.similarity_scores = self.compute_similarity_scores()

        # Initialize empty matches and proposals
        self.node_matches = {}
        self.response_matches = {}
        self.node_proposals = {
            node["id"]: [response["id"] for response in responses] for node in nodes
        }

    def compute_similarity_scores(self) -> Dict[Tuple[str, str], float]:
        """
        Computes the similarity scores between nodes and responses.

        Mathematical Notation:
            N: Set of nodes
            R: Set of responses
            s(n, r): Similarity function for node n and response r

        Algorithm:
            1. Initialize similarity_scores as an empty dictionary
            2. For each node n ∈ N and response r ∈ R:
                - Compute s(n, r) and add it to similarity_scores

        Returns:
            - Dict[Tuple[str, str], float]: Dictionary of similarity scores, where each key is a tuple of the node ID and response ID, and the value is the similarity score.
        """

        similarity_scores = {}

        for node in self.nodes:
            for response in self.responses:
                similarity_scores[(node["id"], response["id"])] = self.similarity_func(
                    [node["embedding"]], [response["embedding"]]
                )[0][0]

        return similarity_scores

    def get_matches(self) -> List[Tuple[int, int]]:
        """
        Executes the stable matching algorithm to find optimal pairings, considering the possibility of indifferent preferences within a given variance.

        Mathematical Notation:
            N: Set of nodes
            R: Set of responses
            s(n, r): Similarity function for node n and response r
            v: Indifference variance
            M: Resulting matching

        Algorithm:
            1. Initialize rejected_proposals for all nodes
            2. While node_proposals is not empty:
                - For each node n ∈ N and response r ∈ R:
                    - If |s(n, r) - best_score| <= v (and indifference enabled), consider r as a best response
                    - If s(n, r) > best_score, update best_response with r
                - If best_response is a tuple (indicating indifference), handle each match in best_response
                - Otherwise, handle the single match best_response
            3. Return the resulting matching M

        In accordance with the Indifference Stability Theorem, this algorithm guarantees no blocking pairs, considering indifference within variance v.
        """

        # Keep track of rejected proposals to prevent revisiting them
        rejected_proposals = {node_id: set() for node_id in self.node_proposals.keys()}

        while self.node_proposals:
            node_id, response_ids = self.node_proposals.popitem()
            best_response = None
            best_score = float("-inf")

            # Iterate through response_ids and propose
            for response_id in response_ids:
                if response_id in rejected_proposals[node_id]:
                    continue

                score = self.similarity_scores[(node_id, response_id)]

                if abs(score - best_score) <= self.variance:
                    best_response = (
                        (best_response, response_id)
                        if isinstance(best_response, tuple)
                        else (best_response,) + (response_id,)
                    )
                elif score > best_score:
                    best_response = response_id
                    best_score = score

            # Handle indifferent matches or single match
            if best_response is not None:
                if isinstance(best_response, tuple):
                    for response_id in best_response:
                        success = self.handle_match(node_id, response_id)
                        if not success:
                            rejected_proposals[node_id].add(response_id)
                else:
                    success = self.handle_match(node_id, best_response)
                    if not success:
                        rejected_proposals[node_id].add(best_response)

        return [(node, response) for node, response in self.node_matches.items()]

    def handle_match(self, node_id: str, response_id: str):
        """
        Handles matching between a node (n) and response (r).

        Mathematical Notation:
            N: Set of nodes
            R: Set of responses
            s(n, r): Similarity function for node n and response r
            M: Current matching
            n: Current node being considered
            r: Current response being considered

        Algorithm:
            1. If r is not matched with any node, add the match (n, r) to M
            2. Else:
                - If s(n, r) > s(m, r), where m is the current node matched with r:
                    - Remove match (m, r) from M
                    - Add match (n, r) to M
                    - Allow m to propose again to r
                - Else:
                    - Allow n to propose again to r

        In accordance with the Indifference Stability Theorem, this subalgorithm ensures the best match between nodes and responses, allowing re-proposal as needed.
        """

        if response_id not in self.response_matches:
            self.node_matches[node_id] = response_id
            self.response_matches[response_id] = node_id
        else:
            current_match_score = self.similarity_scores[
                (self.response_matches[response_id], response_id)
            ]
            proposed_match_score = self.similarity_scores[(node_id, response_id)]

            if proposed_match_score > current_match_score:
                old_node = self.response_matches[response_id]
                self.node_matches.pop(old_node)
                self.node_matches[node_id] = response_id
                self.response_matches[response_id] = node_id
                if old_node not in self.node_proposals:
                    self.node_proposals[old_node] = [response_id]
                else:
                    self.node_proposals[old_node].append(
                        response_id
                    )  # Allow old node to propose again
            else:
                if node_id not in self.node_proposals:
                    self.node_proposals[node_id] = [response_id]
                else:
                    self.node_proposals[node_id].append(
                        response_id
                    )  # Allow this node to propose again


def get_node_response_pairs_stable_matching(
    nodes: List[Dict[str, Any]],
    responses: List[Dict[str, Any]],
    variance: float = 0.0,
    similarity_func: Callable = cosine_similarity,
) -> List[Tuple[Dict[str, Any], Dict[str, Any]]]:
    """
    Gets the node-response pairs for the given nodes and responses using stable matching.

    Mathematical Notation:
        N: Set of nodes
        R: Set of responses
        I: Indifference parameter (boolean)
        V: Variance parameter (float)
        s: Similarity function
        P: Stable matching problem defined as (N, R, I, V, s)
        M: Matching as a result of solving P

    Algorithm:
        1. Validate inputs
        2. Initialize stable matching problem P = (N, R, I, V, s)
        3. Execute stable matching algorithm on P to get M
        4. Return M as a list of node-response pairs

    Args:
        - nodes (List[Dict[str, Any]]): List of nodes, each represented by a dictionary with keys:
            - 'id': Unique identifier for the node
            - 'prompt': Prompt associated with the node
            - 'embedding': Embedding vector for the prompt
        - responses (List[Dict[str, Any]]): List of responses, each represented by a dictionary with keys:
            - 'id': Unique identifier for the response
            - 'response': Text of the response
            - 'embedding': Embedding vector for the response
        - indifference (bool): If True, will include stable matching with indifference. Default is False.
        - variance (float): The range within which scores are considered indifferent. Default is 0.0.
        - similarity_func (Callable): Optional. Function to compute similarity, default is cosine similarity.

    Returns:
        - List[Tuple[Dict[str, Any], Dict[str, Any]]]: List of node-response pairs, where each pair is a tuple of the node and response dictionaries.

    Raises:
        - ValueError: If nodes or responses are empty or if there are more nodes than responses.
    """

    # Validate input
    if not nodes or not responses:
        raise ValueError("Nodes and responses must be non-empty lists.")
    if len(nodes) > len(responses):
        raise ValueError("Number of nodes must not exceed the number of responses.")

    # Perform stable matching between nodes and responses using the StableMatching class
    stable_matching = StableMatching(
        nodes, responses, variance=variance, similarity_func=similarity_func
    )
    matches = stable_matching.get_matches()

    # Create dictionaries to facilitate quick lookup of nodes and responses by ID
    node_dict = {node["id"]: node for node in nodes}
    response_dict = {response["id"]: response for response in responses}

    # Get the node-response pairs using the matches and lookup dictionaries
    node_response_pairs = [
        (node_dict[node_id], response_dict[response_id])
        for node_id, response_id in matches
    ]

    # Return the node-response pairs
    return node_response_pairs
