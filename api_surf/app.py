import ezgmail
import time
import pandas as pd
import sys
import os
sys.path.insert(1, '/Users/paul.chynoweth/git_repo/surf_scraper')

# Local Libraries
from api_surf.magicseaweed import MSW_Forecast
from general.config import api_key, scraper_config
from general.dataframe_builder import *
from api_surf.processor import run_beach_process_api

# Log application start

# for key in scraper_config:
#     run_beach_process_api(scraper_config, key)



# janjuc_forecast = MSW_Forecast(api_key, janjuc_id, unit = 'uk')
# janjuc_future = janjuc_forecast.get_future()

# df_new_list = []
# for i, forecast in enumerate(janjuc_future.data):
#     # if i == 0:
#     #     print(forecast.attrs)
#     #     print(forecast.charts_swell)
#     #     print(forecast.get_swell_url('combined'))
#     #     print(forecast.get_wind_url())
#     #     print(forecast.__getattr__('swell_absMaxBreakingHeight'))
#     hourly_dict = forecast.attrs
#     df = pd.DataFrame.from_records(hourly_dict, index=[0])
#     df_new_list.append(df)
#     # print(df)

# df_new = pd.concat(df_new_list, sort = False)
# df_new['temp_time'] = df_new['begins'].str.split(' ', n = 1, expand = True)[1]
# df_new['size_of_wave'] = df_new['max_breaking_height'].str.split(' ', n = 1, expand = True)[0].astype(int)
# df_new['breaking_height'] = df_new['min_breaking_height'].str.split(' ', n = 1, expand = True)[0] +'-'+ df_new['max_breaking_height']

# df_new['temp_stars_solid'] = df_new['stars'].str.split(' ', n = 3, expand = True)[0].astype(int)
# df_new['temp_stars_faded'] = df_new['stars'].str.split(' ', n = 3, expand = True)[2].astype(int)

# df_new['swell_period_int'] = df_new['swell_period'].str.split(' ', n = 1, expand = True)[0].astype(int)

# df_new['wind_speed2'] = df_new['wind_speed'].str.split(' ', n = 1, expand = True)[0].astype(int)
# df_new['temp_wind_gusts'] = df_new['wind_gusts'].str.split(' ', n = 1, expand = True)[0].astype(int)
# df_new['wind'] = df_new['wind_speed'].str.split(' ', n = 1, expand = True)[0] +'-'+ df_new['wind_gusts']

# df_new       = add_swell_height_rating(df_new)
# df_new       = add_swell_period_rating(df_new)
# df_new       = add_wind_rating(df_new)    
# df_new       = add_total_rating(df_new)

# df_new       = filter_to_high_rating(df_new)
# df_new       = filter_to_relevant_cols(df_new)
# df_new       = filter_out_nocturnal_times(df_new)
# df_new       = add_in_beach_name(scraper_config[beach], beach)   
# df_new       = sort_by_high_rating(df_new)


# print(df_new.head())
# print(df_new.columns.values.tolist())




# Run processory/df builder

# Email



# To do list:
# HOw to render the graphs from the URLs