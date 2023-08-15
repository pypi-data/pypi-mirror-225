from typing import Dict, Any, Optional
import numpy as np
import collections
from dl_matrix.relationship import Relationship


class Estimator(Relationship):
    RELATIONSHIPS = {
        "siblings": {
            "weight": 0.11,
        },
        "cousins": {
            "weight": 0.11,
        },
        "uncles_aunts": {
            "weight": 0.11,
        },
        "nephews_nieces": {
            "weight": 0.11,
        },
        "grandparents": {
            "weight": 0.16,
        },
        "ancestors": {
            "weight": 0.2,
        },
        "descendants": {
            "weight": 0.2,
        },
    }

    def __init__(
        self,
        message_dict: Dict[str, Any],
        conversation_dict: Optional[Dict[str, Any]] = None,
    ):
        self.message_dict = message_dict
        self.conversation_dict = conversation_dict

        self._message_references = {msg_id: {} for msg_id in self.message_dict.keys()}
        self._message_tree = None

        self.estimate_history = {
            "baseline": collections.deque(maxlen=100),
            "relationships": collections.deque(maxlen=100),
            "types": collections.deque(maxlen=100),
            "weighted": collections.deque(maxlen=100),
        }
        self.estimate_weights = {
            "baseline": 1.0,
            "relationships": 1.0,
            "types": 1.0,
            "weighted": 1.0,
        }

        self.n_neighbors_weighted = 0

    def update_estimate_history_and_weights(
        self, new_estimates: Dict[str, int]
    ) -> Dict[str, float]:
        """Update the estimate history with new estimates and recalculate the weights."""

        # Update history
        for estimate_type, new_estimate in new_estimates.items():
            if estimate_type in self.estimate_history:
                self.estimate_history[estimate_type].append(new_estimate)
            else:
                raise ValueError(f"Invalid estimate type: {estimate_type}")

        # Recalculate weights based on history
        for estimate_type, history in self.estimate_history.items():
            mean_estimate = np.mean(history)
            if mean_estimate > 0:
                self.estimate_weights[estimate_type] = 1 / mean_estimate
            else:
                # Handle division by zero: if mean estimate is zero, set weight to zero
                self.estimate_weights[estimate_type] = 0.0

        # Normalize weights so they sum to 1
        total_weight = sum(self.estimate_weights.values())
        if total_weight > 0:
            self.estimate_weights = {
                k: v / total_weight for k, v in self.estimate_weights.items()
            }
        else:
            # Handle division by zero: if total weight is zero, set all weights to equal values
            self.estimate_weights = {
                k: 1.0 / len(self.estimate_weights) for k in self.estimate_weights
            }

        return self.estimate_weights

    def determine_n_neighbors(self, message_id: str) -> int:
        """Calculate the number of neighbors based on message relationships."""

        message_data = self.message_dict.get(message_id)
        if message_data is None:
            raise ValueError(
                f"Message ID {message_id} not found in message dictionary."
            )

        # Get all relationships for the message
        relationship_dict = self.get_relationship(message_id)

        # Compute baseline n_neighbors
        n_neighbors_baseline = int(np.sqrt(len(self.message_dict)))

        # Compute n_neighbors based on the size of the largest relationship
        n_neighbors_relationships = max(len(v) for v in relationship_dict.values())

        # Compute n_neighbors based on the number of different relationship types
        n_neighbors_types = len([k for k, v in relationship_dict.items() if v])

        # Compute n_neighbors based on the weighted size of each relationship
        n_neighbors_weighted = sum(
            self.RELATIONSHIPS[rel_type]["weight"] * len(rel)
            for rel_type, rel in relationship_dict.items()
        )

        # Formulate new estimates
        new_estimates = {
            "baseline": n_neighbors_baseline,
            "relationships": n_neighbors_relationships,
            "types": n_neighbors_types,
            "weighted": n_neighbors_weighted,
        }

        # Update estimate history and recalculate weights
        self.update_estimate_history_and_weights(new_estimates)

        # Compute weighted n_neighbors
        self.n_neighbors_weighted = int(
            sum(
                self.estimate_weights[estimate_type] * new_estimate
                for estimate_type, new_estimate in new_estimates.items()
            )
        )

        estimate = int(
            sum(new_estimates[estimate_type] for estimate_type in new_estimates.keys())
        ) // len(new_estimates)

        return estimate
