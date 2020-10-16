import requests
from general.dataframe_builder import sort_by_high_rating
from general.config import sms_key, sms_secret, bnum_list

def telstra_request(endpoint, body=None, headers=None, *, token=None, method='POST'):
    send_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    if token:  # if this is an authenticated request, add the token header
        send_headers['Authorization'] = 'Bearer ' + token
    if headers:  # add any extra headers if desired
        send_headers.update(headers)

    url = "https://tapi.telstra.com/v2/" + endpoint
    return requests.request(method, url, json=body, headers=send_headers)

def auth(app_key, app_secret):
    body = dict(client_id=app_key, client_secret=app_secret,
        grant_type="client_credentials", scope="NSMS")
    response = requests.post("https://tapi.telstra.com/v2/oauth/token", body)

    if response.status_code != 200:
        raise RuntimeError("Bad response from Telstra API! " + response.text)

    response_json = response.json()
    return response_json['access_token']

def create_subscription(token):
    response = telstra_request("messages/provisioning/subscriptions", {}, token=token)

    if response.status_code != 201:
        raise RuntimeError("Bad response from Telstra API! " + response.text)

    response_json = response.json()
    return response_json['destinationAddress']

def create_bnum(token):
    bnumbers = dict(bnum=bnum_list)
    response = telstra_request("messages/freetrial/bnum",bnumbers, token=token)
    response_json = response.json()


def send_sms(token, to, body):
    payload = dict(to=to, body=body)
    response = telstra_request("messages/sms", payload, token=token)

    if response.status_code != 201:
        raise RuntimeError("Bad response from Telstra API! " + response.text)

    response_json = response.json()
    return response_json


token = auth(sms_key, sms_secret)

def build_sms_body(dataframe, contact_name):
    str_sms_start = '{Name}, the best times for a shred this week are:\n\n'.format(Name = contact_name)
    str_sms_middle = ''
    for i in range(5):
        j = i + 1
        str_interim = """{Number}. {Weekday} {Time} at {Beach}.  It's {Height} with an overall rating of {Rating}/30 \n""".format(
                                                        Number      = j,
                                                        Weekday     = dataframe['day_of_week'].iloc[i],
                                                        Time        = dataframe['time'].iloc[i],
                                                        Height      = dataframe['size'].iloc[i],
                                                        Rating      = dataframe['total_rating'].iloc[i],
                                                        Beach       = dataframe['beach'].iloc[i],                                                                                      
                                                        )
        str_sms_middle = str_sms_middle + str_interim



    dataframe_weekend = dataframe[dataframe['day_of_week'].isin(['Saturday', 'Sunday'])].copy()
    dataframe_weekend = sort_by_high_rating(dataframe_weekend)

    print(dataframe_weekend)
    print(dataframe_weekend['beach'].iloc[0])

    if len(dataframe_weekend) > 0:
        str_weekend = '\n And the best this weekend is: \n \n'
        str_interim = """{Weekday} {Time} at {Beach}. It's {Height} with an overall rating of {Rating}/30 \n""".format(
                                                            Weekday     = dataframe_weekend['day_of_week'].iloc[0],
                                                            Time        = dataframe_weekend['time'].iloc[0],
                                                            Height      = dataframe_weekend['size'].iloc[0],
                                                            Rating      = dataframe_weekend['total_rating'].iloc[0], 
                                                            Beach       = dataframe_weekend['beach'].iloc[0],                                            
                                                            )
        str_weekend = str_weekend + str_interim
    else:
        str_weekend = ''
            

    str_sms_end = ' Happy Shredding. \n'
        


    str_sms_all = str_sms_start + str_sms_middle + str_weekend + str_sms_end
    print(str_sms_all)
    return str_sms_all



def build_sms_body_snow(key,dataframe, contact_name, snow_depth_dict):
    sms_start='{Name}, this is a snow update for {Resort} ski resort(s). The snow depth is {Top}cm at the top, {Bottom}cm at base. The most recent snowfall ({Recent}cm) was on {SnowDate} \n\n\n'.format(Name=contact_name,
                                                                                    Top = snow_depth_dict[1],
                                                                                    Bottom = snow_depth_dict[2],
                                                                                    Recent = snow_depth_dict[3],
                                                                                    SnowDate = snow_depth_dict[4],
                                                                                    Resort = key)
    
    dataframe_snow = dataframe[dataframe['snowfall']>0].copy()

    if len(dataframe_snow) > 0:
        sms_middle = 'There is some snowfall this week!!'
        for i in range(len(dataframe_snow)):
            sms_middle = sms_middle + ' On {day_of_week}, it\'s a balmy {temp} degrees and it\'s snowing a {snow_synopsis} amount. There is {snowfall_cm}cm in snow and {rain_ml}ml in rain. The wind is at {wind_speed}km/h and the freezing level is {freezing_level_synopsis}. \n\n'.format(
                day_of_week = dataframe_snow['day_of_week'].iloc[i],
                temp = dataframe_snow['temp'].iloc[i],
                snow_synopsis = dataframe_snow['snowfall_synopsis'].iloc[i],
                snowfall_cm = dataframe_snow['snowfall'].iloc[i],
                rain_ml = dataframe_snow['rain'].iloc[i],
                wind_speed = dataframe_snow['wind'].iloc[i],
                freezing_level_synopsis = dataframe_snow['freezing_level_synopsis'].iloc[i],
            )
        
        sms_end = '\n\n\n Happy Shredding mate!'

    
        str_sms_all = sms_start + sms_middle + sms_end

        print(str_sms_all)

        return str_sms_all

    else:
        return None