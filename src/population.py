import pandas as pd
import requests
from pathlib import Path


# county level functions
# us_county_population_path = Path('../data/co-est2019-alldata.csv')
# nj_county_population_url = 'https://www.newjersey-demographics.com/counties_by_population'
def us_county_population(csvfile: Path) -> pd.DataFrame:
    population = pd.read_csv(csvfile, encoding = "ISO-8859-1")
    population = population[["STNAME", 'CTYNAME', 'POPESTIMATE2019']]
    return population.rename(columns={"STNAME": "state", "CTYNAME": "county", "POPESTIMATE2019": "pop2019"})
    return population


def nj_county_population(url: str) -> pd.DataFrame:
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }

    r = requests.get(url, headers=header)
    population = pd.read_html(r.text, header=[0], index_col=0, skiprows=[22])[0]
    population = population[['County', 'Population']]
    return population.rename(columns={"County": "county", "Population": "pop2019"})


# state level functions
# state_geog_path = Path('../data/us_geography.csv')
# state_population_path = Path('../data/SCPRC-EST2019-18+POP-RES.csv')
def state_geography(csvfile: Path) -> pd.DataFrame:
    geog = pd.read_csv(csvfile, thousands=',')
    geog = geog[['State', 'tot_sq_mi', 'land_sq_mi']]
    return geog.rename(columns={"State": "state", })


def state_population(csvfile: Path) -> pd.DataFrame:
    population = pd.read_csv(csvfile)
    population = population[["NAME", 'POPESTIMATE2019']]
    return population.rename(columns={"NAME": "state", "POPESTIMATE2019": "pop2019"})


def state_population_density(state_population_path: Path, state_geog_path: Path) -> pd.DataFrame:
    state_pop  = state_population(state_population_path)
    state_geog = state_geography(state_geog_path)

    state_density = pd.merge(state_pop, state_geog)
    state_density['density_land']  = state_density['pop2019'] / state_density['land_sq_mi']
    state_density['density_total'] = state_density['pop2019'] / state_density['tot_sq_mi']
    return state_density
