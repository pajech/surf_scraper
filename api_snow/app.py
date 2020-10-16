import ezgmail
import time
import pandas as pd
import sys
import os
import requests
import pathlib
import sys; sys.path.append(pathlib.Path(__file__).parent.absolute().parent.as_posix())
sys.path.append(pathlib.Path(__file__).parent.absolute().parent.parent.as_posix())

from general.config import scraper_config_snow, snow_api_key, snow_api_secret
from api_snow.weatherunlocked import get_snow

resort_id = scraper_config_snow['Thredbo']['api_id']
APP_ID = snow_api_key
APP_KEY = snow_api_secret


thredbo_url = f'https://api.weatherunlocked.com/api/resortforecast/{resort_id}?app_id={APP_ID}&app_key={APP_KEY}'
print(thredbo_url)
thredbo_forecast = get_snow(thredbo_url)

df_new_list = []
for i, datapoint in enumerate(thredbo_forecast.data):
    hourly_dict = datapoint.attrs
    df = pd.DataFrame.from_records(hourly_dict, index=[0])
    df_new_list.append(df)
df_new = pd.concat(df_new_list, sort = False)
df_new = df_new.set_index(['date','time'])

print(df_new.head())