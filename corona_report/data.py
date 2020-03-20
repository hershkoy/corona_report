"""Data provider for Corona Report application."""

import numpy as np
import pandas as pd
import geopandas as gpd
import datetime as dt
import pytz
from bokeh.models import ColumnDataSource, CDSView, BooleanFilter

import config as cfg


class DataProvider(object):
    RAW_COLS = [ 'confirmed', 'country', 'deaths', 'province', 'recovered',
       'date', 'file_date','datetime']
    COLS = [ 'confirmed', 'country', 'deaths', 'province', 'recovered',
       'date', 'file_date','datetime']
    
    #add a colormap to signal te severity of the accident
    colormap={"1":"darkred",
               "2":"saddlebrown",
               "3":"orange"}
    

    def __init__(self):
        
        self.df_corona = pd.read_csv('corona_report/data/agg_data.csv',
            usecols=DataProvider.RAW_COLS,
            parse_dates=["datetime"],
            index_col="datetime"
        )

        self.df_corona = self.df_corona.sort_index()

        # Preparing containers
        self.type_stats_ds = ColumnDataSource(data={"dates": [], "country1": [], "country2": []})


        self.update_stats()
        
        
    def update_stats(self):
        print("in update_stats")

        usa = self.df_corona.copy().rename({'confirmed':'confirmed_1'}, axis=1)
        usa = usa[usa.country=='US']
        usa = usa.confirmed_1.resample('D').sum().rolling("3D").sum()

        italy = self.df_corona.copy().rename({'confirmed':'confirmed_2'}, axis=1)
        italy.index = italy.index + pd.Timedelta(days=13)
        italy = italy.confirmed_2[italy.country=='Italy']
        italy = italy.resample('D').sum().rolling("3D").sum()

        tmp = pd.concat([usa, italy],axis=1)
        tmp = tmp.reset_index()

        self.type_stats_ds.data = tmp


