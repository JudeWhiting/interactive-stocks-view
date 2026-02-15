from collections import deque
import pandas as pd

def donchian_channel(raw_data: list, window_size: int):
    last_n_values = deque(maxlen=window_size)
    max_vals = []
    min_vals = []
    avg_vals = []

    for row in raw_data:
        last_n_values.append(row["close"])

        if len(last_n_values) < window_size:
            continue

        max_val = max(last_n_values)
        min_val = min(last_n_values)
        avg_val = (max_val + min_val) / 2

        max_vals.append(max_val)
        min_vals.append(min_val)
        avg_vals.append(avg_val)

    return {"max" : [None] * (window_size-1) + max_vals, "min" : [None] * (window_size-1) + min_vals, "avg" : [None] * (window_size-1) + avg_vals}

def simple_moving_average(raw_data, window_size: int):
    last_n_values = deque(maxlen=window_size)
    sma_vals = []

    for row in raw_data:
        last_n_values.append(row["close"])

        if len(last_n_values) < window_size:
            continue

        sma_vals.append(sum(last_n_values) / window_size)

    return [None] * (window_size-1) + sma_vals


# both functions need to take into account non market days
