

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