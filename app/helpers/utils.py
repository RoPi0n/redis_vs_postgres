from time import perf_counter_ns

def time_ms() -> int:
    return perf_counter_ns() // 1000000

def time_us() -> int:
    return perf_counter_ns() // 1000

def time_ns() -> int:
    return perf_counter_ns()