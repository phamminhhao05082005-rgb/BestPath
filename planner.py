from searches import (
    uniform_cost_search,
    astar_search,
    greedy_search,
    breadth_first_search,
    depth_first_search
)
from trees import failure, path_states, path_with_roads
from logger import Logger
from roads import road_names

class SmartPlanner:
    def __init__(self, problem, preference):
        self.problem = problem
        self.preference = preference
        self.logger = Logger("log.txt")


        self.algorithms = {
            "UCS": uniform_cost_search,
            "A*": astar_search,
            "Greedy": greedy_search,
            "BFS": breadth_first_search,
            "DFS": depth_first_search
        }

    def _evaluate(self, result):

        if self.preference == "distance":
            return result.total_km
        elif self.preference == "time":
            return result.path_cost
        elif self.preference == "delay":
            return result.total_delay
        else:
            return result.total_km

    def plan(self):
        results = []

        for name, algo in self.algorithms.items():
            try:
                result, blocked = algo(self.problem)
                results.append((name, result if result != failure else failure, blocked))
            except Exception:
                results.append((name, failure, set()))

        if not results:
            print("Không có thuật toán nào tìm được đường đi.")
            return failure

        valid_results = [(n, r, b) for n, r, b in results if r != failure]
        if not valid_results:
            print("Không tìm thấy hành trình phù hợp.")
            return failure


        metrics = {
            "time": lambda r: r[1].path_cost,
            "distance": lambda r: r[1].total_km,
            "delay": lambda r: r[1].total_delay
        }

        all_keys = ["time", "distance", "delay"]
        ordered = [self.preference] + [k for k in all_keys if k != self.preference]


        def key_func(r):
            return tuple(metrics[k](r) for k in ordered)

        best_name, best_result, best_blocked = min(valid_results, key=key_func)

        print(f"Thuật toán được chọn theo tiêu chí '{self.preference}': {best_name}")
        self.print_result(best_result)

        self.logger.log_result(self.problem, results, best_name, best_result, self.preference)

        return best_result, results

    NODE_NAMES = {
        'B': 'Bảo Tàng HCM',
        'C': 'CV Tao Đàn',
        'D': 'Dinh Độc Lập',
        'SG': 'SG CENTRE',
        'Be': 'Chợ Bến Thành'
    }

    def print_result(self, result):

        path_named = [self.NODE_NAMES.get(node, node) for node in path_states(result)]
        print("🗺 Hành trình:", path_named)
        print("Chi tiết:")
        for a, b, road in path_with_roads(result, road_names):
            a_name = self.NODE_NAMES.get(a, a)
            b_name = self.NODE_NAMES.get(b, b)
            print(f"  {a_name} → {b_name} qua {road}")

        total_seconds = int(result.path_cost)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        print(f"Tổng thời gian: {hours:02d}:{minutes:02d}:{seconds:02d}")
        print(f"Tổng quãng đường (km): {result.total_km:.3f}")
        print(f"Tổng delay do kẹt xe: {result.total_delay:.2f} phút")