import ezgmail
import time
import pandas as pd

from config import scraper_config, email_body, list_of_subscribers
from processor import run_core_processes, extract_all_beach_dataframes
from email_builder import build_email_body, initialise_email
from logger import log_application_header,log_application_footer, log_core_process_start_and_finish
from exporter import local_folder_table_dumps


log_application_header()
application_start_time = time.time()


initialise_email()

for key in scraper_config:
    run_core_processes(scraper_config, key)



scraper_config = extract_all_beach_dataframes(scraper_config, 'All')


for key in scraper_config:
    for contact in list_of_subscribers:
        if key in contact.beach_preferences:
            email_body[key] = build_email_body(scraper_config[key]['weekly_dataframe'], contact.name)
            ezgmail.send(contact.email, key+' Surf Report', email_body[key], [local_folder_table_dumps+'/'+key+'SurfReport.csv'])

log_application_footer(application_start_time)


# To Do List:
# - Add in snowboarding (This site - https://opensnow.com/location/cawhistler or this site https://www.snow-forecast.com/resorts/Whistler-Blackcomb/6day/mid)
# - Add in try and logging functions
# - Add in a list of emails
# - Add in Airflow https://towardsdatascience.com/getting-started-with-apache-airflow-df1aa77d7b1b
# - Change the ELIF statements and apply methods
# - What if the DF is empty? Both when extracted and when you send the email?
# - Make classes for each user(Cho, Harry, Ben, Jess)
# - rename columns
# - incorporate wind sysnopsis into the rating system (i.e. minus 2 for onshore)
# - Add in different websites to compare
# - Get them to work asyncronously
# - Fix decorative functions


# Done
# - x - Currently just Torquay but would like to expand it to other surf locations - x
# - x - Add in decorative functions - x
# - x - Create classes for each user and what they are opted in for - x
# - x - create an all files folder so you can just git ignore that, as opposed to each individual beach - x
