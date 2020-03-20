"""Corona report dashboard."""

import numpy as np
import datetime as dt

from bokeh.plotting import figure, curdoc
from bokeh.models import HoverTool, CustomJSHover,TickFormatter
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models.widgets import DataTable, TableColumn, HTMLTemplateFormatter, DateFormatter, Slider,DateSlider, DateRangeSlider, RangeSlider
from bokeh.models.callbacks import CustomJS
from bokeh.models.tickers import FixedTicker
from bokeh.models import NumeralTickFormatter

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

p=stats_plot = figure(x_axis_type='datetime',plot_height=400, plot_width=400,
                    tools=["save"],
                    name="stats_plot",
                    title="USA vs Italy (shifted 13 days)")
stats_plot.line(x="datetime", y="confirmed_1", width=0.9, source=data_provider.type_stats_ds, legend_label="USA")
stats_plot.line(x="datetime", y="confirmed_2", width=0.9, source=data_provider.type_stats_ds,color="red", legend_label="Italy")
stats_plot.legend.location = "top_left"
p.yaxis.formatter=NumeralTickFormatter(format="00")

#stats_plot.vbar(x="dates", top="country2", width=0.9, source=data_provider.type_stats_ds)
#stats_plot.xaxis[0].ticker=FixedTicker(
 #       ticks=[data_provider.Severitymap[sevirty] for sevirty in data_provider.type_stats_ds['Accident_Severity']])





def update_data():
    data_provider.getdata()



curdoc().add_root(stats_plot)
curdoc().add_periodic_callback(update_data, cfg.UPDATE_INTERVAL)