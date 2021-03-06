import pandas as pd
from datetime import datetime as dt
from typing import List
from us.covid import daily_snapshot

pd.set_option('max_rows', 300)

# DataFrames
state_with_population = None
county_pop = None
daily = None

current_date = None
current_state = None

def county_file_name(state: str) ->str:
    return '/'.join(['data', 'counties', state.lower().replace(' ', '')]) + '.csv'


def states() -> List[str]:
    return list(pd.read_csv('data/us-states-only.csv').state)


def covid_columns () -> List[str]:
    return ['Admin2', 'Confirmed', 'Deaths', 'Active', ]


# def update_dataframes(state:str, date: dt.date) -> None:
#     global daily
#     global county_pop
#     global current_date
#     global current_state
#     changed = False
#     if date != current_date:
#         daily = daily_snapshot(dt.strftime(date, '%m-%d-%Y'))
#         current_date = date
#         changed = True
#     if state != current_state:
#         current_state = state
#         county_pop = pd.read_csv(county_file_name(state))
#         changed = True
#     if changed:
#         update_merge(state, date)

        
def update_dataframes(state:str, date: dt.date) -> None:
    global daily
    global county_pop

    daily = daily_snapshot(dt.strftime(date, '%m-%d-%Y'))
    county_pop = pd.read_csv(county_file_name(state))
    update_merge(state, date)


def update_merge(state:str, date: dt.date) -> pd.DataFrame:
    global state_with_population
    global daily
    global county_pop
    state_covid = daily[daily.Province_State == state].copy()
    state_with_population = pd.merge(state_covid[covid_columns()], 
                                     county_pop,
                                     how='outer',
                                     left_on='Admin2',
                                     right_on='county')
    state_with_population['fraction_confirmed'] = state_with_population['Confirmed'] / state_with_population['pop2019']   * 1000.0
    state_with_population['deaths']             = state_with_population['Deaths']    / state_with_population['pop2019']   * 1000.0
    state_with_population['death_rate']         = state_with_population['Deaths']    / state_with_population['Confirmed'] * 1000.0                              

def update_stats(state:str, date: dt.date) -> pd.DataFrame:
    global state_with_population
    update_dataframes(state, date)
    fmt = dict(
              Confirmed='{:,.1f}',
              Deaths='{:,.1f}',
              Active='{:,.1f}',
              Rank='{:,.1f}',
              pop2019='{:,.1f}',
              fraction_confirmed='{:,.1f}',
              deaths='{:,.1f}',
              death_rate='{:,.1f}',
    )
    return state_with_population.describe().style.format(fmt)


def update_counties(state: str, date: dt.date, column: str, ascending: bool) -> pd.DataFrame:
    global state_with_population
    update_dataframes(state, date)
    fmt = dict(
              Confirmed='{:,.0f}',
              Deaths='{:,.0f}',
              Active='{:,.0f}',
              Rank='{:,.0f}',
              pop2019='{:,.0f}',
              fraction_confirmed='{:,.1f}',
              deaths='{:,.1f}',
              death_rate='{:,.1f}',
    )
    return state_with_population.sort_values(by=column, ascending=ascending).style.format(fmt).hide_index()
