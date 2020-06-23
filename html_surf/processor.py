import pandas as pd
import time

from general.html_scraper import extract_url, extract_html
from general.config import scraper_config
from general.dataframe_builder import *
from general.logger            import log_core_process_start_and_finish, log_core_process_header
from general.exporter          import export_local


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