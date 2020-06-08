import pandas as pd
import time

from general.html_scraper import extract_url, extract_html
from general.config import scraper_config
from general.dataframe_builder import *
from general.logger            import log_core_process_start_and_finish, log_core_process_header
from general.exporter          import export_local

def run_snow_process(dict_of_resorts, resort):
    dict_of_resorts[resort]['response']                                                        = extract_url(dict_of_resorts[resort]['url']) 
    dict_of_resorts[resort]['soup_object']                                                     = extract_html(dict_of_resorts[resort]['response'])
    dict_of_resorts[resort]['weekly_forecast_list'], dict_of_resorts[resort]['date_remap']     = generate_weekly_dict(dict_of_resorts[resort]['soup_object'])
    dict_of_resorts[resort]['dataframe']                                                       = convert_list_to_df(dict_of_resorts[resort]['weekly_forecast_list'])
    dict_of_resorts[resort]                                                                    = add_date(dict_of_resorts[resort])
    dict_of_resorts[resort]['dataframe']                                                       = replace_nulls(dict_of_resorts[resort]['dataframe'])
    dict_of_resorts[resort]['dataframe']                                                       = convert_dtype(dict_of_resorts[resort]['dataframe'], int)
    dict_of_resorts[resort]['dataframe']                                                       = groupby_dataframe(dict_of_resorts[resort]['dataframe'])
    dict_of_resorts[resort]['dataframe']                                                       = add_mountain_heights(dict_of_resorts[resort]['dataframe'], dict_of_resorts[resort]['soup_object'])
    dict_of_resorts[resort]['dataframe']                                                       = add_freezing_level(dict_of_resorts[resort]['dataframe'])
    dict_of_resorts[resort]['dataframe']                                                       = add_localised_date(dict_of_resorts[resort]['dataframe'],  dict_of_resorts[resort]['soup_object'])
    dict_of_resorts[resort]['dataframe']                                                       = add_snowfall_synopsis(dict_of_resorts[resort]['dataframe'])
    dict_of_resorts[resort]['dataframe']                                                       = dict_of_resorts[resort]['dataframe'][['day_of_week', 'wind', 'snowfall', 'rain', 'temp', 'humidity', 'freezing_level', 'wind_description', 'freezing_level_synopsis', 'date_lcl_formatted', 'snowfall_synopsis']]
    export_local(dict_of_resorts[resort]['dataframe'], resort, surf_or_snow='Snow')     
    return dict_of_resorts