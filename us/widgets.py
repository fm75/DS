import panel as pn
import panel.widgets as pnw
import datetime
import pandas as pd

import us.states  as uss


pn.extension()
pn.config.sizing_mode = "stretch_width"

stats_w    = pnw.DataFrame(pd.DataFrame(), name='stats')
counties_w = pnw.DataFrame(pd.DataFrame(), name='counties')

sort_cols = ['Confirmed', 'Deaths', 'Active', 'county', 'pop2019', 
             'fraction_confirmed', 'death_rate']
state_w = pnw.Select(
    name='state',
    options=uss.states(),
    value='Alabama',
    disabled=False
    )

sortby_w = pnw.Select(
    name='sort on column',
    options=sort_cols,
    value='fraction_confirmed',
    disabled=False
    )

ascending_w = pnw.Checkbox(
    name='Sort Ascending',
    value=False,
    disabled=False
    )

date_w = pnw.DatePicker(
    name='date',
    value=datetime.date.today() - datetime.timedelta(1),
    disabled=False
    )