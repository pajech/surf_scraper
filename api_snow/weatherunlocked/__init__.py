import requests
import collections


ERROR_RESPONSE = 'error_response'
def get_snow(request_url):
    """Get Weather Unlicked API response."""
    snow_response = requests.get(request_url)
    snow_response.raise_for_status()

    
    json_d = snow_response.json()
    headers = snow_response.headers


    if ERROR_RESPONSE in json_d:
        code = json_d.get(ERROR_RESPONSE).get('code')
        msg = json_d.get(ERROR_RESPONSE).get('error_msg')
        raise Exception('API returned error code {}. {}'.format(code, msg)) 
    if len(json_d) == 1:
        return ForecastDataPoint(json_d[0], headers, snow_response)
    return ForecastDataBlock(json_d['forecast'], json_d['name'], json_d['country'], headers, snow_response)


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def _forecast_transform(f_d):
    """Get attribute dict from flattened forecast dict."""

    date                    = f_d.get('date', None)
    time                    = f_d.get('time', None)
    cloud_pct_low           = f_d.get('lowcloud_pct', None)
    cloud_pct_mid           = f_d.get('midcloud_pct', None)
    cloud_pct_high          = f_d.get('highcloud_pct', None)
    cloud_pct_total         = f_d.get('totalcloud_pct', None)
    freezing_level_ft       = f_d.get('frzglvl_ft', None)
    freezing_level_m        = f_d.get('frzglvl_m', None)
    precip_mm               = f_d.get('precip_mm', None)
    precip_in               = f_d.get('precip_in', None)
    rain_mm                 = f_d.get('rain_mm', None)
    rain_in                 = f_d.get('rain_in', None)
    snow_mm                 = f_d.get('snow_mm', None)
    snow_in                 = f_d.get('snow_in', None)
    humidity_pct            = f_d.get('hum_pct', None)
    dewpoint_c              = f_d.get('dewpoint_c', None)
    dewpoint_f              = f_d.get('dewpoint_f', None)
    visibility_km           = f_d.get('vis_km', None)
    visibility_mi           = f_d.get('vis_mi', None)
    sealevel_pressure_mb    = f_d.get('slp_mb', None)
    sealevel_pressure_in    = f_d.get('slp_in', None)
    base_wx_desc            = f_d.get('base_wx_desc', None)
    base_wx_code            = f_d.get('base_wx_code', None)
    base_wx_icon            = f_d.get('base_wx_icon', None)
    base_freshsnow_cm       = f_d.get('base_freshsnow_cm', None)
    base_freshsnow_in       = f_d.get('base_freshsnow_in', None)
    base_temp_c             = f_d.get('base_temp_c', None)
    base_temp_f             = f_d.get('base_temp_f', None)
    base_feelslike_c        = f_d.get('base_feelslike_c', None)
    base_feelslike_f        = f_d.get('base_feelslike_f', None)
    base_winddir_compass    = f_d.get('base_winddir_compass', None)
    base_windspeed_mph      = f_d.get('base_windspd_mph', None)
    base_windspeed_kmh      = f_d.get('base_windspd_kmh', None)
    base_windspeed_kts      = f_d.get('base_windspd_kts', None)
    base_windspeed_ms       = f_d.get('base_windspd_ms', None)
    base_windgust_mph       = f_d.get('base_windgst_mph', None)
    base_windgust_kmh       = f_d.get('base_windgst_kmh', None)
    base_windgust_kts       = f_d.get('base_windgst_kts', None)
    base_windgust_ms        = f_d.get('base_windgst_ms', None)
    mid_wx_desc             = f_d.get('mid_wx_desc', None)
    mid_wx_code             = f_d.get('mid_wx_code', None)
    mid_wx_icon             = f_d.get('mid_wx_icon', None)
    mid_freshsnow_cm        = f_d.get('mid_freshsnow_cm', None)
    mid_freshsnow_in        = f_d.get('mid_freshsnow_in', None)
    mid_temp_c              = f_d.get('mid_temp_c', None)
    mid_temp_f              = f_d.get('mid_temp_f', None)
    mid_feelslike_c         = f_d.get('mid_feelslike_c', None)
    mid_feelslike_f         = f_d.get('mid_feelslike_f', None)
    mid_winddir_deg         = f_d.get('mid_winddir_deg', None)
    mid_winddir_compass     = f_d.get('mid_winddir_compass', None)
    mid_windspd_mph         = f_d.get('mid_windspd_mph', None)
    mid_windspd_kmh         = f_d.get('mid_windspd_kmh', None)
    mid_windspd_kts         = f_d.get('mid_windspd_kts', None)
    mid_windspd_ms          = f_d.get('mid_windspd_ms', None)
    mid_windgst_mph         = f_d.get('mid_windgst_mph', None)
    mid_windgst_kmh         = f_d.get('mid_windgst_kmh', None)
    mid_windgst_kts         = f_d.get('mid_windgst_kts', None)
    upper_wx_desc           = f_d.get('upper_wx_desc', None)
    upper_wx_code           = f_d.get('upper_wx_code', None)
    upper_wx_icon           = f_d.get('upper_wx_icon', None)
    upper_freshsnow_cm      = f_d.get('upper_freshsnow_cm', None)
    upper_freshsnow_in      = f_d.get('upper_freshsnow_in', None)
    upper_temp_c            = f_d.get('upper_temp_c', None)
    upper_temp_f            = f_d.get('upper_temp_f', None)
    upper_feelslike_c       = f_d.get('upper_feelslike_c', None)
    upper_feelslike_f       = f_d.get('upper_feelslike_f', None)
    upper_winddir_deg       = f_d.get('upper_winddir_deg', None)
    upper_winddir_compass   = f_d.get('upper_winddir_compass', None)
    upper_windspd_mph       = f_d.get('upper_windspd_mph', None)
    upper_windspd_kmh       = f_d.get('upper_windspd_kmh', None)
    upper_windspd_kts       = f_d.get('upper_windspd_kts', None)
    upper_windspd_ms        = f_d.get('upper_windspd_ms', None)
    upper_windgst_mph       = f_d.get('upper_windgst_mph', None)
    upper_windgst_kmh       = f_d.get('upper_windgst_kmh', None)
    upper_windgst_kts       = f_d.get('upper_windgst_kts', None)

    dictionary_f_d =  {
    date                    :'date',
    time                    :'time',
    cloud_pct_low           :'lowcloud_pct',
    cloud_pct_mid           :'midcloud_pct',
    cloud_pct_high          :'highcloud_pct',
    cloud_pct_total         :'totalcloud_pct',
    freezing_level_ft       :'frzglvl_ft',
    freezing_level_m        :'frzglvl_m',
    precip_mm               :'precip_mm',
    precip_in               :'precip_in',
    rain_mm                 :'rain_mm',
    rain_in                 :'rain_in',
    snow_mm                 :'snow_mm',
    snow_in                 :'snow_in',
    humidity_pct            :'hum_pct',
    dewpoint_c              :'dewpoint_c',
    dewpoint_f              :'dewpoint_f',
    visibility_km           :'vis_km',
    visibility_mi           :'vis_mi',
    sealevel_pressure_mb    :'slp_mb',
    sealevel_pressure_in    :'slp_in',
    base_wx_desc            :'base_wx_desc',
    base_wx_code            :'base_wx_code',
    base_wx_icon            :'base_wx_icon',
    base_freshsnow_cm       :'base_freshsnow_cm',
    base_freshsnow_in       :'base_freshsnow_in',
    base_temp_c             :'base_temp_c',
    base_temp_f             :'base_temp_f',
    base_feelslike_c        :'base_feelslike_c',
    base_feelslike_f        :'base_feelslike_f',
    base_winddir_compass    :'base_winddir_compass',
    base_windspeed_mph      :'base_windspd_mph',
    base_windspeed_kmh      :'base_windspd_kmh',
    base_windspeed_kts      :'base_windspd_kts',
    base_windspeed_ms       :'base_windspd_ms',
    base_windgust_mph       :'base_windgst_mph',
    base_windgust_kmh       :'base_windgst_kmh',
    base_windgust_kts       :'base_windgst_kts',
    base_windgust_ms        :'base_windgst_ms',
    mid_wx_desc             :'mid_wx_desc',
    mid_wx_code             :'mid_wx_code',
    mid_wx_icon             :'mid_wx_icon',
    mid_freshsnow_cm        :'mid_freshsnow_cm',
    mid_freshsnow_in        :'mid_freshsnow_in',
    mid_temp_c              :'mid_temp_c',
    mid_temp_f              :'mid_temp_f',
    mid_feelslike_c         :'mid_feelslike_c',
    mid_feelslike_f         :'mid_feelslike_f',
    mid_winddir_deg         :'mid_winddir_deg',
    mid_winddir_compass     :'mid_winddir_compass',
    mid_windspd_mph         :'mid_windspd_mph',
    mid_windspd_kmh         :'mid_windspd_kmh',
    mid_windspd_kts         :'mid_windspd_kts',
    mid_windspd_ms          :'mid_windspd_ms',
    mid_windgst_mph         :'mid_windgst_mph',
    mid_windgst_kmh         :'mid_windgst_kmh',
    mid_windgst_kts         :'mid_windgst_kts',
    upper_wx_desc           :'upper_wx_desc',
    upper_wx_code           :'upper_wx_code',
    upper_wx_icon           :'upper_wx_icon',
    upper_freshsnow_cm      :'upper_freshsnow_cm',
    upper_freshsnow_in      :'upper_freshsnow_in',
    upper_temp_c            :'upper_temp_c',
    upper_temp_f            :'upper_temp_f',
    upper_feelslike_c       :'upper_feelslike_c',
    upper_feelslike_f       :'upper_feelslike_f',
    upper_winddir_deg       :'upper_winddir_deg',
    upper_winddir_compass   :'upper_winddir_compass',
    upper_windspd_mph       :'upper_windspd_mph',
    upper_windspd_kmh       :'upper_windspd_kmh',
    upper_windspd_kts       :'upper_windspd_kts',
    upper_windspd_ms        :'upper_windspd_ms',
    upper_windgst_mph       :'upper_windgst_mph',
    upper_windgst_kmh       :'upper_windgst_kmh',
    upper_windgst_kts       :'upper_windgst_kts' 
    }

    list_of_items = {}
    for key,value in dictionary_f_d.items():

        list_of_items[value] = "{}".format(key)
    
    return list_of_items
#TODO: Fix up that dictionary

class ForecastDataBlock():

    def __init__(self, d=None, name=None, country=None, headers=None, response=None):
        d = d or {}
        self.resort_name = name
        self.resort_country = country
        self.headers = headers
        self.response = response
        self.data = [ForecastDataPoint(datapoint)
                     for datapoint in d]
        self.summary = self._summary(self.data)

    def _summary(self, d):
        try:
            num = len(d)
            start = d[0].attrs['date']
            end = d[-1].attrs['date']
            return "{} forecasts from {} to {} for {} in {}".format(num, start, end, self.resort_name, self.resort_country)
        except:
            return "No forecasts."

class ForecastDataPoint():
    def __init__(self, d={}, headers=None, response=None):
        self.d = d
        self.f_d = flatten(d)
        self.attrs = _forecast_transform(self.f_d)
        self.headers = headers
        self.response = response
        self.summary = self._summary(d)

    def _summary(self, d):
        try:
            snow_mm = self.attrs['snow_mm']
            base_temp = self.attrs['base_temp_c']
            upper_wind_speed = self.attrs['upper_windspd_kmh']
            return "Snowfal: {} - Base Temp: {} - Peak Wind Spedk {}".format(snow_mm, base_temp,upper_wind_speed)
        except:
            return None

    def __getattr__(self, name):
        try:
            return self.f_d[name]
        except:
            return PropertyUnavailable("Property {} is unavailable for this forecast".format(name))
