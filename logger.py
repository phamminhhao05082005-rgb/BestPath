import datetime
from datetime import timedelta
from trees import failure

class Logger:
    def __init__(self, filename="log.txt"):
        self.filename = filename

    def log(self, message):

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")

    def log_result(self, problem, results, best_name, best_result, preference):

        with open(self.filename, "a", encoding="utf-8") as f:
            f.write("\n============================\n")
            f.write(f"Tìm đường từ {problem.initial} → {problem.goal}\n")
            f.write(f"Ưu tiên: {preference}\n")
            f.write("----------------------------\n")


            for name, result, _ in results:
                if result != failure:
                    f.write(
                        f"{name}: time={result.path_cost:.2f} giay, "
                        f"distance={result.total_km:.3f} km, "
                        f"delay={result.total_delay:.2f} phút\n"
                    )
                else:
                    f.write(f"{name}: thất bại\n")

            f.write("----------------------------\n")

            f.write(
                f"Best ({preference}): {best_name} | "
                f"time={best_result.path_cost:.2f} giay, "
                f"distance={best_result.total_km:.3f} km, "
                f"delay={best_result.total_delay:.2f} phut\n"
            )
            f.write("============================\n\n")