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

email_body = {}

class EmailSubscriber:
    def __init__(self, name, surname, email, beach_preferences):
        self.name               = name
        self.surnamme           = surname
        self.email              = email
        self.beach_preferences  = beach_preferences

Paul = EmailSubscriber(
    "Pauly",
    "C",
    "paulychynoweth@gmail.com",
    ['All']
)

Choy = EmailSubscriber(
    "Cho'y",
    "Richardson",
    "emmett.richardson@hotmail.com",
    ["All"]
)

Rob = EmailSubscriber(
    "Robby",
    "Hay",
    "rob@blueswoop.com",
    ["Scamander","ShipsternBluff "]
)

list_of_subscribers = [Paul, Rob]