import ezgmail
import time
import pandas as pd

from config import scraper_config, email_body, email_body_snow, list_of_subscribers, scraper_config_snow, api_key
from processor import run_beach_process, extract_all_beach_dataframes, run_snow_process
from email_builder import build_email_body, initialise_email, build_email_body_snow
from logger import log_application_header,log_application_footer, log_core_process_start_and_finish
from exporter import local_folder_table_dumps
from magicseaweed import MSW_Forecast
from secrets import api_key

log_application_header()
application_start_time = time.time()


# Scraper:
# initialise_email()

# for key in scraper_config:
#     run_beach_process(scraper_config, key)

# scraper_config = extract_all_beach_dataframes(scraper_config, 'All')

# for key in scraper_config:
#     for contact in list_of_subscribers:
#         if key in contact.beach_preferences:
#             email_body[key] = build_email_body(scraper_config[key]['weekly_dataframe'], contact.name)
#             ezgmail.send(contact.email, key+' Surf Report', email_body[key], [local_folder_table_dumps+'/'+key+'SurfReport.csv'])

# for key in scraper_config_snow:
#     run_snow_process(scraper_config_snow, key)

# for key in scraper_config_snow:
#     for contact in list_of_subscribers:
#         if key in contact.snow_preferences:
#             email_body_snow[key] = build_email_body_snow(key, scraper_config_snow[key]['dataframe'], contact.name)
#             ezgmail.send(contact.email, key+' Snow Report', email_body_snow[key], [local_folder_table_dumps+'/'+key+'SnowReport.csv'])

# API Connector:

# Surf API 
janjuc_id = 1066
janjuc_forecast = MSW_Forecast(api_key, janjuc_id, unit = 'uk')
janjuc_future = janjuc_forecast.get_future()

df_new_list = []
for i, forecast in enumerate(janjuc_future.data):
    hourly_dict = forecast.attrs
    df = pd.DataFrame.from_records(hourly_dict, index=[0])
    df_new_list.append(df)
    # df = pd.DataFrame(hourly_dict.items(), columns = list(hourly_dict.keys()) )
    # # if i == 0:
    #     # print(df)

df_new = pd.concat(df_new_list, sort = False)

df_new.to_csv('beach_files/surfcrawler_api_test.csv')
print(df_new.columns.values.tolist())






# log_application_footer(application_start_time)


# To Do List:
# - Add in try and logging functions
# - Add in Airflow https://towardsdatascience.com/getting-started-with-apache-airflow-df1aa77d7b1b
# - Change the ELIF statements and apply methods
# - What if the DF is empty? Both when extracted and when you send the email?
# - rename columns
# - incorporate wind sysnopsis into the rating system (i.e. minus 2 for onshore)
# - Add in different websites to compare
# - Get them to work asyncronously
# - Fix decorative functions
