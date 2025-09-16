import heapq
import math

def euclidean_distance(A, B):
    return math.sqrt(sum((a - b) ** 2 for (a, b) in zip(A, B)))

class PriorityQueue:
    def __init__(self, nodes=(), key=lambda x: x):
        self.nodes = []
        self.key = key
        for node in nodes:
            self.add(node)

    def add(self, node):
        pair = (self.key(node), node)
        heapq.heappush(self.nodes, pair)

    def pop(self):
        return heapq.heappop(self.nodes)[1]

    def __contains__(self, item):
        return any(n[1] == item for n in self.nodes)

    def __len__(self):
        return len(self.nodes)