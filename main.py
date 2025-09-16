from maps import Map
from problems import RouteProblem
from trafficCondition import TrafficCondition
from planner import SmartPlanner
from visualizeMap import visualize_map
from excelLogger import ExcelLogger
from trees import path_states, failure
from searches import (
    breadth_first_search,
    depth_first_search,
    uniform_cost_search,
    greedy_search,
    astar_search
)
from trees import path_states
from datetime import time


def create_map():

    return Map(
        distance_km={
            ('SG', 'C47'): 0.020,
            ('B', 'C17'): 0.052, ('Be', 'C13'): 0.060,
            ('D', 'C34'): 0.143, ('D', 'C39'): 0.077,
            ('C', 'C41'): 0.157,
            ('C01', 'C02'): 0.084, ('C01', 'C04'): 0.126,
            ('C02', 'C06'): 0.124, ('C02', 'C09'): 0.062, ('C02', 'C19'): 0.125,
            ('C03', 'C01'): 0.138, ('C03', 'C17'): 0.132,
            ('C04', 'C05'): 0.031, ('C04', 'C48'): 0.051,
            ('C05', 'C07'): 0.157, ('C05', 'C09'): 0.053, ('C05', 'C48'): 0.046,
            ('C06', 'C08'): 0.083, ('C06', 'C20'): 0.053,
            ('C07', 'C08'): 0.062, ('C07', 'C15'): 0.105, ('C07', 'Be'): 0.057,
            ('C08', 'C09'): 0.137,
            ('C09', 'C02'): 0.062, ('C09', 'C05'): 0.053,
            ('C10', 'C03'): 0.142, ('C10', 'C04'): 0.134,
            ('C11', 'C12'): 0.083, ('C11', 'C14'): 0.150,
            ('C12', 'C13'): 0.060, ('C12', 'C43'): 0.146,
            ('C13', 'C16'): 0.141,
            ('C14', 'C22'): 0.100, ('C14', 'C44'): 0.090,
            ('C15', 'C48'): 0.276, ('C15', 'C13'): 0.060,
            ('C16', 'C43'): 0.037, ('C16', 'C46'): 0.132,
            ('C17', 'C32'): 0.160,
            ('C18', 'C01'): 0.134, ('C18', 'B'): 0.082,
            ('C19', 'C02'): 0.125, ('C19', 'C18'): 0.145, ('C19', 'C30'): 0.152,
            ('C20', 'C11'): 0.061,
            ('C21', 'C19'): 0.143, ('C21', 'C20'): 0.103,
            ('C22', 'C21'): 0.225, ('C22', 'C28'): 0.140,
            ('C23', 'C24'): 0.135, ('C23', 'C26'): 0.131, ('C23', 'C45'): 0.147,
            ('C24', 'C23'): 0.135, ('C24', 'C42'): 0.362,
            ('C25', 'C22'): 0.070, ('C25', 'C44'): 0.095,
            ('C26', 'C25'): 0.060,
            ('C27', 'C24'): 0.152, ('C27', 'C26'): 0.136,
            ('C28', 'C'): 0.246, ('C28', 'C27'): 0.129,
            ('C29', 'C21'): 0.134, ('C29', 'C28'): 0.214,
            ('C30', 'C19'): 0.152, ('C30', 'C29'): 0.146,
            ('C31', 'C18'): 0.158, ('C31', 'C30'): 0.153,
            ('C32', 'C31'): 0.131, ('C32', 'C33'): 0.143,
            ('C33', 'C34'): 0.072, ('C33', 'C39'): 0.135,
            ('C34', 'C35'): 0.080, ('C34', 'D'): 0.143,
            ('C35', 'C36'): 0.150, ('C35', 'C38'): 0.140,
            ('C37', 'C36'): 0.136, ('C37', 'C38'): 0.140,
            ('C38', 'D'): 0.078, ('C38', 'C35'): 0.140,
            ('C39', 'C31'): 0.147, ('C39', 'C33'): 0.135,
            ('C40', 'C29'): 0.440, ('C40', 'C37'): 0.310,
            ('C41', 'C40'): 0.217,
            ('C42', 'C24'): 0.362, ('C42', 'C41'): 0.360,
            ('C43', 'C12'): 0.146, ('C43', 'C14'): 0.080,
            ('C44', 'C25'): 0.095, ('C44', 'C45'): 0.064, ('C44', 'C46'): 0.044,
            ('C45', 'C23'): 0.147, ('C45', 'C46'): 0.072,
            ('C46', 'C16'): 0.132, ('C46', 'C44'): 0.044,
            ('C47', 'C10'): 0.041,
            ('C48', 'SG'): 0.013, ('C48', 'C05'): 0.046
        },
        locations={
            'SG': (68.2, 1.4), 'Be': (43, 5), 'B': (75, 22), 'C': (30.6, 54.5), 'D': (69.5, 49.7),
            'C01': (65, 12.7), 'C02': (58.7, 12.7), 'C03': (75.7, 13.1), 'C04': (61.2, 4),
            'C05': (58.8, 3.8), 'C06': (49.8, 14.3), 'C07': (47, 3.8), 'C08': (48.3, 8.4),
            'C09': (58.6, 7.6), 'C10': (71.7, 3.93), 'C11': (41.7, 16.2), 'C12': (39.9, 10.2),
            'C13': (38.5, 6.4), 'C14': (30.6, 18.7), 'C15': (39.5, 1.7), 'C16': (29.4, 10.3),
            'C17': (79, 22), 'C18': (69, 22), 'C19': (58.7, 22), 'C20': (45.8, 14.1),
            'C21': (47.8, 22.6), 'C22': (31.9, 26.3), 'C23': (13.3, 30.6), 'C24': (11, 40.4),
            'C25': (26.8, 27.2), 'C26': (22.5, 28.3), 'C27': (22.3, 37.7), 'C28': (31.5, 35.9),
            'C29': (47, 33.4), 'C30': (58, 33), 'C31': (69.6, 33.3), 'C32': (79.3, 33.7),
            'C33': (79.4, 44.4), 'C34': (79.3, 49.6), 'C35': (79.4, 55.6), 'C36': (79.4, 66.2),
            'C37': (69.1, 66.2), 'C38': (69.2, 55.3), 'C39': (69.3, 44.2), 'C40': (46.6, 66),
            'C41': (30, 66), 'C42': (3.4, 66), 'C43': (30.3, 13.2), 'C44': (24.4, 20.4),
            'C45': (18.8, 22.5), 'C46': (22.6, 17.5), 'C47': (70.1, 1.2), 'C48': (59.7, 1.4)
        },
        directed=True
    )


def create_traffic():

    traffic = TrafficCondition()

    # test SG - B
    #traffic.add_peak_hour('C02', 'C19', time(7, 0), time(9, 50), 10)
    #traffic.add_road_closure('C02', 'C19', time(7, 00), time(9, 55))

    #test SG - Be
    #traffic.add_peak_hour('C04', 'C05', time(7, 0), time(9, 50), 10)
    #traffic.add_road_closure('C04', 'C05', time(7, 00), time(9, 55))

    #test SG - D
    #traffic.add_peak_hour('C34', 'D', time(7, 0), time(9, 50), 10)
    #traffic.add_road_closure('C34', 'D', time(7, 00), time(9, 55))

    #test SG - C
    #traffic.add_peak_hour('C02', 'C06', time(7, 0), time(9, 50), 10)
    #traffic.add_road_closure('C02', 'C06', time(7, 00), time(9, 55))

    #test B - SG
    #traffic.add_peak_hour('C31', 'C18', time(7, 0), time(9, 50), 10)
    #traffic.add_road_closure('C31', 'C18', time(7, 00), time(9, 55))

    #test B - Be
    #traffic.add_peak_hour('C31', 'C18', time(7, 0), time(9, 50), 10)
    #traffic.add_road_closure('C31', 'C18', time(7, 00), time(9, 55))

    # test B - D
    #traffic.add_peak_hour('C34', 'D', time(7, 0), time(9, 50), 10)
    #traffic.add_road_closure('C34', 'D', time(7, 00), time(9, 55))

    # test B - C
    #traffic.add_peak_hour('C30', 'C29', time(7, 0), time(9, 50), 10)
    #traffic.add_road_closure('C30', 'C29', time(7, 00), time(9, 55))

    # test Be - SG
    #traffic.add_peak_hour('C14', 'C22', time(7, 0), time(9, 50), 10)
    #traffic.add_road_closure('C14', 'C22', time(7, 00), time(9, 55))

    # test Be - B
    #traffic.add_peak_hour('C19', 'C18', time(7, 0), time(9, 50), 10)
    #traffic.add_road_closure('C19', 'C18', time(7, 00), time(9, 55))

    return traffic


if __name__ == "__main__":

    romania = create_map()
    traffic = create_traffic()
    romania.traffic = traffic


    problem = RouteProblem(
        initial='Be',
        goal='D',
        map=romania,
        traffic_conditions=traffic,
        start_time=time(8,0)
    )

    # người dùng được lựa chọn ưu tiên cái nào nhất (distance, time, delay)
    planner = SmartPlanner(problem,"time")

    result, results = planner.plan()


    if result:
        path = path_states(result)
        visualize_map(romania, path)
    else:
        print("Không tìm thấy đường đi.")

    logger = ExcelLogger("routes_log.xlsx")
    if result != failure:

        best_name = next(name for name, r, b in results if r == result)
        logger.log_best_route(problem, results, best_name, result, planner.preference)