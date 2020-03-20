#!/usr/bin/env python3
from __future__ import print_function
import pandas as pd
import re
import os
import sys
import git
from tqdm import tqdm
from time import strftime
from dateutil.parser import parse
from datetime import datetime, date, time 
from config import REPO, TMP_FOLDER, TMP_GIT, DATA, KEEP_COLS, NUMERIC_COLS

def clean_sheet_names(new_ranges):
    indices = []    
    # Remove all sheets that dont have a numeric header
    numeric_sheets = [x for x in new_ranges if re.search(r'\d', x)]
    
    return numeric_sheets

def clone_repo(TMP_FOLDER, REPO):
    print('Cloning Data Repo...')
    git.Git(TMP_FOLDER).clone(REPO)

def clean_last_updated(last_update):
    '''
    convert date and time in YYYYMMDD HMS format
    '''
    date = parse(str(last_update).split(' ')[0]).strftime("%Y-%m-%d")
    time = parse(str(last_update).split(' ')[1]).strftime('%H:%M:%S')
    parsed_date = str(date) + ' ' + str(time)

    return parsed_date

def get_date(last_update):
    return parse(str(last_update).split(' ')[0]).strftime("%Y-%m-%d")

def get_csv_date(file):
    return get_date(file.split('.')[0] + ' ')


def drop_duplicates(df_raw):
    '''
    Take the max date value for each province for a given date
    '''
    days_list = []
    
    for datetime in df_raw.date.unique():
        tmp_df = df_raw[df_raw.date == datetime]
        tmp_df = tmp_df.sort_values(['Last Update']).drop_duplicates('Province/State', keep='last')
        days_list.append(tmp_df)

    return days_list
    
def get_data(cleaned_sheets):
    all_csv = []
    # Import all CSV's
    for file in tqdm(sorted(cleaned_sheets), desc='... importing data: '):
        if 'csv' in file:
            # print('...', file)
            tmp_df = pd.read_csv(os.path.join(DATA, file), index_col=None, 
                                 header=0, parse_dates=['Last Update'])
            tmp_df = tmp_df[KEEP_COLS]
            tmp_df[NUMERIC_COLS] = tmp_df[NUMERIC_COLS].fillna(0)
            tmp_df[NUMERIC_COLS] = tmp_df[NUMERIC_COLS].astype(int)
            tmp_df['Province/State'].fillna(tmp_df['Country/Region'], inplace=True) #If no region given, fill it with country

            tmp_df['Last Update'] = tmp_df['Last Update'].apply(clean_last_updated)
            tmp_df['date'] = tmp_df['Last Update'].apply(get_date)
            tmp_df['file_date'] = get_csv_date(file)
            all_csv.append(tmp_df)

    # concatenate all csv's into one df
    df_raw = pd.concat(all_csv, axis=0, ignore_index=True, sort=True)
    df_raw = df_raw.sort_values(by=['Last Update'])

    frames = drop_duplicates(df_raw)
    tmp = pd.concat(frames, axis=0, ignore_index=True, sort=True)
    
    return tmp


# Now that we have all the data we now need to clean it 
# - Fill null values
# - remore suspected values
# - change column names
def clean_data(tmp_df):
    if 'Demised' in tmp_df.columns:
        tmp_df.rename(columns={'Demised':'Deaths'}, inplace=True)

    if 'Country/Region' in tmp_df.columns:
        tmp_df.rename(columns={'Country/Region':'country'}, inplace=True)
    
    if 'Province/State' in tmp_df.columns:
        tmp_df.rename(columns={'Province/State':'province'}, inplace=True)
        
    if 'Last Update' in tmp_df.columns:
        tmp_df.rename(columns={'Last Update':'datetime'}, inplace=True)
        
    if 'Suspected' in tmp_df.columns:
        tmp_df = tmp_df.drop(columns='Suspected')

    for col in tmp_df.columns:
        tmp_df[col] = tmp_df[col].fillna(0)
    
    #Lower case all col names
    tmp_df.columns = map(str.lower, tmp_df.columns) 
    return tmp_df
    

# use this function to fetch the data
def get():
        
    # Create Tmp Folder
    if not os.path.isdir(TMP_FOLDER):
        print('Creating folder...')
        print('...', TMP_FOLDER)
        os.mkdir(TMP_FOLDER)

    #Check if repo exists
    #git pull if it does
    if not os.path.isdir(TMP_GIT):
        clone_repo(TMP_FOLDER, REPO)
    else:
        try:
            print('git pull from', REPO)
            rep = git.Repo(TMP_GIT)
            rep.remotes.origin.pull()
        except:
            print('Could not pull from', REPO)
            sys.exit(1)

    sheets = os.listdir(DATA)
    
    # Clean the result to the sheet tabs we want
    print('Getting sheets...')
    cleaned_sheets = clean_sheet_names(sheets)

    # Aggregate all the data from sheets
    df = get_data(cleaned_sheets)
    
    #Clean the column names
    return clean_data(df)