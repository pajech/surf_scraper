import ezgmail
import time
import pandas as pd
import sys
import os
import pathlib
# sys.path.insert(1, os.path.normpath(os.getcwd() + os.sep + os.pardir))
import sys; sys.path.append(pathlib.Path(__file__).parent.absolute().parent.as_posix())
sys.path.append(pathlib.Path(__file__).parent.absolute().parent.parent.as_posix())

import requests


from general.config import scraper_config, email_body, sms_body, email_body_snow, list_of_subscribers, scraper_config_snow, api_key,sms_key, sms_secret
from html_surf.processor import run_beach_process, extract_all_beach_dataframes
from general.email_builder import build_email_body, initialise_email, build_email_body_snow
from general.logger import log_application_header,log_application_footer, log_core_process_start_and_finish
from general.exporter import local_folder_table_dumps
from general.sms_builder import * 


log_application_header()
application_start_time = time.time()


# Scraper:
initialise_email()
create_subscription(token)
create_bnum(token)

for key in scraper_config:
    run_beach_process(scraper_config, key)

scraper_config = extract_all_beach_dataframes(scraper_config, 'All')

for key in scraper_config:
    for contact in list_of_subscribers:
        if key in contact.beach_preferences:
            email_body[key] = build_email_body(scraper_config[key]['weekly_dataframe'], contact.name)
            ezgmail.send(contact.email, key+' Surf Report', email_body[key], [local_folder_table_dumps+'/'+key+'SurfReport.csv'])

            sms_body[key] = build_sms_body(scraper_config[key]['weekly_dataframe'], contact.name)
            send_sms(token, contact.phone_number, sms_body[key])

for key in scraper_config:
    os.remove(local_folder_table_dumps+'/'+key+'SurfReport.csv')
    os.remove(local_folder_table_dumps+'/'+key+'Dict.csv')





# log_application_footer(application_start_time)


# To Do List:

