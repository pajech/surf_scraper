import pandas as pd
import numpy as np
from general.logger import log_start_and_finish
from string import printable
from datetime import timedelta

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


# Snow functions
weekday_renaming_dict = {
    'Thu':'Thursday',
    'Fri':'Friday',
    'Sat':'Saturday',
    'Sun':'Sunday',
    'Mon':'Monday',
    'Tue':'Tuesday',
    'Wed':'Wednesday'
}

# @log_start_and_finish
def generate_weekly_dict(soup_object):
    day_of_week = soup_object.findAll('div', class_ = 'forecast-table-days__name')[0].text
    if len(day_of_week) < 4:
        max_range = 17
    else:
        max_range = 18

    weekly_forecast_series_list = []
    weekly_snow_forecast_dict = {
                                    'day_of_week':{
                                        'range_start':0,
                                        'range_end':6,
                                        'html_element':'div',
                                        'class':'forecast-table-days__name',
                                        'final_list':[]
                                    },
                                    'time_of_day':{
                                        'range_start':0,
                                        'range_end':max_range,
                                        'html_element':'span',
                                        'class':'forecast-table-time__period en',
                                        'final_list':[]
                                    },
                                    'wind':{
                                        'range_start':3,
                                        'range_end':max_range + 3,
                                        'html_element':'text',
                                        'class':'wind-icon-val wind',
                                        'final_list':[]
                                    },
                                    'wind_description':{
                                        'range_start':0,
                                        'range_end':max_range,
                                        'html_element':'span',
                                        'class':'forecast-table-phrases__value en',
                                        'final_list':[]
                                    },
                                    'snowfall':{
                                        'range_start':0,
                                        'range_end':max_range,
                                        'html_element':'div',
                                        'class':'forecast-table-snow__container',
                                        'final_list':[]
                                    },
                                    'rain':{
                                        'range_start':0,
                                        'range_end':max_range,
                                        'html_element':'div',
                                        'class':'forecast-table-rain__container',
                                        'final_list':[]
                                    },
                                    'temp':{
                                        'range_start':0,
                                        'range_end':max_range,
                                        'html_element':'div',
                                        'class':'forecast-table-temp__container',
                                        'final_list':[]
                                    },
                                    'humidity':{
                                        'range_start':0,
                                        'range_end':max_range,
                                        'html_element':'div',
                                        'class':'forecast-table-humidity__container',
                                        'final_list':[]
                                    },
                                    'freezing_level':{
                                        'range_start':0,
                                        'range_end':max_range,
                                        'html_element':'div',
                                        'class':'forecast-table-freezing-level__container',
                                        'final_list':[]
                                    }
                                }
    
    for key in weekly_snow_forecast_dict:
        if key in ['day_of_week']:
        
            for i in range(weekly_snow_forecast_dict[key]['range_start'], weekly_snow_forecast_dict[key]['range_end']):
                item = soup_object.findAll(weekly_snow_forecast_dict[key]['html_element'], class_ = weekly_snow_forecast_dict[key]['class'])[i].text
                if len(item) < 4:
                    item = weekday_renaming_dict[item]
                    list_of_items = [item,item] 
                else:
                    list_of_items = [item,item,item]
                
                weekly_snow_forecast_dict[key]['final_list'] = weekly_snow_forecast_dict[key]['final_list'] + list_of_items
    
        elif key in ['wind_description']:
            for i in range(weekly_snow_forecast_dict[key]['range_start'], weekly_snow_forecast_dict[key]['range_end']):
                weekly_snow_forecast_dict[key]['final_list'] = weekly_snow_forecast_dict[key]['final_list'] + [soup_object.findAll(weekly_snow_forecast_dict[key]['html_element'], class_ = weekly_snow_forecast_dict[key]['class'])[i].text]
                    
        else:
            for i in range(weekly_snow_forecast_dict[key]['range_start'], weekly_snow_forecast_dict[key]['range_end']):
                weekly_snow_forecast_dict[key]['final_list'] = weekly_snow_forecast_dict[key]['final_list'] + soup_object.findAll(weekly_snow_forecast_dict[key]['html_element'], class_ = weekly_snow_forecast_dict[key]['class'])[i].text.split()
            
    
        weekly_snow_forecast_dict[key]['final_series'] = pd.Series(weekly_snow_forecast_dict[key]['final_list'], name = key)   
    
    
        weekly_forecast_series_list.append(weekly_snow_forecast_dict[key]['final_series']) 

        day_to_date_dict= {}
        for i in range(0,6):
            item = soup_object.findAll(weekly_snow_forecast_dict['day_of_week']['html_element'], class_ = weekly_snow_forecast_dict['day_of_week']['class'])[i].text
            if len(item) < 4:
                        item = weekday_renaming_dict[item]
            
            day_to_date_dict[item] = soup_object.findAll('div', class_ = 'forecast-table-days__date')[i].text

    return weekly_forecast_series_list, day_to_date_dict


def convert_list_to_df(list_object):
    dataframe = pd.concat(list_object, axis=1)
    return dataframe

def add_date(resort_dict):
   resort_dict['dataframe']['day_date'] = resort_dict['dataframe']['day_of_week'].map(resort_dict['date_remap'])
   return resort_dict


def replace_nulls(dataframe):
    dataframe.replace('-','0', inplace = True)
    return dataframe

def convert_dtype(dataframe, dtype):
    dataframe['rain']              = dataframe['rain'].astype(dtype)
    dataframe['snowfall']          = dataframe['snowfall'].astype(dtype)
    dataframe['freezing_level']    = dataframe['freezing_level'].astype(dtype)
    return dataframe

def groupby_dataframe(dataframe):
    merge_df = pd.merge(
        dataframe.groupby('day_of_week', sort=False, as_index = False).agg({'wind':'max','snowfall':'sum','rain':'sum','temp':'max','humidity':'max','freezing_level':'max','day_date':'first'}),
        dataframe.groupby('day_of_week')['wind_description'].apply(list),
        on = 'day_of_week',
        how = 'left'
        )
    return merge_df

def add_mountain_heights(dataframe, soup_object):
    dataframe['mountain_height_top'] = int(soup_object.findAll('span', class_ ="height")[0].text)
    dataframe['mountain_height_mid'] = int(soup_object.findAll('span', class_ ="height")[1].text)
    dataframe['mountain_height_btm'] = int(soup_object.findAll('span', class_ ="height")[2].text)
    return dataframe

def add_freezing_level(dataframe):
    dataframe['freezing_level_synopsis'] = np.where( dataframe['freezing_level'] > dataframe['mountain_height_top'], 'Above Peak',
                                               np.where( dataframe['freezing_level'] > dataframe['mountain_height_mid'], 'Mid to Peak',
                                                       np.where(dataframe['freezing_level'] > dataframe['mountain_height_btm'], 'Base to Mid',
                                                               'Below Base')))
    return dataframe

def add_localised_date(dataframe, soup_object):
    #Pull the date from the web page
    d = {'date_lcl' :  ''.join(char for char in soup_object.findAll('span', class_ ="location-issued__no-wrap")[3].text if char in printable)}
    df = pd.DataFrame(data=d, index = [0])
    #Create datetime object
    df['date_lcl_formatted'] = pd.to_datetime(df['date_lcl'], format='%d %b%Y')

    #create a dummy dataframe with the next 6 days in dates
    d2 = { 'date_lcl': [0,0,0,0,0], 'date_lcl_formatted' : [] }
    for i in range(1,6):
        df = df.copy()
        d2['date_lcl_formatted'].append(df['date_lcl_formatted'][0]+timedelta(days=i))
    df2 = pd.DataFrame(data=d2)
    
    #Combine the two
    df = pd.concat([df, df2])
    
    #Merge on day_of_week
    df['date_lcl_formatted1'] = df['date_lcl_formatted'].dt.strftime('%d-%m-%Y')
    df['day_of_week'] = df['date_lcl_formatted'].dt.day_name()
    df = df[['day_of_week','date_lcl_formatted']]
    dataframe = pd.merge(dataframe, df, how = 'left', on = 'day_of_week')

    return dataframe

def add_snowfall_synopsis(dataframe):
    dataframe['snowfall_synopsis'] = np.where(dataframe['snowfall']>15,'Shit Tonne',
    np.where((dataframe['snowfall']<=15)&(dataframe['snowfall']>5),'Decent',
    np.where((dataframe['snowfall']<=5)&(dataframe['snowfall']>0),'Trace',
    'Fuck All')))
    return dataframe

