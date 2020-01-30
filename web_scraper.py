import requests
import urllib.request
import time
from bs4 import BeautifulSoup


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

from config import scraper_config
scraper_config['Torquay']['response']               = extract_url(scraper_config['Torquay']['url'])
scraper_config['Torquay']['soup_object']            = extract_html(scraper_config['Torquay']['response'])
scraper_config['Torquay']['weekly_forecast_dict']   = build_forecast_dict(scraper_config['Torquay']['soup_object'])


print(scraper_config['Torquay']['soup_object'])

# To Do List:
# - Currently just Torquay but would like to expand it to other surf locations
