"""Corona report dashboard."""

import numpy as np
import datetime as dt

from bokeh.plotting import figure, curdoc
from bokeh.models import HoverTool, CustomJSHover,TickFormatter
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models.widgets import DataTable, TableColumn, HTMLTemplateFormatter, DateFormatter, Slider,DateSlider, DateRangeSlider, RangeSlider
from bokeh.models.callbacks import CustomJS
from bokeh.models.tickers import FixedTicker

from data import DataProvider
import config as cfg

TOOLTIP = """
<div class="plot-tooltip">
tooltip
</div>
"""

COL_TPL = """
<%= get_icon(type.toLowerCase()) %> <%= type %>
"""

data_provider = DataProvider()

stats_plot = figure(x_axis_type='datetime',plot_height=400, plot_width=400,
                    tools=["save"],
                    name="stats_plot",
                    title="USA vs Italy (shifted 13 days)")
stats_plot.line(x="datetime", y="confirmed_1", width=0.9, source=data_provider.type_stats_ds)
stats_plot.line(x="datetime", y="confirmed_2", width=0.9, source=data_provider.type_stats_ds,color="red")
#stats_plot.vbar(x="dates", top="country2", width=0.9, source=data_provider.type_stats_ds)
#stats_plot.xaxis[0].ticker=FixedTicker(
 #       ticks=[data_provider.Severitymap[sevirty] for sevirty in data_provider.type_stats_ds['Accident_Severity']])




def update_stats():
    stats_plot.x_range.factors = data_provider.dispatch_types


def update():
    data_provider.fetch_data()
    update_stats()



curdoc().add_root(stats_plot)
