from collections import defaultdict

class Map:
    def __init__(self, distance_km, locations=None, directed=True):

        if not directed:
            sym = {}
            for (a, b), km in distance_km.items():
                sym[a, b] = km
                sym[b, a] = km
            distance_km = sym

        self.distance_km = distance_km
        self.locations = locations or {}
        self.directed = directed


        self._neighbors = defaultdict(list)
        for (a, b) in self.distance_km.keys():
            self._neighbors[a].append(b)

    def neighbors(self, state):

        return self._neighbors.get(state, [])

    def get_distance(self, a, b):

        return self.distance_km.get((a, b))