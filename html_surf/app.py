import ezgmail
import time
import pandas as pd
import sys
sys.path.insert(1, '/Users/paul.chynoweth/git_repo/surf_scraper')


from general.config import scraper_config, email_body, email_body_snow, list_of_subscribers, scraper_config_snow, api_key
from html_surf.processor import run_beach_process, extract_all_beach_dataframes
from general.email_builder import build_email_body, initialise_email, build_email_body_snow
from general.logger import log_application_header,log_application_footer, log_core_process_start_and_finish
from general.exporter import local_folder_table_dumps


log_application_header()
application_start_time = time.time()


# Scraper:
initialise_email()

for key in scraper_config:
    run_beach_process(scraper_config, key)

scraper_config = extract_all_beach_dataframes(scraper_config, 'All')

for key in scraper_config:
    for contact in list_of_subscribers:
        if key in contact.beach_preferences:
            email_body[key] = build_email_body(scraper_config[key]['weekly_dataframe'], contact.name)
            ezgmail.send(contact.email, key+' Surf Report', email_body[key], [local_folder_table_dumps+'/'+key+'SurfReport.csv'])







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
