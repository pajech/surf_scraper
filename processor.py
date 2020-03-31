import pandas as pd
import time

from config import scraper_config

from html_scraper import extract_url, extract_html

from dataframe_builder import build_forecast_dict, build_forecast_list, build_forecast_df, add_wind_metrics
from dataframe_builder import add_day_date, add_size_of_wave, add_wind_speed, add_swell_period, add_swell_height_rating
from dataframe_builder import add_swell_period_rating, add_wind_rating, add_day_of_week, add_total_rating
from dataframe_builder import filter_to_high_rating, filter_to_relevant_cols, filter_out_nocturnal_times, sort_by_high_rating, add_in_beach_name,concatenate_dataframes
from logger            import log_core_process_start_and_finish, log_core_process_header

@log_core_process_start_and_finish
def run_core_processes(dict_of_beaches, beach):
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
    dict_of_beaches[beach]['weekly_dataframe'].to_csv(beach+'SurfReport.csv', index = False)
    dict_of_beaches[beach]['weekly_dataframe']       = sort_by_high_rating(dict_of_beaches[beach]['weekly_dataframe'])
    return dict_of_beaches

@log_core_process_start_and_finish
def extract_all_beach_dataframes(dict_of_beaches, beach):
    scraper_config[beach] = {}
    scraper_config[beach]['weekly_dataframe']           = pd.DataFrame()
    dict_of_beaches[beach]['weekly_dataframe']           =  concatenate_dataframes(dict_of_beaches, 'weekly_dataframe')
    dict_of_beaches[beach]['weekly_dataframe']          = sort_by_high_rating(dict_of_beaches[beach]['weekly_dataframe'])
    dict_of_beaches[beach]['weekly_dataframe'].to_csv('All'+'SurfReport.csv', index = False)
    return dict_of_beaches


