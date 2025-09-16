from datetime import timedelta

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0,
                 arrival_time=None, total_km=0, total_delay=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.arrival_time = arrival_time
        self.total_km = total_km
        self.total_delay = total_delay


    def __repr__(self):
        return f"<{self.state}, {self.total_km:.3f}km, delay={self.total_delay}m>"


    def __lt__(self, other):
        return self.path_cost < other.path_cost

    def get_total_time_minutes(self):

        return self.path_cost / 60.0


    def get_path_nodes(self):

        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]

    def get_path_states(self):

        return [node.state for node in self.get_path_nodes()]

    def is_failure(self):

        return self == cutoff or self == failure

    def get_total_delay_minutes(self):

        return self.total_delay


cutoff = Node('cutoff', path_cost=float('inf'))
failure = Node('failure', path_cost=float('inf'))


def expand(problem, node, all_blocked=None):
    if all_blocked is None:
        all_blocked = set()
    for s1 in problem.actions(node.state):
        km = problem.map.get_distance(node.state, s1)
        if km is None:
            continue


        if node.arrival_time and problem.traffic_conditions:
            if problem.traffic_conditions.is_closed(node.state, s1, node.arrival_time.time()):
                all_blocked.add(f"{node.state}-{s1}")
                continue


        base_time_sec = (km / 20.0) * 60 * 60


        delay = 0
        if node.arrival_time and problem.traffic_conditions:
            delay = problem.traffic_conditions.get_traffic_delay(node.state, s1, node.arrival_time.time())
        total_time_sec = base_time_sec + delay*60
        arrival_time = node.arrival_time + timedelta(seconds=total_time_sec) if node.arrival_time else None

        yield Node(
            state=s1,
            parent=node,
            action=s1,
            path_cost=node.path_cost + total_time_sec,
            arrival_time=arrival_time,
            total_km=node.total_km + km,
            total_delay=node.total_delay + delay
        )



def path_states(node):
    if node in (failure, None):
        return []
    if isinstance(node, list):
        return node
    return path_states(node.parent) + [node.state]


def path_with_roads(node, road_names):

    states = path_states(node)
    path_info = []
    for i in range(len(states) - 1):
        a, b = states[i], states[i + 1]
        road = road_names.get((a, b), road_names.get((b, a), "???"))
        path_info.append((a, b, road))
    return path_info