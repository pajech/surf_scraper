import requests
from general.dataframe_builder import sort_by_high_rating

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


def send_sms(token, to, body):
    payload = dict(to=to, body=body)
    response = telstra_request("messages/sms", payload, token=token)

    if response.status_code != 201:
        raise RuntimeError("Bad response from Telstra API! " + response.text)

    response_json = response.json()
    return response_json


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