import pandas as pd
import requests
from pathlib import Path



def strip_county_name(name: str) -> str:
    '''Remove " County" from county names.'''
    return name[:-7] if name[-6:].lower() == 'county' else name
def domainify(state: str) -> str:
    return f"https://www.{state.replace(' ', '').lower()}-demographics.com/counties_by_population"


# county level functions
# us_county_population_path = Path('../data/co-est2019-alldata.csv')
# nj_county_population_url = 'https://www.newjersey-demographics.com/counties_by_population'
def us_county_population(csvfile: Path) -> pd.DataFrame:
    colmap = {"STNAME": "state", "CTYNAME": "county", "POPESTIMATE2019": "pop2019"}
    population = pd.read_csv(csvfile, encoding = "ISO-8859-1",
                             usecols=colmap,
                             converters={'CTYNAME':strip_county_name})
    return population


def us_county_population(url: str) -> pd.DataFrame:
    '''Get latest county population.
    Omit the last line retrieved which is just an explanation.'''
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }
    names = ['County', 'Population']
    r = requests.get(url, headers=header)
    population = pd.read_html(r.text, header=[0], index_col=0, 
                              converters={'County':strip_county_name})[0]
    population = population[names]
    return population.rename(columns={"County": "county", "Population": "pop2019"})[:-1]


def nj_county_population(url: str) -> pd.DataFrame:
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }
    names = ['County', 'Population']
    r = requests.get(url, headers=header)
    population = pd.read_html(r.text, header=[0], index_col=0, 
                              skiprows=[22], converters={'County':strip_county_name})[0]
    population = population[names]
    return population.rename(columns={"County": "county", "Population": "pop2019"})


# state level functions
# state_geog_path = Path('../data/us_geography.csv')
# state_population_path = Path('../data/SCPRC-EST2019-18+POP-RES.csv')
def state_geography(csvfile: Path) -> pd.DataFrame:
    colmap = {"State": "state", 'tot_sq_mi':'tot_sq_mi', 'land_sq_mi':'land_sq_mi'}
    return pd.read_csv(csvfile, thousands=',', usecols=colmap)


def state_population(csvfile: Path) -> pd.DataFrame:
    colmap = {"NAME": "state", "POPESTIMATE2019": "pop2019"}
    return pd.read_csv(csvfile, usecols=colmap)


def state_population_density(state_population_path: Path, state_geog_path: Path) -> pd.DataFrame:
    state_pop  = state_population(state_population_path)
    state_geog = state_geography(state_geog_path)

    state_density = pd.merge(state_pop, state_geog)
    state_density['density_land']  = state_density['pop2019'] / state_density['land_sq_mi']
    state_density['density_total'] = state_density['pop2019'] / state_density['tot_sq_mi']
    return state_density
