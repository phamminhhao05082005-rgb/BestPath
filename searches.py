import heapq
import math
from collections import deque
from datetime import datetime
from trees import Node, failure, cutoff, expand

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

def uniform_cost_search(problem):
    all_blocked = set()
    initial_node = Node(state=problem.initial, arrival_time=datetime.combine(datetime.today(), problem.start_time))
    frontier = PriorityQueue([initial_node], key=lambda n: n.path_cost)
    explored = set()
    while frontier:
        node = frontier.pop()
        if node.state in explored:
            continue
        if problem.is_goal(node.state):
            return node, all_blocked
        explored.add(node.state)
        for child in expand(problem, node, all_blocked):
            if child.state not in explored and child not in frontier:
                frontier.add(child)
    return failure, all_blocked

def astar_search(problem):
    all_blocked = set()
    def f(n):
        return n.path_cost + problem.h(n)
    initial_node = Node(state=problem.initial, arrival_time=datetime.combine(datetime.today(), problem.start_time))
    frontier = PriorityQueue([initial_node], key=f)
    explored = set()
    while frontier:
        node = frontier.pop()
        if node.state in explored:
            continue
        if problem.is_goal(node.state):
            return node, all_blocked
        explored.add(node.state)
        for child in expand(problem, node, all_blocked):
            if child.state not in explored and child not in frontier:
                frontier.add(child)
    return failure, all_blocked

def greedy_search(problem):
    all_blocked = set()
    initial_node = Node(state=problem.initial, arrival_time=datetime.combine(datetime.today(), problem.start_time))
    frontier = PriorityQueue([initial_node], key=problem.h)
    explored = set()
    while frontier:
        node = frontier.pop()
        if node.state in explored:
            continue
        if problem.is_goal(node.state):
            return node, all_blocked
        explored.add(node.state)
        for child in expand(problem, node, all_blocked):
            if child.state not in explored and child not in frontier:
                frontier.add(child)
    return failure, all_blocked

def breadth_first_search(problem):
    all_blocked = set()
    initial_node = Node(state=problem.initial, arrival_time=datetime.combine(datetime.today(), problem.start_time))
    frontier = deque([initial_node])
    explored = set()
    while frontier:
        node = frontier.popleft()
        if problem.is_goal(node.state):
            return node, all_blocked
        explored.add(node.state)
        for child in expand(problem, node, all_blocked):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
    return failure, all_blocked

def depth_first_search(problem):
    all_blocked = set()
    initial_node = Node(state=problem.initial, arrival_time=datetime.combine(datetime.today(), problem.start_time))
    frontier = [initial_node]  # Stack
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node, all_blocked
        explored.add(node.state)
        for child in expand(problem, node, all_blocked):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
    return failure, all_blocked