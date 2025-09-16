import pandas as pd
from datetime import datetime, timedelta
from openpyxl import load_workbook
from roads import road_names
from trees import path_states, path_with_roads, failure

class ExcelLogger:
    def __init__(self, filename="routes_log.xlsx"):
        self.filename = filename

    def _format_time(self, seconds):

        if seconds is None or seconds == float('inf'):
            return "N/A"
        total_seconds = int(seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        sec = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{sec:02d}"

    def log_best_route(self, problem, results, best_name, best_result, preference):
        if best_result == failure:
            print("Không có kết quả để ghi.")
            return


        path_nodes = path_states(best_result)
        path_info = path_with_roads(best_result, road_names)


        congested_segments = []
        traffic_condition = "Normal"
        for a, b, road in path_info:
            if problem.traffic_conditions and best_result.arrival_time:
                arrival_time = best_result.arrival_time.time()
                delay = problem.traffic_conditions.get_traffic_delay(a, b, arrival_time)
                if delay > 0:
                    traffic_condition = "Congested"
                    start = arrival_time.strftime("%H:%M")
                    end = (datetime.combine(datetime.today(), arrival_time) +
                           timedelta(minutes=delay)).strftime("%H:%M")
                    congested_segments.append(f"{a}-{b} ({start};{end})")


        blocked_segments = next(b for n, r, b in results if n == best_name)
        if blocked_segments:
            traffic_condition = "Closed"

        fixed_columns = [
            'STT', 'Start', 'Goal', 'Departure time', 'Algorithm',
            'Path', 'Cost(km)', 'Total Time', 'Traffic Condition',
            'Congested Segments', 'Blocked Segments', 'Recorded Time'
        ]
        algo_columns = [name for name, _, _ in results]


        data = {
            'STT': [1],
            'Start': [problem.initial],
            'Goal': [problem.goal],
            'Departure time': [problem.start_time.strftime("%H:%M") if problem.start_time else "N/A"],
            'Algorithm': [best_name],
            'Path': ['→'.join(path_nodes)],
            'Cost(km)': [best_result.total_km],
            'Total Time': [self._format_time(best_result.path_cost)],
            'Traffic Condition': [traffic_condition],
            'Congested Segments': [','.join(congested_segments) if congested_segments else "None"],
            'Blocked Segments': [','.join(blocked_segments) if blocked_segments else "None"],
            'Recorded Time': [datetime.now().strftime("%Y-%m-%d %H:%M")]
        }


        for name, result, _ in results:
            if result != failure:
                data[name] = [self._format_time(result.path_cost)]
            else:
                data[name] = ["Fail"]

        new_df = pd.DataFrame(data, columns=fixed_columns + algo_columns)


        try:
            existing_df = pd.read_excel(self.filename, sheet_name='Routes', engine='openpyxl')
            start_stt = int(existing_df['STT'].max()) + 1  # Ép kiểu int
            new_df['STT'] = pd.Series(range(start_stt, start_stt + len(new_df)))
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        except (FileNotFoundError, ValueError, KeyError):
            new_df['STT'] = 1
            combined_df = new_df


        with pd.ExcelWriter(self.filename, engine='openpyxl') as writer:
            combined_df.to_excel(writer, sheet_name='Routes', index=False)


        wb = load_workbook(self.filename)
        ws = wb['Routes']
        for row in ws.rows:
            for cell in row:
                cell.alignment = cell.alignment.copy(horizontal='center')

        for col in ws.columns:
            max_length = max(len(str(cell.value)) for cell in col)
            ws.column_dimensions[col[0].column_letter].width = max_length + 2

        wb.save(self.filename)
        print(f"Đã ghi và định dạng tuyến đường tốt nhất vào {self.filename}")

    def get_route_info(self, start=None, goal=None, preference=None):
        try:
            df = pd.read_excel(self.filename, sheet_name='Routes', engine='openpyxl')
        except FileNotFoundError:
            print("File Excel không tồn tại.")
            return []

        filtered = df.copy()
        if start:
            filtered = filtered[filtered['Start'] == start]
        if goal:
            filtered = filtered[filtered['Goal'] == goal]
        if preference:
            filtered = filtered[filtered['Algorithm'].str.contains(preference, na=False)]

        if filtered.empty:
            print("Không tìm thấy thông tin phù hợp.")
            return []

        route_list = []
        for _, row in filtered.iterrows():
            route_list.append({
                'stt': row['STT'],
                'start': row['Start'],
                'goal': row['Goal'],
                'departure_time': row['Departure time'],
                'algorithm': row['Algorithm'],
                'path': row['Path'].split('→') if pd.notna(row['Path']) else [],
                'cost_km': row['Cost(km)'],
                'traffic_condition': row['Traffic Condition'],
                'congested_segments': row['Congested Segments'].split(',') if pd.notna(row['Congested Segments']) and row['Congested Segments'] != "None" else [],
                'blocked_segments': row['Blocked Segments'].split(',') if pd.notna(row['Blocked Segments']) and row['Blocked Segments'] != "None" else [],
                'recorded_time': row['Recorded Time']
            })

        print(f"Tìm thấy {len(route_list)} tuyến đường phù hợp.")
        return route_list