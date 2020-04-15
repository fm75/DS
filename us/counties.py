# import pandas as pd
# import datetime as dt
from typing import List

# df = None
# current_state = None

def county_file_name(state: str) ->str:
    return '/'.join(['data', 'counties', state.lower().replace(' ', '-')]) + '.csv'


# def update_county_stats(state:str, date: dt.date) -> pd.DataFrame:
#     global df
#     global current_state
#     if state != current_state:
#         df = pd.read_csv(county_file_name(state))
#         current_state = state
#     return df.describe()[['pop2019']].style.format({"pop2019": "{:,.0f}",})


# def update_counties(state: str, date: dt.date, column: str, ascending: bool) -> pd.DataFrame:
#     global df
#     df = pd.read_csv(county_file_name(state))
#     df.style.format({"pop2019": "{:,.0f}",})
#     return df.sort_values(by=column, ascending=ascending)[['county', 'pop2019']]