import pandas as pd
df = pd.DataFrame({"a": [1,2,3], "b": [4,5,6], "c": [7,8,9]})
def get_daterange(df: pd.DataFrame):

    print(df)
    return df.at[1,"b"]#, df.iat[len(df)-1, 0]

print(get_daterange(df))