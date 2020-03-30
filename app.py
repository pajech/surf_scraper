import ezgmail
import time

from config import scraper_config, email_body
from processor import run_core_processes
from email_builder import build_email_body, initialise_email
from logger import log_application_header,log_application_footer, log_core_process_start_and_finish


log_application_header()
application_start_time = time.time()


initialise_email()

for key in scraper_config:

    run_core_processes(scraper_config, key)
    email_body[key] = build_email_body(scraper_config[key]['weekly_dataframe'])
    ezgmail.send('paulychynoweth@gmail.com', key+' Surf Report', email_body[key], [key+'SurfReport.csv'])

log_application_footer(application_start_time)

# run_core_processes(scraper_config, 'JanJuc')




# email_body['Torquay'] = build_email_body(scraper_config['Torquay']['weekly_dataframe'])
# email_body['JanJuc'] = build_email_body(scraper_config['JanJuc']['weekly_dataframe'])

# ezgmail.send('paulychynoweth@gmail.com', 'Surf Report', email_body['Torquay'], ['TorquaySurfReport.csv'])
# ezgmail.send('paulychynoweth@gmail.com', 'Surf Report', email_body['JanJuc'], ['JanJucSurfReport.csv'])


# To Do List:
# - Add in snowboarding
# - Add in decorative functions
# - Add in try and logging functions
# - Add in a list of emails
# - Create classes for each user and what they are opted in for
# - Add in Airflow https://towardsdatascience.com/getting-started-with-apache-airflow-df1aa77d7b1b
# - Change the ELIF statements and apply methods
# - What if the DF is empty? Both when extracted and when you send the email?
# - Make classes for each user(Cho, Harry, Ben, Jess)
# - rename columns
# - incorporate wind sysnopsis into the rating system (i.e. minus 2 for onshore)
# - Add in different websites to compare
# - Get them to work asyncronously

# Done
# - x - Currently just Torquay but would like to expand it to other surf locations - x
