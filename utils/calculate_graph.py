from collections import deque
import pandas as pd

def donchian_channel(df: pd.DataFrame, window_size: int) -> pd.DataFrame:
    last_n_values = deque(maxlen=window_size)
    max_vals = []
    min_vals = []
    avg_vals = []
    dates = []

    df = df[df["type"]== "PRICE"]
    if df.iloc[-1]["t"] < df.iloc[0]["t"]:
        # checks if the dates are the right way around (earlier dates should be at top of df)
        df = df[::-1]

    for row in df.index:
        last_n_values.append(df.at[row,"c"])
        dates.append(df.at[row,"t"])
        max_val = max(last_n_values)
        min_val = min(last_n_values)
        avg_val = (max_val + min_val) / 2

        max_vals.append(max_val)
        min_vals.append(min_val)
        avg_vals.append(avg_val)

    donchian_max = pd.DataFrame({"t": dates, "c": max_vals, "type": "Donchian Upper" })
    donchian_min = pd.DataFrame({"t": dates, "c": min_vals, "type": "Donchian Lower" })
    donchian_avg = pd.DataFrame({"t": dates, "c": avg_vals, "type": "Donchian Avg"})
    return pd.concat([donchian_max, donchian_min, donchian_avg])

def simple_moving_average(df: pd.DataFrame, window_size: int) -> pd.DataFrame:
    last_n_values = deque(maxlen=window_size)
    sma_vals = []
    dates = []

    df = df[df["type"] == "PRICE"]
    if df.iloc[-1]["t"] < df.iloc[0]["t"]:
        # checks if the dates are the right way around (earlier dates should be at top of df)
        df = df[::-1]

    for row in df.index:
        last_n_values.append(df.at[row, "c"])

        if len(last_n_values) < window_size:
            continue

        dates.append(df.at[row,"t"])
        sma_vals.append(sum(last_n_values) / window_size)

    return pd.DataFrame({"t": dates, "c": sma_vals, "type": "Simple Moving Average"})


# both functions need to take into account non market days
