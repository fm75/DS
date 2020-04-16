import panel as pn
from us.widgets import state_w, date_w, sortby_w, ascending_w
from us.model import update_stats, update_counties

pn.extension()

@pn.depends(state_w, date_w)
def show_stats(state_w, date_w, view_fn=update_stats):
    return update_stats(state_w, date_w)


@pn.depends(state_w, date_w, sortby_w, ascending_w)
def show_counties(state_w, date_w, sortby_w, ascending_w, view_fn=update_counties):
    return update_counties(state_w, date_w, sortby_w, ascending_w)


# column1 = pn.Column(state_w, date_w)
# column2 = pn.Column(state_w, date_w, sortby_w, ascending_w)
# pane1 = pn.Row(show_stats, column1)
# pane2 = pn.Row(show_counties, column2)
# pane1 = pn.Column(show_stats, column1)
# pane2 = pn.Column(show_counties, column2)
row1 = pn.Row(state_w, date_w)
row2 = pn.Row(state_w, date_w, sortby_w, ascending_w)
pane1 = pn.Column(row1, show_stats)
pane2 = pn.Column(row2, show_counties)
tabs = pn.Tabs()
tabs.extend (
    [
    ('County Statistical Summary', pane1),
    ('County Details', pane2),
    ]
)