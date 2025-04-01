import time
from functools import wraps
from collections import defaultdict


class Profiler():
  _instance = None  # Singleton instance

  def __new__(cls):
    """Ensure a single instance is shared across all classes."""
    if cls._instance is None:
      cls._instance = super(Profiler, cls).__new__(cls)
      cls._instance.reset_profiler()
    return cls._instance

  @staticmethod
  def profile_function(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
      profiler = Profiler()  # Get the shared instance
      start_time = time.time()
      result = func(*args, **kwargs)
      elapsed_time = time.time() - start_time

      if profiler.start_time is None:
        profiler.start_time = start_time

      profiler.profile_data[func.__name__]["total_time"] += elapsed_time
      profiler.profile_data[func.__name__]["call_count"] += 1

      return result

    return wrapper

  def print_profile_summary(moves_evaluated):
    profiler = Profiler()  # Get the singleton instance directly here

    print(f"\n{'-' * 10} Chess Engine Profiling Summary {'-' * 10}")
    print(f"Total time to calculate move: {(time.time() - profiler.start_time):.2f}s.")
    print(f"Moves evaluated per second: {int(moves_evaluated // (time.time() - profiler.start_time))}")
    print("-" * 56)

    print("{:<25} {:<15} {:<15}".format("Function Name", "Call Count", "Total Time (s)"))
    print("-" * 56)

    for func_name, data in sorted(profiler.profile_data.items(), key=lambda x: x[1]["total_time"], reverse=True):
      print("{:<25} {:<15} {:<15.3f}".format(func_name, data["call_count"], data["total_time"]))

  def reset_profiler(self):
    self.start_time = None

    def default_profiling_data():
      return {"total_time": 0, "call_count": 0}

    self.profile_data = defaultdict(default_profiling_data)
