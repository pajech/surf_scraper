import pandas as pd
from logger import log_start_and_finish

@log_start_and_finish
def build_forecast_dict(soup_object):
    weekly_forecast_dict = {}
    for i in range (1,8):
        daily_table = soup_object.findAll('tr',{'data-forecast-day':str(i)})
        weekly_forecast_dict[i] = daily_table
    
    return weekly_forecast_dict

@log_start_and_finish
def build_forecast_list(forecast_dict):
    weekly_forecast_list = []
    for key in forecast_dict:
        #Loop through dictionary to gather the relevant surf forecast for each day
        day_forecast_list = []
        for i in range (8):
            #Loop through each hour segment (only 8 as they don't do all 24) and split up the key information
            hour_forcast = forecast_dict[key][i].text.split()
            #Sometimes additional 2 fields are included in the forecast (i.e. secondary swell), they aren't needed
            if len(hour_forcast) == 11:
                del hour_forcast[4:6]
            #Sometimes additional 4 fields are included in the forecast (i.e. secondary swell), they aren't needed
            elif len(hour_forcast)==13:
                del hour_forcast[4:8]
            
            #append the day date to the list 
            hour_forcast = [forecast_dict[key][i]['data-date-anchor']] + hour_forcast
            
            wind_desc_index = len(forecast_dict[key][i].find_all('td')) - 4
            for i,td in enumerate(forecast_dict[key][i].find_all('td')):
                if i == wind_desc_index:
                    wind_desc = str(td.get('title')).split('-')[0]
                    wind_desc_list = []
                    wind_desc_list.append(wind_desc)
            hour_forcast = hour_forcast + wind_desc_list
            
            
            #Append the hourly data to the day forecast
            day_forecast_list.append(hour_forcast)
        
        #Append the day data to the weekly forecast
        weekly_forecast_list.append(day_forecast_list)
    
    return weekly_forecast_list

@log_start_and_finish
def build_forecast_df(forecast_list):
    # ============================================================================= Convert List into a Dataframe
    columns = ['daydate','time', 'size', 'primary_swell','swell_period','wind_speed1','wind_speed2','wind_metrics', 'temperature','probability','wind_synopsis']
    weekly_dataframe = pd.DataFrame(columns=columns)
    for i in range (7):
        df = pd.DataFrame(forecast_list[i], columns = columns)
        #print(df)
        weekly_dataframe = weekly_dataframe.append(df)
    
    return weekly_dataframe

@log_start_and_finish
def add_wind_metrics(dataframe):
    #Check to see if winds exist here
    dataframe['wind'] = dataframe['wind_speed1'] +'-'+ dataframe['wind_speed2'] + ' '+ dataframe['wind_metrics'] 
    return dataframe

@log_start_and_finish
def add_day_date(dataframe):
    # Add Try and Logging
    day_date_split = dataframe["daydate"].str.split("(\d\d\d\d)", n = 1, expand = True) 
    dataframe['day_of_week'] = day_date_split[0]
    dataframe['date'] = day_date_split[1]
    return dataframe

@log_start_and_finish
def add_size_of_wave(dataframe):
    dataframe['size_of_wave'] = dataframe['primary_swell'].str.split("ft", n=1, expand = True)[0]
    dataframe['size_of_wave'] = dataframe['size_of_wave'].astype('float')
    return dataframe

@log_start_and_finish
def add_wind_speed(dataframe):
    dataframe['wind_speed1'] = dataframe['wind_speed1'].astype('int')
    dataframe['wind_speed2'] = dataframe['wind_speed2'].astype('int')
    return dataframe

@log_start_and_finish
def add_swell_period(dataframe):
    dataframe['swell_period_int'] = dataframe['swell_period'].str.split("s", n=1, expand = True)[0]
    dataframe['swell_period_int'] = dataframe['swell_period_int'].astype('int')
    return dataframe

@log_start_and_finish
def add_swell_height_rating(dataframe):
    def add_rating(row):
        swell_height = row['size_of_wave']
        if swell_height <1:
            return 2
        elif swell_height < 2:
            return 4
        elif swell_height < 3:
            return 6
        elif swell_height < 4:
            return 8
        elif swell_height < 5:
            return 10
        elif swell_height < 6:
            return 8
        elif swell_height < 7:
            return 6
        elif swell_height < 8:
            return 4
        elif swell_height < 9:
            return 2
        else:
            return 0
    dataframe['heigh_rating']=dataframe.apply(lambda row: add_rating (row), axis="columns")
    return dataframe

@log_start_and_finish
def add_swell_period_rating(dataframe):
    def add_rating(row):
        swell_period = row['swell_period_int']
        if swell_period <8:
            return 2
        elif swell_period <9:
            return 4
        elif swell_period < 11:
            return 5
        elif swell_period < 13:
            return 6
        elif swell_period < 15:
            return 8
        else:
            return 10
    dataframe['swellperiod_rating']=dataframe.apply(lambda row: add_rating (row), axis="columns")
    return dataframe

@log_start_and_finish
def add_wind_rating(dataframe):
    def add_rating(row):
        wind_speed = row['wind_speed2']
        
        if wind_speed <5:
            return 10
        elif wind_speed <10:
            return 8
        elif wind_speed < 15:
            return 6
        elif wind_speed < 20:
            return 5
        elif wind_speed < 25:
            return 3
        else:
            return 1

    dataframe['wind_rating']=dataframe.apply(lambda row: add_rating(row), axis="columns")
    return dataframe

@log_start_and_finish
def add_total_rating(dataframe):
    dataframe['total_rating'] = dataframe['wind_rating'] + dataframe['swellperiod_rating'] + dataframe['heigh_rating']
    return dataframe

@log_start_and_finish
def filter_to_high_rating(dataframe):
    dataframe = dataframe[dataframe['total_rating']>15]
    return dataframe

@log_start_and_finish
def add_day_of_week(dataframe):
    dataframe['day_of_week'] = dataframe['daydate'].str.split(r'[0-9]', expand=True)
    return dataframe

@log_start_and_finish
def filter_to_relevant_cols(dataframe):
    dataframe = dataframe[['daydate','time','size','swell_period','wind','total_rating','day_of_week','wind_synopsis']]
    return dataframe

@log_start_and_finish
def sort_by_high_rating(dataframe):
    dataframe = dataframe.sort_values(by='total_rating', ascending = False)
    return dataframe

@log_start_and_finish
def filter_out_nocturnal_times(dataframe):
    dataframe = dataframe[dataframe['time'].isin(['6am','9am','Noon','3pm'])]
    return dataframe

@log_start_and_finish
def add_in_beach_name(dataframe, beach):
    dataframe['beach'] = beach
    return dataframe

def concatenate_dataframes(dict_of_dataframes, df_name):
    list_of_dataframes = []
    for key in dict_of_dataframes:
        list_of_dataframes.append(dict_of_dataframes[key][df_name])
    final_dataframe = pd.concat(list_of_dataframes, ignore_index = True, sort = False)
    return final_dataframe