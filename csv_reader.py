import numpy as np
import pandas as pd


def get_csv_from_url(url: str) -> pd.Series:
    s: pd.DataFrame = pd.read_csv(url)
    for r in s.iterrows():
        yield r[1]


def main():
    for el in get_csv_from_url("c2.csv"):
        print(el.replace(np.nan, 0).to_dict())


if __name__ == '__main__':
    main()
