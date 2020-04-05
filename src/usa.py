from typing import List
from pathlib import Path
import pandas as pd


def us_states() -> List[str]:
    '''USA states only'''
    return us_data('../data/us-states-only.csv')


def us_all() -> List[str]:
    '''USA states, DC, and Territories'''
    return us_data('../data/us-all.csv')


def us_data(name: str) -> List[str]:
    with Path(name) as f:
        states = pd.read_csv(f)
    return list(states.state)