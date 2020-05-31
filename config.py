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
    },
    'Bells':{
        'url'                   :'https://magicseaweed.com/Bells-Beach-Surf-Report/524/',
        'response'              :None,
        'soup_object'           :None,
        'weekly_forecast_dict'  :{},
        'weekly_forecast_list'  :[]
    },
    'Scamander':{
        'url'                   :'https://magicseaweed.com/Scamander-Surf-Report/734/',
        'response'              :None,
        'soup_object'           :None,
        'weekly_forecast_dict'  :{},
        'weekly_forecast_list'  :[]
    },
    'ShipsternBluff':{
        'url'                   :'https://magicseaweed.com/Shipstern-Bluff-Surf-Report/537/',
        'response'              :None,
        'soup_object'           :None,
        'weekly_forecast_dict'  :{},
        'weekly_forecast_list'  :[]
    }

}

scraper_config_snow = {
    'Whistler':{
        'url'                   :'https://www.snow-forecast.com/resorts/Whistler-Blackcomb/6day/mid',
        'response'              :None,
        'soup_object'           :None,
        'weekly_forecast_dict'  :{},
        'weekly_forecast_list'  :[]
    },

    'Thredbo':{
        'url'                   :'https://www.snow-forecast.com/resorts/Thredbo/6day/mid',
        'response'              :None,
        'soup_object'           :None,
        'weekly_forecast_dict'  :{},
        'weekly_forecast_list'  :[]
    },

}

email_body = {}
email_body_snow = {}

class EmailSubscriber:
    def __init__(self, name, surname, email, beach_preferences, snow_preferences):
        self.name               = name
        self.surnamme           = surname
        self.email              = email
        self.beach_preferences  = beach_preferences
        self.snow_preferences   = snow_preferences

Paul = EmailSubscriber(
    "Pauly",
    "C",
    "paulychynoweth@gmail.com",
    ['All'],
    ['Thredbo', 'Whistler']
)

Choy = EmailSubscriber(
    "Cho'y",
    "Richardson",
    "emmett.richardson@hotmail.com",
    ["All"],
    ['Thredbo']
)

Ben = EmailSubscriber(
    "Benny",
    "Carter",
    "cartbg@gmail.com",
    ["All"],
    ['Thredbo']
)

Rob = EmailSubscriber(
    "Robby",
    "Hay",
    "rob@blueswoop.com",
    ["Scamander","ShipsternBluff "],
    ['Thredbo']
)

list_of_subscribers = [
    Paul, 
    # Rob, 
    # Choy,
    # Ben
    ]