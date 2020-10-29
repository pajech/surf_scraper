import ezgmail
import time
import pandas as pd
import sys
import os
import pathlib
import sys; sys.path.append(pathlib.Path(__file__).parent.absolute().parent.as_posix())
sys.path.append(pathlib.Path(__file__).parent.absolute().parent.parent.as_posix())

from general.html_scraper import extract_url
from general.config import scraper_config, email_body, email_body_snow, sms_body_snow, list_of_subscribers, scraper_config_snow, api_key
from html_snow.processor import run_snow_process
from general.email_builder import build_email_body, initialise_email, build_email_body_snow
from general.logger import log_application_header,log_application_footer, log_core_process_start_and_finish
from general.exporter import local_folder_table_dumps
from general.sms_builder import *



log_application_header()
application_start_time = time.time()

initialise_email()
create_subscription(token)
# create_bnum(token)

for key in scraper_config_snow:
    run_snow_process(scraper_config_snow, key)

for key in scraper_config_snow:
    for contact in list_of_subscribers:
        if key in contact.snow_preferences:
            email_body_snow[key] = build_email_body_snow(key, scraper_config_snow[key]['dataframe'], contact.name,scraper_config_snow[key]['mountain_snowfall'] )
            ezgmail.send(contact.email, key+' Snow Report', email_body_snow[key], local_folder_table_dumps+'/'+key+'SnowReport.csv')

            sms_body_snow[key] = build_sms_body_snow(key, scraper_config_snow[key]['dataframe'], contact.name, scraper_config_snow[key]['mountain_snowfall'] )
            if sms_body_snow[key] != None:
                send_sms(token, contact.phone_number, sms_body_snow[key])
    os.remove(local_folder_table_dumps+'/'+key+'SnowReport.csv')
    os.remove(local_folder_table_dumps+'/'+key+'Dict.csv')   
                

log_application_footer(application_start_time)


# To Do List:

