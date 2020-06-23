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


# Run processory/df builder
for key in scraper_config:
    run_beach_process_api(scraper_config, key)

# Email



# To do list:
# Add in Email
# Add in SMS