"""Corona report dashboard."""

import numpy as np
import datetime as dt

from bokeh.plotting import figure, curdoc
from bokeh.models import HoverTool, CustomJSHover,TickFormatter
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models.widgets import DataTable, TableColumn, HTMLTemplateFormatter, DateFormatter, Slider,DateSlider, DateRangeSlider, RangeSlider,CheckboxGroup,Button,Select
from bokeh.models.callbacks import CustomJS
from bokeh.models.tickers import FixedTicker
from bokeh.models import NumeralTickFormatter
from bokeh.layouts import row, widgetbox, Column


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

cur_ratio = 0 #global


data_provider = DataProvider()

countries = data_provider.get_countries()

p=stats_plot = figure(x_axis_type='datetime',plot_height=400, plot_width=400,
                    tools=["save","crosshair"],  #todo: add hover
                    name="stats_plot",
                    title="USA vs Italy (shifted)")
stats_plot.line(x="datetime", y="confirmed_1", width=0.9, source=data_provider.type_stats_ds, legend_label="USA")
stats_plot.line(x="datetime", y="confirmed_2", width=0.9, source=data_provider.type_stats_ds,color="red", legend_label="Italy")
stats_plot.legend.location = "top_left"
p.yaxis.formatter=NumeralTickFormatter(format="00")

shifter_slider =  Slider(start=-1, end=20,
                value=10, 
                step=1,name="shifter_slider", title="Shift by")


sizedCorrection_chkbox = CheckboxGroup(
    labels=[ "Apply size correction"], 
    active=[],
    name="sizedCorrection_chkbox")

country_select1 = Select(title="Country:", name="country_select1",value="US", options=countries)
country_select2 = Select(title="Country:", name="country_select2",value="Italy", options=countries)



def update_shifter(attr, old, new):
    if new != old:
        data_provider.set_shifter(new)
        data_provider.update_stats()

def sizeCorrection_click(attr, old, new):
    #print("in sizedCorrection_click:")
    if new == old:
        return
    val = len(new)
    data_provider.set_sizedCorrection(val)
    data_provider.update_stats()

def country_select1_change(attr, old, new):
    global cur_ratio
    print("in country_select1_change:", old, new)
    if new == old:
        return
    data_provider.set_country(0,new)
    data_provider.update_stats()
    cur_ratio = data_provider.get_ratio()
    print("ratio:", cur_ratio)
    curdoc().template_variables["cur_ratio"] = round(cur_ratio,1)

def country_select2_change(attr, old, new):
    global cur_ratio
    print("in country_select1_change:", old, new)
    if new == old:
        return
    data_provider.set_country(1,new)
    data_provider.update_stats()
    cur_ratio = data_provider.get_ratio()
    print("ratio:", cur_ratio)
    curdoc().template_variables["cur_ratio"] = round(cur_ratio,1)


def update_data():
    data_provider.getdata()

cur_ratio = data_provider.get_ratio()
country1,country2 = data_provider.get_country_sizes()


shifter_slider.on_change("value_throttled", update_shifter)
sizedCorrection_chkbox.on_change('active',sizeCorrection_click)
country_select1.on_change('value',country_select1_change)
country_select2.on_change('value',country_select2_change)


curdoc().add_root(sizedCorrection_chkbox)
curdoc().add_root(stats_plot)
curdoc().add_root(shifter_slider)
curdoc().add_root(country_select1)
curdoc().add_root(country_select2)

curdoc().template_variables["cur_ratio"] = round(cur_ratio,1)
curdoc().template_variables["country1"] = round(country1/1e6,1)
curdoc().template_variables["country2"] = round(country2/1e6,1)

curdoc().add_periodic_callback(update_data, cfg.UPDATE_INTERVAL)