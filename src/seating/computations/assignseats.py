import numpy as np
import networkx as nx

from ..models import Person


class SeatAssigner:
    """Assign seats to people."""
    def __init__(self):
        """
        Builds a graph that shows who can sit next to who.

        The people are the vertices. There is an edge between two people if they are
        allowed to sit next to each other.
        """
        # Get all the people currently in the database.
        self.people = Person.objects.all()
        # Create a complete graph with all the people connected to everyone.
        self.graph = nx.complete_graph(self.people)
        # Retrieve the set of all forbidden edges.
        self.forbidden = self.get_all_forbidden_edges()
        # Remove the forbidden edges from the graph.
        self.graph.remove_edges_from(self.forbidden)

    def valid_seats(self) -> [Person]:
        """
        'Computes' a valid seat arrangement.

        :return: A list of people who are all allowed to sit next to each other. One
            could put the people around the table in this order.
        """
        # Initial shuffling of people.
        random = np.random.permutation(self.people)

        # Keep shuffling until we find a valid order.
        while not self.is_valid(path=random):
            random = np.random.permutation(random)
        return random

    def is_valid(self, path) -> bool:
        """
        Tests if the current path is a valid seating order, by checking if all edges
        are in the graph.

        :return: True if this is a valid seating arrangement, false otherwise.
        """
        return all([(path[i], path[(i+1) % len(path)]) in self.graph.edges() for i in range(len(path))])

    def get_all_forbidden_edges(self) -> [(Person, Person)]:
        """Get all the forbidden neighbor pairs from the database."""
        return list(set([
            (p, it) for p in self.people
            for it in list(p.forbidden_neighbors.all())
        ]))

