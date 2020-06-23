import os

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# Local Folders
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
application_folder = os.path.normpath(os.getcwd() + os.sep + os.pardir)
# application_folder                      = os.path.dirname( os.path.realpath( __file__) ) 
local_folder_table_dumps                = 'general/beach_files'
if not os.path.isdir(application_folder + '/'+local_folder_table_dumps): os.makedirs(application_folder + '/'+local_folder_table_dumps)

def export_local( dataframe, beach, surf_or_snow = 'Surf' ):
    dataframe_dict = dataframe.dtypes.to_frame('dtypes').reset_index()
    dataframe_dict.to_csv(application_folder + '/' + local_folder_table_dumps + '/' + beach+'Dict.csv', index = False)
    dataframe.to_csv(application_folder + '/' + local_folder_table_dumps +'/' + beach+'{surf_snow}Report.csv'.format(surf_snow = surf_or_snow), index = False)