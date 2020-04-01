import ezgmail


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



    dataframe_weekend = dataframe[dataframe['day_of_week'].isin(['Saturday', 'Sunday'])]

    if len(dataframe_weekend) > 0:
        str_weekend = '\n If you are relegated to the weekend like the corporate drone that you are, you\'re best bests are: \n \n'
        for i in range(len(dataframe_weekend)):
            str_interim = """{Weekday} {Time} at {Beach}. \n This is the height: {Height}, the period: {Period} and the wind: {Wind} (it is {Synopsis}). 
        It scored an overall rating of {Rating}/30 \n \n""".format(
                                                        Weekday     = dataframe_weekend['day_of_week'].iloc[i],
                                                        Time        = dataframe_weekend['time'].iloc[i],
                                                        Height      = dataframe_weekend['size'].iloc[i],
                                                        Period      = dataframe_weekend['swell_period'].iloc[i],
                                                        Wind        = dataframe_weekend['wind'].iloc[i],
                                                        Rating      = dataframe_weekend['total_rating'].iloc[i],
                                                        Beach       = dataframe_weekend['beach'].iloc[i],
                                                        Synopsis    = dataframe_weekend['wind_synopsis'].iloc[i]                                               
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