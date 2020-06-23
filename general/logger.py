

import time
import datetime
import sys


try:
    rows, line_length = (int(item) for item in os.popen('stty size', 'r').read().split())
    tab_list = [0.4228, 0.0805, 0.2483, 0.0671, 0.0671, 0.1141]
    tab1, tab2, tab3, tab4, tab5, tab6 = (int(tab * line_length) for tab in tab_list)

except:
    tab1, tab2, tab3, tab4, tab5, tab6 = 63, 12, 37, 10, 10, 17
    line_length = tab1 + tab2 + tab3 + tab4 + tab5 + tab6

col_headings = str      ( 
                        'process or function'.          ljust(tab1) + 
                        'progress'.                     ljust(tab2) + 
                        'source = table or core_df'.    ljust(tab3) + 
                        'rows'.                         ljust(tab4) + 
                        'columns'.                      ljust(tab5) +
                        'load time'.                    ljust(tab6)      
                        )

def print_line_of_dashes(): print('-'*line_length)
def print_line_of_equals(): print('='*line_length)


def log_core_process_start_and_finish(func):
    def log_core_process_start_and_finish_decorator(dict_of_beaches, beach, *args, **kwargs):
        core_process_start_time = time.time()
        log_core_process_header(beach, func.__name__)
        result = func(dict_of_beaches, beach, *args, **kwargs)
        log_core_process_footer(func.__name__, core_process_start_time)
        return result
    return log_core_process_start_and_finish_decorator


def log_core_process_header( beach, core_process ):
    print_line_of_dashes()
    print (core_process, ' - ', beach )
    print( col_headings )
    print_line_of_dashes()

def log_core_process_footer(core_process, start_time):
    current_time = time.time()
    time_difference_seconds = str ( round( ( current_time - start_time ), 3 ) )
    time_difference_seconds = ( '.'.join(map('{0:0>2}'.format, time_difference_seconds.split('.'))) )   
    time_difference_minutes = str ( round( ( ( current_time - start_time ) / 60 ), 3 ) )
    time_difference_minutes = ( '.'.join(map('{0:0>3}'.format, time_difference_minutes.split('.'))) )   
    print_line_of_dashes()
    print       (      
                core_process.                                   ljust( tab1 - 1        ), 
                str( 'COMPLETED' ).                             ljust( tab2 - 1        ), 
                str( 'total load time =').                      ljust( tab3 - 1        ), 
                str(time_difference_seconds + ' seconds' ).     ljust( tab4 + tab5 - 1 ), 
                str(time_difference_minutes + ' minutes' ) 
                )


def log_application_header():
    print ('\n' * 10)  
    print_line_of_equals()
    print ( '\n' )
    print ( 'Surf Crawler Commenced @',  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
    print ( '' )
    print ( 'Python build Verion   = 3.7.4')
    print ( 'Environment Version   =', sys.version )
    print ( 'Python Executable     = ',sys.executable )   
    print ( '' )   
    print_line_of_equals()
    print ( '' )


def log_application_footer(start_time):
    current_time = time.time()
    time_difference_seconds = round( ( ( current_time - start_time )      ), 2 )
    time_difference_minutes = round( ( ( current_time - start_time ) / 60 ), 2 )
    print_line_of_equals()
    print(      'FINISHED PROCESSING @', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '- total load time =', time_difference_seconds, 'seconds  - ', time_difference_minutes, 'minutes' )
    print_line_of_equals()


def log_start_and_finish(func):
    ''' Function needs to input campaign, dictionary_of_dfs, df_name
    then output either dictionary_of_dfs or tuple with dictionary_of_dfs and error message
    '''
    def log_process_start_and_finish(*args, **kwargs):
        try:
            process_start_time = time.time()
            log_process_start(func.__name__)
            result = func(*args, **kwargs)
            if type(result) == tuple:
                result, message = result[0], result[1] if result[1] is not None else 'Completed'
                log_process_end(func.__name__, process_start_time, result=message )
            else:
                log_process_end(func.__name__, process_start_time)

            return result
        except Exception as error: log_process_end(func.__name__, process_start_time, None, error_message=str(error) ); raise error
    return log_process_start_and_finish

def log_process_start( object_name ):
    if len(str( object_name )) > ( 46 ):  
        display_name = str( object_name )[:42] + '...'
    else :
        display_name = str( object_name )
    
    print( display_name.ljust( tab1 ), end ='')


def log_process_end( process_name, process_start_time, result='Completed', error_message=None ):
    current_time = time.time()
    diff = str ( round( ( current_time - process_start_time ), 3 ) )
    time_difference = ( '.'.join(map('{0:0>3}'.format, diff.split('.'))) )

    if error_message is not None:
        result = color_text('-FAILURE-', 'red')
    elif result == 'Unavailable':
        result = color_text(result, 'purple')
    elif result.startswith('n/a'):
        result = color_text(result, 'blue')
    else:
        result = color_text(result, None)

    # else :
    number_of_rows      = str( 'n/a' )
    number_of_columns   = str( 'n/a' )

    print(
            result, 
            process_name.ljust( tab3 - 1 ),  
            number_of_rows.ljust( tab4 - 1 ),  
            number_of_columns.ljust( tab5 - 1 ), 
            'seconds = ' + str ( time_difference ) 
            )
    if error_message is not None:
        print ( error_message )

def color_text(text, color):
    if color == 'red':
        return '\033[31m' + text.ljust( tab2 ) + '\033[0m'
    elif color == 'purple':
        return '\033[31m' + text.ljust( tab2 ) + '\033[0m'
    elif color == 'blue':
        return '\033[35m' + text.ljust( tab2 ) + '\033[0m'
    elif color is None:
        return text.ljust( tab2 )
    else: raise NotImplementedError(f"We do not support color {color}")