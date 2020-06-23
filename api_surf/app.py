import ezgmail
import time
import pandas as pd
import sys
import os
sys.path.insert(1, '/Users/paul.chynoweth/git_repo/surf_scraper')

# Local Libraries
from api_surf.magicseaweed import MSW_Forecast
from general.config import api_key



# Log application start
janjuc_id = 1066


janjuc_forecast = MSW_Forecast(api_key, janjuc_id, unit = 'uk')
janjuc_future = janjuc_forecast.get_future()

df_new_list = []
for i, forecast in enumerate(janjuc_future.data):
    # if i == 0:
    #     print(forecast.attrs)
    #     print(forecast.charts_swell)
    #     print(forecast.get_swell_url('combined'))
    #     print(forecast.get_wind_url())
    #     print(forecast.__getattr__('swell_absMaxBreakingHeight'))
    hourly_dict = forecast.attrs
    df = pd.DataFrame.from_records(hourly_dict, index=[0])
    df_new_list.append(df)
    # print(df)

df_new = pd.concat(df_new_list, sort = False)




# Run processory/df builder

# Email



# To do list:
# HOw to render the graphs from the URLs