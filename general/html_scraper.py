import requests
import urllib.request
from bs4 import BeautifulSoup

# Add in decorator class
def extract_url(url):
    # Add in logging & 
    response = requests.get(url)
    return response

def extract_html(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


