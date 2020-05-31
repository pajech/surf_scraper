import pandas as pd
import time

from html_scraper import extract_url, extract_html
from config import scraper_config
from dataframe_builder import *
from logger            import log_core_process_start_and_finish, log_core_process_header
from exporter          import export_local

@log_core_process_start_and_finish
def run_beach_process(dict_of_beaches, beach):
    dict_of_beaches[beach]['response']               = extract_url(dict_of_beaches[beach]['url'])
    dict_of_beaches[beach]['soup_object']            = extract_html(dict_of_beaches[beach]['response'])
    dict_of_beaches[beach]['weekly_forecast_dict']   = build_forecast_dict(dict_of_beaches[beach]['soup_object'])
    dict_of_beaches[beach]['weekly_forecast_list']   = build_forecast_list(dict_of_beaches[beach]['weekly_forecast_dict'])
    dict_of_beaches[beach]['weekly_dataframe']       = build_forecast_df(dict_of_beaches[beach]['weekly_forecast_list'])
    dict_of_beaches[beach]['weekly_dataframe']       = add_wind_metrics(dict_of_beaches[beach]['weekly_dataframe'])
    dict_of_beaches[beach]['weekly_dataframe']       = add_day_date(dict_of_beaches[beach]['weekly_dataframe'])
    dict_of_beaches[beach]['weekly_dataframe']       = add_size_of_wave(dict_of_beaches[beach]['weekly_dataframe'])
    dict_of_beaches[beach]['weekly_dataframe']       = add_wind_speed(dict_of_beaches[beach]['weekly_dataframe'])
    dict_of_beaches[beach]['weekly_dataframe']       = add_swell_period(dict_of_beaches[beach]['weekly_dataframe'])
    dict_of_beaches[beach]['weekly_dataframe']       = add_swell_height_rating(dict_of_beaches[beach]['weekly_dataframe'])
    dict_of_beaches[beach]['weekly_dataframe']       = add_swell_period_rating(dict_of_beaches[beach]['weekly_dataframe'])
    dict_of_beaches[beach]['weekly_dataframe']       = add_wind_rating(dict_of_beaches[beach]['weekly_dataframe'])
    dict_of_beaches[beach]['weekly_dataframe']       = add_day_of_week(dict_of_beaches[beach]['weekly_dataframe'])
    dict_of_beaches[beach]['weekly_dataframe']       = add_total_rating(dict_of_beaches[beach]['weekly_dataframe'])
    dict_of_beaches[beach]['weekly_dataframe']       = filter_to_high_rating(dict_of_beaches[beach]['weekly_dataframe'])
    dict_of_beaches[beach]['weekly_dataframe']       = filter_to_relevant_cols(dict_of_beaches[beach]['weekly_dataframe'])
    dict_of_beaches[beach]['weekly_dataframe']       = filter_out_nocturnal_times(dict_of_beaches[beach]['weekly_dataframe'])
    dict_of_beaches[beach]['weekly_dataframe']       = add_in_beach_name(scraper_config[beach]['weekly_dataframe'], beach)
    export_local(dict_of_beaches[beach]['weekly_dataframe'], beach)     
    dict_of_beaches[beach]['weekly_dataframe']       = sort_by_high_rating(dict_of_beaches[beach]['weekly_dataframe'])
    return dict_of_beaches

@log_core_process_start_and_finish
def extract_all_beach_dataframes(dict_of_beaches, beach):
    scraper_config[beach] = {}
    scraper_config[beach]['weekly_dataframe']               = pd.DataFrame()
    dict_of_beaches[beach]['weekly_dataframe']              =  concatenate_dataframes(dict_of_beaches, 'weekly_dataframe')
    dict_of_beaches[beach]['weekly_dataframe']              = sort_by_high_rating(dict_of_beaches[beach]['weekly_dataframe'])
    export_local(dict_of_beaches[beach]['weekly_dataframe'], beach)
    return dict_of_beaches

# @log_core_process_start_and_finish
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
    
    # 
