from general.config import api_key
from api_surf.magicseaweed import MSW_Forecast
from general.dataframe_builder import *

def run_beach_process_api(dict_of_beaches, beach):
    if beach == 'JanJuc':
        dict_of_beaches[beach]['forecast'] = MSW_Forecast(api_key, dict_of_beaches[beach]['spot_id'], unit = 'uk')
        dict_of_beaches[beach]['forecast_future'] = dict_of_beaches[beach]['forecast'].get_future()
        dict_of_beaches[beach]['weekly_dataframe'] = compile_api_dataframe(dict_of_beaches[beach]['forecast_future'])
        dict_of_beaches[beach]['weekly_dataframe']['temp_time'] = dict_of_beaches[beach]['weekly_dataframe']['begins'].str.split(' ', n = 1, expand = True)[1]
        dict_of_beaches[beach]['weekly_dataframe']['size_of_wave'] = dict_of_beaches[beach]['weekly_dataframe']['max_breaking_height'].str.split(' ', n = 1, expand = True)[0].astype(int)
        dict_of_beaches[beach]['weekly_dataframe']['breaking_height'] = dict_of_beaches[beach]['weekly_dataframe']['min_breaking_height'].str.split(' ', n = 1, expand = True)[0] +'-'+ dict_of_beaches[beach]['weekly_dataframe']['max_breaking_height']
        dict_of_beaches[beach]['weekly_dataframe']['swell_period_int'] = dict_of_beaches[beach]['weekly_dataframe']['swell_period'].str.split(' ', n = 1, expand = True)[0].astype(int)
        dict_of_beaches[beach]['weekly_dataframe']['wind_speed2'] = dict_of_beaches[beach]['weekly_dataframe']['wind_speed'].str.split(' ', n = 1, expand = True)[0].astype(int)
        dict_of_beaches[beach]['weekly_dataframe']['wind'] = dict_of_beaches[beach]['weekly_dataframe']['wind_speed'].str.split(' ', n = 1, expand = True)[0] +'-'+ dict_of_beaches[beach]['weekly_dataframe']['wind_gusts']
        dict_of_beaches[beach]['weekly_dataframe']       = add_swell_height_rating(dict_of_beaches[beach]['weekly_dataframe'])
        dict_of_beaches[beach]['weekly_dataframe']       = add_swell_period_rating(dict_of_beaches[beach]['weekly_dataframe'])
        dict_of_beaches[beach]['weekly_dataframe']       = add_wind_rating(dict_of_beaches[beach]['weekly_dataframe'])    
        dict_of_beaches[beach]['weekly_dataframe']       = add_total_rating(dict_of_beaches[beach]['weekly_dataframe'])
        print(dict_of_beaches[beach]['weekly_dataframe'].head())        
        
        
# To Do List:
# - rename columns
# - filter to relevant columns
# - filter out nocturnal hours
# - add in beach name
# - sort by higher rating
# - add in photos        
        