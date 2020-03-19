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
        
        self.df_corona = pd.read_csv('data/agg_data_2020-03-19.csv',
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

        usa = self.df_corona[self.df_corona.country=='US']
        usa = usa.confirmed.resample('D').sum().rolling("3D").sum()
        tmp = usa.to_frame().reset_index()

        self.type_stats_ds.data = tmp
        print(tmp)


