"""Data provider for Corona Report application."""

import os
import sys
import numpy as np
import pandas as pd
import calendar
import time
from string import capwords
from difflib import get_close_matches
from bokeh.models import ColumnDataSource

import github
from config import REPO, TMP_FOLDER, TMP_GIT, DATA


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

        print("in init")

        self.getdata()

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
        usa = usa.confirmed_1.resample('D').sum().rolling("3D").mean()

        italy = self.df_corona.copy().rename({'confirmed':'confirmed_2'}, axis=1)
        italy.index = italy.index + pd.Timedelta(days=13)
        italy = italy.confirmed_2[italy.country=='Italy']
        italy = italy.resample('D').sum().rolling("3D").mean()

        tmp = pd.concat([usa, italy],axis=1)
        tmp = tmp.reset_index()

        self.type_stats_ds.data = tmp


    def getdata(self):

            save_dir = os.path.join(os.getcwd(), "corona_report/data")
            print('save_dir:', save_dir)
            if not os.path.exists(save_dir):
                os.system('mkdir -p '+save_dir)

            csv_file_name = 'agg_data.csv'
            print('...', csv_file_name)

            if os.path.exists(os.path.join(save_dir, csv_file_name)):
                current_time_epoch = calendar.timegm(time.gmtime())
                last_update = os.path.getmtime(os.path.join(save_dir, csv_file_name))
                print("t:",current_time_epoch,last_update)
                diff = current_time_epoch-last_update
                print("diff:",diff)
                if (diff<20000):
                    return


            df = github.get()
            print("back from github",df.info())
            # sheets need to be sorted by date value
            print('Sorting by datetime...')
            df = df.sort_values('datetime')
            df.astype(str).to_csv(os.path.join(save_dir, csv_file_name))

