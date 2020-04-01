import pandas as pd
import requests


def daily_url(mmddyy: str) -> str:
    '''date in mm-dd-yyyy format'''
    return f'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports/{date}.csv'


def daily_snapshot(date: str) -> pd.DataFrame:
    '''date in mm-dd-yyyy format'''
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }

    r = requests.get(url, headers=header)
    df = pd.read_html(r.text, header=[0], index_col=1)[0]
    return df