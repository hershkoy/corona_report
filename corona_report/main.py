"""Corona report dashboard."""

import numpy as np
import datetime as dt

from bokeh.plotting import figure, curdoc
from bokeh.models import HoverTool, CustomJSHover,TickFormatter
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models.widgets import DataTable, TableColumn, HTMLTemplateFormatter, DateFormatter, Slider,DateSlider, DateRangeSlider, RangeSlider,CheckboxGroup
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
                    title="USA vs Italy (shifted)")
stats_plot.line(x="datetime", y="confirmed_1", width=0.9, source=data_provider.type_stats_ds, legend_label="USA")
stats_plot.line(x="datetime", y="confirmed_2", width=0.9, source=data_provider.type_stats_ds,color="red", legend_label="Italy")
stats_plot.legend.location = "top_left"
p.yaxis.formatter=NumeralTickFormatter(format="00")

shifter_slider =  Slider(start=-1, end=20,
                value=10, 
                step=1,name="shifter_slider", title="Shift by")



sizedCorrection_chkbox = CheckboxGroup(labels=[ "Apply size correction"], active=[])



def update_shifter(attr, old, new):
    if new != old:
        data_provider.set_shifter(new)
        data_provider.update_stats()

def sizedCorrection_click(attr, old, new):
    print("in sizedCorrection_click:",old,new)
    if new == old:
        return
    val = len(new)
    data_provider.set_sizedCorrection(val)
    data_provider.update_stats()

    

def update_data():
    data_provider.getdata()

cur_ratio = data_provider.get_ratio()
print("cur_ratio:",cur_ratio)

shifter_slider.on_change("value_throttled", update_shifter)
sizedCorrection_chkbox.on_change('active',sizedCorrection_click)


curdoc().add_root(stats_plot)
curdoc().add_root(shifter_slider)
#curdoc().add_root(sizedCorrection_chkbox)
curdoc().add_periodic_callback(update_data, cfg.UPDATE_INTERVAL)