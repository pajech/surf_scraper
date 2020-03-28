from config import scraper_config
from processor import run_core_processes
from email_builder import build_email_body

import ezgmail

run_core_processes(scraper_config, 'Torquay')

ezgmail.init()

email_body = build_email_body(scraper_config['Torquay']['weekly_dataframe'])

ezgmail.send('paulychynoweth@gmail.com', 'Surf Report', email_body, ['TorquaySurfReport.csv'])


# To Do List:
# - Currently just Torquay but would like to expand it to other surf locations
# - Add in transformations and other modules to expand it out
# - Add in snowboarding
# - Add in decorative functions
# - Add in try and logging functions
# - Add in a list of emails
# - Create classes for each user and what they are opted in for
# - Add in Airflow https://towardsdatascience.com/getting-started-with-apache-airflow-df1aa77d7b1b
# - Change the ELIF statements and apply methods
