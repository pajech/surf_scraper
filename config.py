import pandas as pd

empty_df = pd.DataFrame()

scraper_config = {
    'Torquay':{
        'url'                   :'https://magicseaweed.com/Torquay-Surf-Report/525/',
        'response'              :None,
        'soup_object'           :None,
        'weekly_forecast_dict'  :{},
        'weekly_forecast_list'  :[],
        'summarised_df'         :empty_df
    }
}