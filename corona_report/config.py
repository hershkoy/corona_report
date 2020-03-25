import os

#
# CLI 
#
SCRIPT = '/pipeline.sh'

#
# DATA PREP
#
REPO = 'https://github.com/CSSEGISandData/COVID-19.git'
TMP_FOLDER = '/tmp/corona/'
TMP_GIT = os.path.join(TMP_FOLDER, REPO.split('/')[-1].split('.')[0])
DATA = os.path.join(TMP_GIT, 'csse_covid_19_data', 'csse_covid_19_daily_reports')

#Github cols
KEEP_COLS = ['country',
             'province', 
             'confirmed',
             'deaths',
             'recovered',
             'date',
             'datetime',
             'file_date']

NUMERIC_COLS = ['confirmed', 
                'deaths', 
                'recovered']

UPDATE_INTERVAL = 40000
