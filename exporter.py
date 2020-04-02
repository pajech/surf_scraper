import os

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# Local Folders
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
application_folder                      = os.path.dirname( os.path.realpath( __file__) ) 
local_folder_table_dumps                = 'beach_files'
if not os.path.isdir(local_folder_table_dumps): os.makedirs(local_folder_table_dumps)

def export_local( dataframe, beach ):
    dataframe_dict = dataframe.dtypes.to_frame('dtypes').reset_index()
    dataframe_dict.to_csv(application_folder + '/' + local_folder_table_dumps + '/' + beach+'Dict.csv', index = False)
    dataframe.to_csv(application_folder + '/' + local_folder_table_dumps + '/' + beach+'SurfReport.csv', index = False)