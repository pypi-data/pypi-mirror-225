import numpy as np
from typing import List, Tuple, Dict, Any, Union
from sklearn.cluster import DBSCAN
from datetime import timedelta


class SimplicialChainIndex:
    def __init__(self, conversation_tree: Dict[str, List[Any]], max_dimension: int = 3):
        """
        Creates a simplicial complex index for a conversation tree.

        Args:
            conversation_tree: A dictionary of lists containing messages.
        """

        self.conversation_tree = conversation_tree
        self.max_dimension = max_dimension
        self.vertex_to_index = {}
        self.index_to_vertex = []
        self.edge_to_index = {}
        self.index_to_edge = []
        self.index_simplices = []
        self.index_map = [{}]
        self.num_vertices = 0
        try:
            self._create_index()
        except ValueError as e:
            print(f"Error: {str(e)}")
            return None

    def _temporal_weight(self, delta_time: timedelta) -> float:
        """Compute a temporal weight based on the time difference."""
        decay_rate = 1.0  # tune this as per requirements
        return np.exp(-decay_rate * delta_time)

    def _create_index(self):
        """
        Creates indices for vertices (messages), edges (replies), and higher-dimensional simplices
        based on temporal relationships.
        """

        # Create index for vertices
        messages = list(self.conversation_tree.conversation.mapping.values())
        seen_messages = set()
        self.index_to_vertex = [
            message.id
            for message in messages
            if message.id not in seen_messages and not seen_messages.add(message.id)
        ]
        self.vertex_to_index = {
            vertex: index for index, vertex in enumerate(self.index_to_vertex)
        }

        # Create index for edges
        seen_edges = set()
        edges = [
            (message.parent, message.id)
            for message in messages
            if message.parent is not None
            and message.parent != message.id
            and not seen_edges.add(
                frozenset(
                    [
                        self.vertex_to_index[message.parent],
                        self.vertex_to_index[message.id],
                    ]
                )
            )
        ]
        self.index_to_edge = [
            tuple(sorted([self.vertex_to_index[parent], self.vertex_to_index[child]]))
            for parent, child in edges
        ]
        self.edge_to_index = {
            edge: index for index, edge in enumerate(self.index_to_edge)
        }

        # Calculate temporal weights matrix
        num_messages = len(messages)
        temporal_weights = np.zeros((num_messages, num_messages))
        for i in range(num_messages):
            for j in range(i + 1, num_messages):
                if messages[i].parent == messages[j].parent:
                    delta_time = abs(
                        messages[i].message.create_time
                        - messages[j].message.create_time
                    )
                    temporal_weights[i, j] = self._temporal_weight(delta_time)
                    temporal_weights[j, i] = temporal_weights[i, j]

        # Clustering based on temporal weights
        clustering = DBSCAN(metric="precomputed", min_samples=3, eps=0.5).fit(
            1 - temporal_weights
        )

        # Convert clusters to simplices
        self.index_simplices = []
        for label in set(clustering.labels_):
            if label != -1:  # Ignore noise (-1)
                members = np.where(clustering.labels_ == label)[0]
                if len(members) > 2:  # At least a 2-simplex
                    simplex = sorted(
                        [self.vertex_to_index[messages[i].id] for i in members]
                    )
                    self.index_simplices.append(np.array(simplex))

        # Create index map for vertices, edges, and simplices
        self.index_map = [{} for _ in range(3)]
        self.index_map[0] = {
            vertex: index for index, vertex in enumerate(self.index_to_vertex)
        }
        self.index_map[1] = {
            edge: index for index, edge in enumerate(self.index_to_edge)
        }
        self.index_map[2] = {
            simplex: index for index, simplex in enumerate(self.index_simplices)
        }

        self.max_dimension = (
            2 if self.index_simplices else 1
        )  # adjust based on the highest dimension present

        self.num_vertices = len(self.index_to_vertex)

    def get_index(self, simplex: List[str]) -> Union[int, None]:
        """
        Retrieves the index of a given simplex.

        Args:
        - simplex (List[str]): The simplex represented as a list of vertex identifiers.

        Returns:
        - Union[int, None]: The index of the simplex or None if the simplex is not present.
        """
        if len(simplex) == 1:
            return self.vertex_to_index.get(simplex[0], None)
        elif len(simplex) == 2:
            return self.edge_to_index.get(tuple(sorted(simplex)), None)
        else:
            return self.index_map[2].get(tuple(sorted(simplex)), None)

    def get_simplex(self, index: int) -> Union[List[str], None]:
        """
        Retrieves the simplex corresponding to a given index.

        Args:
        - index (int): The index of the target simplex.

        Returns:
        - Union[List[str], None]: The simplex represented as a list of vertex identifiers
          or None if the index is invalid.
        """
        if index < 0 or index >= len(self.index_simplices):
            return None
        return [
            self.index_to_vertex[vertex_index]
            for vertex_index in self.index_simplices[index]
        ]

    def get_max_dimension(self) -> int:
        """
        Returns the maximum dimension of the simplicial complex.

        Returns:
        - int: The maximum dimension of the simplicial complex.
        """
        return self.max_dimension

    def get_edges(self) -> List[Tuple[str, str]]:
        """
        Retrieves all edges of the simplicial complex.

        Returns:
        - List[Tuple[str, str]]: A list of edges, each represented as a tuple of two vertex identifiers.
        """
        return [
            (self.index_to_vertex[edge[0]], self.index_to_vertex[edge[1]])
            for edge in self.index_to_edge
        ]

    def get_simplices(self) -> List[List[str]]:
        """
        Retrieves all simplices of the simplicial complex.

        Returns:
        - List[List[str]]: A list of simplices, each represented as a list of vertex identifiers.
        """
        return [
            [self.index_to_vertex[vertex_index] for vertex_index in simplex]
            for simplex in self.index_simplices
        ]

    def get_simplex_indices(self, vertex_id: str) -> List[int]:
        """
        Retrieves indices of all simplices containing a given vertex.

        Args:
        - vertex_id (str): Identifier of the target vertex.

        Returns:
        - List[int]: List of indices of simplices that contain the target vertex.
        """
        vertex_index = self.vertex_to_index.get(vertex_id)
        if vertex_index is None:
            return []
        else:
            return [
                i
                for i, simplex in enumerate(self.index_simplices)
                if vertex_index in simplex
            ]

    def get_neighbors(self, vertex_id: str) -> List[str]:
        """
        Retrieves the neighboring vertices of a given vertex.

        Args:
        - vertex_id (str): Identifier of the target vertex.

        Returns:
        - List[str]: List of identifiers of vertices that are neighbors of the target vertex.
        """
        vertex_index = self.vertex_to_index.get(vertex_id)
        if vertex_index is None:
            return []
        else:
            neighbor_indices = [
                edge[1] if edge[0] == vertex_index else edge[0]
                for edge in self.index_to_edge
                if vertex_index in edge
            ]
            return [self.index_to_vertex[index] for index in neighbor_indices]

    def get_degree(self, vertex_id: str) -> int:
        """
        Retrieves the degree of a given vertex.

        Args:
        - vertex_id (str): Identifier of the target vertex.

        Returns:
        - int: The degree of the vertex.
        """
        vertex_index = self.vertex_to_index.get(vertex_id)
        if vertex_index is None:
            return 0
        else:
            return sum(1 for edge in self.index_to_edge if vertex_index in edge)

    def get_neighbors_count(self, vertex_id: str) -> int:
        """
        Retrieves the number of neighboring vertices of a given vertex.

        Args:
        - vertex_id (str): Identifier of the target vertex.

        Returns:
        - int: The number of neighbors of the vertex.
        """
        vertex_index = self.vertex_to_index.get(vertex_id)
        if vertex_index is None:
            return 0
        else:
            return sum(1 for edge in self.index_to_edge if vertex_index in edge)

    def get_adjacent_vertices(self, vertex_id: str) -> List[str]:
        """
        Returns the vertices adjacent to a given vertex.

        Args:
        - vertex_id (str): The ID of the target vertex.

        Returns:
        - List[str]: A list of adjacent vertices' IDs.
        """
        vertex_index = self.vertex_to_index.get(vertex_id)
        if vertex_index is None:
            return []

        neighbor_indices = [
            edge[1] if edge[0] == vertex_index else edge[0]
            for edge in self.index_to_edge
            if vertex_index in edge
        ]

        return [self.index_to_vertex[index] for index in neighbor_indices]

    def get_vertex_degree(self, vertex_id: str) -> int:
        """
        Returns the degree of a given vertex.

        Args:
        - vertex_id (str): The ID of the target vertex.

        Returns:
        - int: The degree of the vertex.
        """
        vertex_index = self.vertex_to_index.get(vertex_id)
        if vertex_index is None:
            return 0
        else:
            return sum(1 for edge in self.index_to_edge if vertex_index in edge)

    def get_edge_length(self, parent_id: str, child_id: str) -> int:
        """
        Returns the length of the edge between the specified parent and child vertices.

        Args:
        - parent_id (str): The ID of the parent vertex.
        - child_id (str): The ID of the child vertex.

        Returns:
        - int: The length of the edge.
        """
        parent_index = self.vertex_to_index.get(parent_id)
        child_index = self.vertex_to_index.get(child_id)
        if parent_index is None or child_index is None:
            return 0
        else:
            edge = tuple(sorted([parent_index, child_index]))
            if edge in self.edge_to_index:
                return len(self.index_to_edge[self.edge_to_index[edge]])
            else:
                return 0

    def get_vertex_index(self, message_id: str) -> Union[int, None]:
        """
        Returns the index associated with the given vertex ID.

        Args:
        - message_id (str): The ID of the vertex.

        Returns:
        - int, None: The index of the vertex or None if not found.
        """
        return self.vertex_to_index.get(message_id)

    def get_edge_index(self, parent_id: str, child_id: str) -> Union[int, None]:
        """
        Returns the index associated with the edge connecting the specified parent and child vertices.

        Args:
        - parent_id (str): The ID of the parent vertex.
        - child_id (str): The ID of the child vertex.

        Returns:
        - int, None: The index of the edge or None if not found.
        """
        parent_index = self.vertex_to_index.get(parent_id, -1)
        child_index = self.vertex_to_index.get(child_id, -1)
        if parent_index == -1 or child_index == -1:
            return None
        edge = tuple(sorted([parent_index, child_index]))
        return self.edge_to_index.get(edge, None)

    def get_vertex(self, index: int) -> Union[str, None]:
        """
        Returns the vertex ID associated with the given index.

        Args:
        - index (int): The index of the vertex.

        Returns:
        - str, None: The ID of the vertex or None if not found.
        """
        if index < 0 or index >= len(self.index_to_vertex):
            return None
        return self.index_to_vertex[index]

    def get_edge(self, index: int) -> Union[Tuple[str, str], None]:
        """
        Returns the edge (as a tuple of vertex IDs) associated with the given index.

        Args:
        - index (int): The index of the edge.

        Returns:
        - Tuple[str, str], None: The edge as a tuple of vertex IDs or None if not found.
        """
        if index < 0 or index >= len(self.index_to_edge):
            return None
        edge = self.index_to_edge[index]
        parent_id = self.index_to_vertex[edge[0]]
        child_id = self.index_to_vertex[edge[1]]
        return parent_id, child_id

    def get_boundary_matrix(self, k: int) -> List[List[int]]:
        """
        Return the boundary matrix of the k-th dimension simplicial complex.

        The boundary matrix indicates the boundary of each k-simplex as a linear combination of
        the (k-1)-simplices. Each row corresponds to a k-simplex, and each column corresponds to a
        (k-1)-simplex. The entry in row i and column j is the coefficient of the j-th (k-1)-simplex
        in the boundary of the i-th k-simplex.

        Args:
        - k (int): The dimension of interest.

        Returns:
        - List[List[int]]: The boundary matrix of the k-th dimension simplicial complex.
        """
        if k > self.max_dimension:
            raise ValueError(f"Invalid k {k} for max dimension {self.max_dimension}")
        num_k_simplices = len(self.index_simplices[k])
        num_k_minus_one_simplices = len(self.index_simplices[k - 1])
        matrix = [[0] * num_k_minus_one_simplices for _ in range(num_k_simplices)]
        for i, simplex in enumerate(self.index_simplices[k]):
            for j, face in enumerate(self.get_boundary(k, simplex)):
                sign = (-1) ** j
                face_index = self.index_map[k - 1][tuple(sorted(face))]
                matrix[i][face_index] = sign
        return matrix

    def get_neighborhood(self, vertex_id: str, radius: int) -> List[str]:
        """
        Returns the neighborhood of a given vertex.

        The neighborhood of a vertex is the set of vertices that are at most a given radius
        away from the vertex. The radius is defined as the number of edges in the shortest
        path between the vertex and the other vertex.

        Args:
        - vertex_id (str): Identifier of the target vertex.
        - radius (int): The radius of the neighborhood.

        Returns:
        - List[str]: A list of identifiers of vertices that are in the neighborhood of the target vertex.
        """
        vertex_index = self.vertex_to_index.get(vertex_id)
        if vertex_index is None:
            return []
        else:
            neighborhood_indices = set()
            frontier = {vertex_index}
            for _ in range(radius):
                new_frontier = set()
                for v in frontier:
                    for edge in self.index_to_edge:
                        if v in edge:
                            neighbor_index = edge[1] if v == edge[0] else edge[0]
                            if neighbor_index not in neighborhood_indices:
                                neighborhood_indices.add(neighbor_index)
                                new_frontier.add(neighbor_index)
                frontier = new_frontier
            return [self.index_to_vertex[index] for index in neighborhood_indices]

    def get_boundary_operator(self, k: int) -> List[List[int]]:
        """
        Computes the boundary operator for the \( k \)-th chain group of the simplicial complex.

        The boundary operator maps \( k \)-chains to their \( (k-1) \)-chain boundaries.
        The resulting matrix represents this mapping, with each row corresponding to a \( (k-1) \)-simplex,
        and each column to a \( k \)-simplex. The matrix entry at [i, j] specifies how \( k \)-simplex j
        contributes to the boundary of \( (k-1) \)-simplex i.

        Args:
        - k (int): The dimension of the chain group for which the boundary operator is to be computed.

        Returns:
        - List[List[int]]: The boundary operator as a list of lists.
        """
        if k < 1 or k > self.max_dimension:
            return None

        if k == 1:
            # The boundary operator for 1-chains is just the edge-to-vertex incidence matrix.
            # The entry in row i and column j is 1 if vertex j is an endpoint of edge i, and 0 otherwise.
            return [
                [1 if j in edge else 0 for j in range(self.num_vertices)]
                for edge in self.index_simplices
            ]

        # To compute the boundary operator for higher dimensional chains, we first need to compute the boundary matrix
        # for the (k-1)-dimensional simplicial complex.
        boundary_matrix = self.get_boundary_matrix(k - 1)

        # The transpose of the boundary matrix is the matrix that maps k-chains to (k-1)-chains.
        boundary_operator = [
            [0 for j in range(len(self.index_simplices))]
            for i in range(len(boundary_matrix[0]))
        ]
        for i in range(len(boundary_matrix)):
            for j in range(len(boundary_matrix[0])):
                if boundary_matrix[i][j] != 0:
                    for l in range(len(self.index_simplices)):
                        if j in self.index_simplices[l]:
                            boundary_operator[l][i] = boundary_matrix[i][j]

        return boundary_operator

    def get_coboundary_matrix(self, k: int) -> List[List[int]]:
        """
        Return the coboundary matrix of the k-th dimension simplicial complex.

        The coboundary matrix is the transpose of the boundary matrix and indicates the coboundary
        of each (k-1)-simplex as a linear combination of the k-simplices. Each row corresponds to a
        (k-1)-simplex, and each column corresponds to a k-simplex. The entry in row i and column j
        is the coefficient of the j-th k-simplex in the coboundary of the i-th (k-1)-simplex.

        Args:
        - k (int): The dimension of interest.

        Returns:
        - List[List[int]]: The coboundary matrix of the k-th dimension simplicial complex.
        """
        if k > self.max_dimension or k < 1:
            raise ValueError(f"Invalid k {k} for max dimension {self.max_dimension}")
        num_k_simplices = len(self.index_simplices[k])
        num_k_minus_one_simplices = len(self.index_simplices[k - 1])
        matrix = [[0] * num_k_simplices for _ in range(num_k_minus_one_simplices)]
        for i, face in enumerate(self.index_simplices[k - 1]):
            for j, simplex in enumerate(self.get_star(k - 1, face)):
                sign = (-1) ** j
                simplex_index = self.index_map[k][tuple(sorted(simplex))]
                matrix[i][simplex_index] = sign
        return matrix

    def get_homology(self, k: int) -> List[Tuple[int, int]]:
        """
        Return the k-th homology group of the simplicial complex.

        The k-th homology group represents the group of k-dimensional holes in the complex.
        Each element of the homology group is represented as a pair of integers (betti number, rank),
        where betti number is the number of k-dimensional holes and rank is the dimension of the
        vector space of cycles modulo boundaries.

        Args:
        - k (int): The dimension of interest.

        Returns:
        - List[Tuple[int, int]]: The k-th homology group as a list of (betti number, rank) pairs.
        """
        if k > self.max_dimension:
            raise ValueError(f"Invalid k {k} for max dimension {self.max_dimension}")
        boundary_matrix = self.get_boundary_matrix(k)
        coboundary_matrix = self.get_coboundary_matrix(k + 1)
        nullity = len(boundary_matrix) - np.linalg.matrix_rank(boundary_matrix)
        nullity_co = len(coboundary_matrix) - np.linalg.matrix_rank(coboundary_matrix)

        betti_number = nullity - nullity_co
        return [(betti_number, np.linalg.matrix_rank(boundary_matrix))]

    def get_connected_components(self) -> List[List[str]]:
        """
        Return the connected components of the simplicial complex.

        A connected component is a maximal set of simplices that are pairwise connected,
        meaning that there exists a sequence of simplices such that each pair of consecutive
        simplices share a common face. This method can be useful for understanding the global
        structure of a simplicial complex.

        Returns:
        - List[List[str]]: A list of connected components, where each component is a list of simplices.
        """
        # Convert index simplices to a set of tuples for faster lookup
        simplices_set = {tuple(simplex) for simplex in self.index_simplices}

        # Initialize empty list to store connected components
        connected_components = []

        # Initialize set of visited vertices
        visited_vertices = set()

        # Loop through all vertices
        for vertex in self.index_to_vertex:
            # If the vertex has not been visited, it must belong to a new connected component
            if vertex not in visited_vertices:
                # Initialize a new connected component
                component = []
                # Add the vertex to the connected component and mark it as visited
                component.append(vertex)
                visited_vertices.add(vertex)
                # Initialize a set of frontier vertices
                frontier = {vertex}
                # Loop through the frontier vertices and add their neighbors to the connected component
                while frontier:
                    # Remove a vertex from the frontier
                    v = frontier.pop()
                    # Loop through the edges incident to v using the set for efficient lookup
                    for simplex in (s for s in simplices_set if v in s):
                        # Get the neighbor vertex
                        neighbor = next(x for x in simplex if x != v)
                        # If the neighbor has not been visited, add it to the connected component and mark it as visited
                        if neighbor not in visited_vertices:
                            component.append(neighbor)
                            visited_vertices.add(neighbor)
                            # Add the neighbor to the frontier
                            frontier.add(neighbor)
                # Add the connected component to the list of connected components
                connected_components.append(component)

        return connected_components

    def get_filtration(self) -> List[List[str]]:
        """
        Returns a filtration of the simplicial complex.

        A filtration is an ordered list of simplices where each simplex and all its faces are added
        before the next simplex in the list. This method can be useful for understanding the
        incremental building of a simplicial complex.

        Returns:
        - List[List[str]]: An ordered list of simplices representing the filtration.
        """
        simplices = []
        for k in range(self.max_dimension + 1):
            for simplex in self.index_simplices[k]:
                if simplex not in simplices:
                    simplices.append(simplex)
        return simplices

    def get_closure(self, simplex: List[str]) -> List[List[str]]:
        """
        Returns the closure of a given simplex.

        The closure of a simplex is the union of the simplex with all of its faces.
        This method can be useful for understanding the substructure of a given simplex
        in the complex.

        Args:
        - simplex (List[str]): The target simplex.

        Returns:
        - List[List[str]]: A list of simplices representing the closure.
        """
        closure = []
        for k in range(len(simplex), self.max_dimension + 1):
            for candidate_simplex in self.index_simplices[k]:
                if set(simplex).issubset(candidate_simplex):
                    if candidate_simplex not in closure:
                        closure.append(candidate_simplex)
        return closure

    def get_star(self, simplex: List[str]) -> List[List[str]]:
        """
        Returns the star of a given simplex.

        The star of a simplex is the collection of all simplices that have the given simplex
        as a face. This method can be useful for understanding the local neighborhood
        around a given simplex.

        Args:
        - simplex (List[str]): The target simplex.

        Returns:
        - List[List[str]]: A list of simplices representing the star.
        """
        star = []
        for k in range(len(simplex) + 1):
            for candidate_simplex in self.index_simplices[k]:
                if set(simplex).issubset(candidate_simplex):
                    if candidate_simplex not in star:
                        star.append(candidate_simplex)
        return star

    def get_link(self, simplex: List[str]) -> List[List[str]]:
        """
        Returns the link of a given simplex.

        The link of a simplex consists of all simplices that are disjoint from the simplex
        but share a common boundary. This method can be useful for understanding the relation
        of a simplex with other simplices that don't share vertices with it but are
        topologically adjacent.

        Args:
        - simplex (List[str]): The target simplex.

        Returns:
        - List[List[str]]: A list of simplices representing the link.
        """
        link = []
        for k in range(len(simplex) + 1, self.max_dimension + 1):
            for candidate_simplex in self.index_simplices[k]:
                if set(simplex).intersection(candidate_simplex) == set(simplex):
                    if candidate_simplex not in link:
                        link.append(candidate_simplex)
        return link

    def get_boundary(self, simplex: List[str]) -> List[List[str]]:
        """
        Returns the boundary of a given simplex.

        The boundary of a simplex is the set of its proper faces. This method can be useful
        for understanding the outer shell or border of a given simplex in the complex.

        Args:
        - simplex (List[str]): The target simplex.

        Returns:
        - List[List[str]]: A list of simplices representing the boundary.
        """
        boundary = []
        for k in range(len(simplex) + 1):
            for candidate_simplex in self.index_simplices[k]:
                if set(simplex).issubset(candidate_simplex):
                    if candidate_simplex not in boundary:
                        boundary.append(candidate_simplex)
        return boundary
