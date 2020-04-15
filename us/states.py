import pandas as pd
from typing import List


def states() -> List[str]:
    return list(pd.read_csv('data/us-states-only.csv').state)


def states_and_territories() -> List[str]:
    return list(pd.read_csv('data/us-all.csv').state)
