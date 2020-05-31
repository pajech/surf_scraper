import ezgmail
from dataframe_builder import sort_by_high_rating


def build_email_body(dataframe, contact_name):
    str_email_start = 'Hey {Name}, the best times for a shred this week are: \n \n'.format(Name = contact_name)
    str_email_middle = ''
    for i in range(5):
        j = i + 1
        str_interim = """{Number}. {Weekday} {Time} at {Beach}. \n This is the height: {Height}, the period: {Period} and the wind: {Wind} (it is {Synopsis}). 
        It scored an overall rating of {Rating}/30 \n \n""".format(
                                                        Number      = j,
                                                        Weekday     = dataframe['day_of_week'].iloc[i],
                                                        Time        = dataframe['time'].iloc[i],
                                                        Height      = dataframe['size'].iloc[i],
                                                        Period      = dataframe['swell_period'].iloc[i],
                                                        Wind        = dataframe['wind'].iloc[i],
                                                        Rating      = dataframe['total_rating'].iloc[i],
                                                        Beach       = dataframe['beach'].iloc[i],
                                                        Synopsis    = dataframe['wind_synopsis'].iloc[i]                                                                                         
                                                        )
        str_email_middle = str_email_middle + str_interim



    dataframe_weekend = dataframe[dataframe['day_of_week'].isin(['Saturday', 'Sunday'])].copy()
    dataframe_weekend = sort_by_high_rating(dataframe_weekend)

    print(dataframe_weekend)

    if len(dataframe_weekend) > 0:
        str_weekend = '\n If you are relegated to the weekend like the corporate drone that you are, your best bets are: \n \n'
        str_interim = """{Weekday} {Time} at {Beach}. \n This is the height: {Height}, the period: {Period} and the wind: {Wind} (it is {Synopsis}). 
            It scored an overall rating of {Rating}/30 \n \n""".format(
                                                            Weekday     = dataframe_weekend['day_of_week'].iloc[0],
                                                            Time        = dataframe_weekend['time'].iloc[0],
                                                            Height      = dataframe_weekend['size'].iloc[0],
                                                            Period      = dataframe_weekend['swell_period'].iloc[0],
                                                            Wind        = dataframe_weekend['wind'].iloc[0],
                                                            Rating      = dataframe_weekend['total_rating'].iloc[0],
                                                            Beach       = dataframe_weekend['beach'].iloc[0],
                                                            Synopsis    = dataframe_weekend['wind_synopsis'].iloc[0]                                               
                                                            )
        str_weekend = str_weekend + str_interim
    else:
        str_weekend = ''
            

    str_email_end = ' Happy Shredding. \n'
        


    str_email_all = str_email_start + str_email_middle + str_weekend + str_email_end
    print(str_email_all)
    return str_email_all


def initialise_email():
    ezgmail.init()


def build_email_body_snow(key,dataframe, contact_name):
    email_start='Hey {Name}, attached is this weeks snow report for {Resort} ski resort(s). \n\n\n'.format(Name=contact_name,
                                                                                    Resort = key)
    
    dataframe_snow = dataframe[dataframe['snowfall']>0].copy()

    if len(dataframe_snow) > 0:
        email_middle = 'There is some snowfall this week!!'
        for i in range(len(dataframe_snow)):
            email_middle = email_middle + ' On {day_of_week}, it\'s a balmy {temp} degrees and it\'s snowing a {snow_synopsis} amount. There is {snowfall_cm}cm in snow and {rain_ml}ml in rain. The wind is at {wind_speed}km/h and the freezing level is {freezing_level_synopsis}. \n\n'.format(
                day_of_week = dataframe_snow['day_of_week'].iloc[i],
                temp = dataframe_snow['temp'].iloc[i],
                snow_synopsis = dataframe_snow['snowfall_synopsis'].iloc[i],
                snowfall_cm = dataframe_snow['snowfall'].iloc[i],
                rain_ml = dataframe_snow['rain'].iloc[i],
                wind_speed = dataframe_snow['wind'].iloc[i],
                freezing_level_synopsis = dataframe_snow['freezing_level_synopsis'].iloc[i],
            )
        
        email_end = '\n\n\n Happy Shredding mate!'
    
    else:
        email_middle = 'There is fuck all snow this week. '
        email_end = 'Don\'t bother, go surfing instead. \n'
    
    str_email_all = email_start + email_middle + email_end

    print(str_email_all)

    return str_email_all