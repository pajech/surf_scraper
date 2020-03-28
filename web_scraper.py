import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
import ezgmail
import os


# Helper Functions
def extract_url(url):
    response = requests.get(url)
    return response

def extract_html(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def build_forecast_dict(soup_object):
    weekly_forecast_dict = {}
    for i in range (1,8):
        daily_table = soup_object.findAll('tr',{'data-forecast-day':str(i)})
        weekly_forecast_dict[i] = daily_table
    
    return weekly_forecast_dict

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
            
            #Append the hourly data to the day forecast
            day_forecast_list.append(hour_forcast)
        
        #Append the day data to the weekly forecast
        weekly_forecast_list.append(day_forecast_list)
    
    return weekly_forecast_list

def build_forecast_df(forecast_list):
    # ============================================================================= Convert List into a Dataframe
    columns = ['daydate','time', 'size', 'primary_swell','swell_period','wind_speed1','wind_speed2','wind_metrics', 'temperature','probability']
    weekly_dataframe = pd.DataFrame(columns=columns)
    for i in range (7):
        df = pd.DataFrame(forecast_list[i], columns = columns)
        #print(df)
        weekly_dataframe = weekly_dataframe.append(df)
    
    return weekly_dataframe

def add_wind_metrics(dataframe):
    #Check to see if winds exist here
    dataframe['wind'] = dataframe['wind_speed1'] +'-'+ dataframe['wind_speed2'] + ' '+ dataframe['wind_metrics'] 
    return dataframe

def add_day_date(dataframe):
    # Add Try and Logging
    day_date_split = dataframe["daydate"].str.split("(\d\d\d\d)", n = 1, expand = True) 
    dataframe['day_of_week'] = day_date_split[0]
    dataframe['date'] = day_date_split[1]
    return dataframe

def add_size_of_wave(dataframe):
    dataframe['size_of_wave'] = dataframe['primary_swell'].str.split("ft", n=1, expand = True)[0]
    dataframe['size_of_wave'] = dataframe['size_of_wave'].astype('float')
    return dataframe

def add_wind_speed(dataframe):
    dataframe['wind_speed1'] = dataframe['wind_speed1'].astype('int')
    dataframe['wind_speed2'] = dataframe['wind_speed2'].astype('int')
    return dataframe

def add_swell_period(dataframe):
    dataframe['swell_period_int'] = dataframe['swell_period'].str.split("s", n=1, expand = True)[0]
    dataframe['swell_period_int'] = dataframe['swell_period_int'].astype('int')
    return dataframe

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

def add_total_rating(dataframe):
    dataframe['total_rating'] = dataframe['wind_rating'] + dataframe['swellperiod_rating'] + dataframe['heigh_rating']
    return dataframe

def filter_to_high_rating(dataframe):
    dataframe = dataframe[dataframe['total_rating']>15]
    return dataframe

def add_day_of_week(dataframe):
    dataframe['day_of_week'] = dataframe['daydate'].str.split(r'[0-9]', expand=True)
    return dataframe

def filter_to_relevant_cols(dataframe):
    dataframe = dataframe[['daydate','time','size','swell_period','wind','total_rating','day_of_week']]
    return dataframe

def build_email_body(dataframe):
    str_email_start = 'Hey Roost, the best times for a shred this week are: \n \n'
    str_email_middle = ''
    for i in range(5):
        str_interim = """{Weekday} at {Time}. \n This is the height: {Height}, the period: {Period} and the wind: {Wind}. 
        It scored an overall rating of {Rating}/30 \n \n""".format(Weekday = dataframe['day_of_week'].iloc[i],
                                                        Time = dataframe['time'].iloc[i],
                                                        Height = dataframe['size'].iloc[i],
                                                        Period = dataframe['swell_period'].iloc[i],
                                                        Wind = dataframe['wind'].iloc[i],
                                                        Rating = dataframe['total_rating'].iloc[i]                                                   
                                                        )
        str_email_middle = str_email_middle + str_interim



    dataframe_weekend = dataframe[dataframe['day_of_week'].isin(['Saturday', 'Sunday'])]

    if len(dataframe_weekend) > 0:
        str_weekend = '\n If you are relegated to the weekend like the corporate drone that you are, you\'re best bests are: \n \n'
        for i in range(len(dataframe_weekend)):
            str_interim = """{Weekday} at {Time}. \n This is the height: {Height}, the period: {Period} and the wind: {Wind}. 
        It scored an overall rating of {Rating}/30 \n \n""".format(Weekday = dataframe_weekend['day_of_week'].iloc[i],
                                                        Time = dataframe_weekend['time'].iloc[i],
                                                        Height = dataframe_weekend['size'].iloc[i],
                                                        Period = dataframe_weekend['swell_period'].iloc[i],
                                                        Wind = dataframe_weekend['wind'].iloc[i],
                                                        Rating = dataframe_weekend['total_rating'].iloc[i]                                                   
                                                        )
        str_weekend = str_weekend + str_interim
    else:
        str_weekend = ''
            

    str_email_end = ' Happy Shredding. \n'
        


    str_email_all = str_email_start + str_email_middle + str_weekend + str_email_end
    return str_email_all


def sort_by_high_rating(dataframe):
    dataframe = dataframe.sort_values(by='total_rating', ascending = False)
    return dataframe

    
def filter_out_nocturnal_times(dataframe):
    dataframe = dataframe[dataframe['time'].isin(['6am','9am','Noon','3pm'])]
    return dataframe



from config import scraper_config
scraper_config['Torquay']['response']               = extract_url(scraper_config['Torquay']['url'])
scraper_config['Torquay']['soup_object']            = extract_html(scraper_config['Torquay']['response'])
scraper_config['Torquay']['weekly_forecast_dict']   = build_forecast_dict(scraper_config['Torquay']['soup_object'])
scraper_config['Torquay']['weekly_forecast_list']   = build_forecast_list(scraper_config['Torquay']['weekly_forecast_dict'])
scraper_config['Torquay']['weekly_dataframe']       = build_forecast_df(scraper_config['Torquay']['weekly_forecast_list'])
scraper_config['Torquay']['weekly_dataframe']       = add_wind_metrics(scraper_config['Torquay']['weekly_dataframe'])
scraper_config['Torquay']['weekly_dataframe']       = add_day_date(scraper_config['Torquay']['weekly_dataframe'])
scraper_config['Torquay']['weekly_dataframe']       = add_size_of_wave(scraper_config['Torquay']['weekly_dataframe'])
scraper_config['Torquay']['weekly_dataframe']       = add_wind_speed(scraper_config['Torquay']['weekly_dataframe'])
scraper_config['Torquay']['weekly_dataframe']       = add_swell_period(scraper_config['Torquay']['weekly_dataframe'])
scraper_config['Torquay']['weekly_dataframe']       = add_swell_height_rating(scraper_config['Torquay']['weekly_dataframe'])
scraper_config['Torquay']['weekly_dataframe']       = add_swell_period_rating(scraper_config['Torquay']['weekly_dataframe'])
scraper_config['Torquay']['weekly_dataframe']       = add_wind_rating(scraper_config['Torquay']['weekly_dataframe'])
scraper_config['Torquay']['weekly_dataframe']       = add_day_of_week(scraper_config['Torquay']['weekly_dataframe'])
scraper_config['Torquay']['weekly_dataframe']       = add_total_rating(scraper_config['Torquay']['weekly_dataframe'])
scraper_config['Torquay']['weekly_dataframe']       = filter_to_high_rating(scraper_config['Torquay']['weekly_dataframe'])
scraper_config['Torquay']['weekly_dataframe']       = filter_to_relevant_cols(scraper_config['Torquay']['weekly_dataframe'])
scraper_config['Torquay']['weekly_dataframe']       = filter_out_nocturnal_times(scraper_config['Torquay']['weekly_dataframe'])
scraper_config['Torquay']['weekly_dataframe'].to_csv('TorquaySurfReport.csv', index = False)
scraper_config['Torquay']['weekly_dataframe']       = sort_by_high_rating(scraper_config['Torquay']['weekly_dataframe'])




print(scraper_config['Torquay']['weekly_dataframe'].columns.values)
print(scraper_config['Torquay']['weekly_dataframe'].head())
print(scraper_config['Torquay']['weekly_dataframe'].total_rating.min())


ezgmail.init()

email_body = build_email_body(scraper_config['Torquay']['weekly_dataframe'])
print(email_body)

# The best times to go this week are:

# If you are stuck to weekend vibes, here is your best bet

ezgmail.send('paulychynoweth@gmail.com', 'Yo Bra', email_body, ['TorquaySurfReport.csv'])

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
