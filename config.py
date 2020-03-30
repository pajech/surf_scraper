import pandas as pd

empty_df = pd.DataFrame()

scraper_config = {
    'Torquay':{
        'url'                   :'https://magicseaweed.com/Torquay-Surf-Report/525/',
        'response'              :None,
        'soup_object'           :None,
        'weekly_forecast_dict'  :{},
        'weekly_forecast_list'  :[]
    },
    'JanJuc':{
        'url'                   :'https://magicseaweed.com/Jan-Juc-Surf-Report/1066/',
        'response'              :None,
        'soup_object'           :None,
        'weekly_forecast_dict'  :{},
        'weekly_forecast_list'  :[]
    }
}

email_body = {}