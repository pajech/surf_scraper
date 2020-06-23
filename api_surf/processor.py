from general.config import api_key
from api_surf.magicseaweed import MSW_Forecast

def run_beach_process_api(dict_of_beaches, beach):
    if beach == 'Torquay':
        print(beach)
        print(api_key)
        print(dict_of_beaches[beach]['spot_id'])
        dict_of_beaches[beach]['forecast'] = MSW_Forecast(api_key, dict_of_beaches[beach]['spot_id'], unit = 'uk')
        dict_of_beaches[beach]['forecast_future'] = dict_of_beaches[beach]['forecast'].get_future()
        for i, forecast in enumerate(dict_of_beaches[beach]['forecast_future'].data):
            if i == 0:
                print(forecast.attrs)