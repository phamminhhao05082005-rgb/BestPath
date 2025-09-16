from datetime import time

class TrafficCondition:
    def __init__(self):
        self.conditions = {}
        self.closures = {}

    def add_peak_hour(self, a, b, start_time, end_time, delay_minutes):

        for edge in [(a, b), (b, a)]:
            if edge not in self.conditions:
                self.conditions[edge] = []
            self.conditions[edge].append((start_time, end_time, delay_minutes))

    def add_road_closure(self, a, b, start_time, end_time):

        for edge in [(a, b), (b, a)]:
            if edge not in self.closures:
                self.closures[edge] = []
            self.closures[edge].append((start_time, end_time))

    def get_traffic_delay(self, a, b, current_time):

        conds = self.conditions.get((a, b), [])
        for (start, end, delay) in conds:
            if start <= current_time <= end:
                return delay
        return 0

    def is_closed(self, a, b, current_time):

        conds = self.closures.get((a, b), [])
        for (start, end) in conds:
            if start <= current_time <= end:
                return True
        return False