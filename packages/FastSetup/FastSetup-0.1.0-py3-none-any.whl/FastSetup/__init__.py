
import logging
import datetime
import pandas


def main_log(log_folder):
    
    
        # create a log file with today's date and define its format and set the level to DEBUG
    logging.basicConfig(filename=log_folder + datetime.datetime.now().strftime( '%d-%m-%Y.log' ),
                        filemode='a',
                        format='Line: %(lineno)d - Time: %(asctime)s - Position: %(name)s - Status: %(levelname)s - Message: %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    
    # create the main log names 
    loggerMain = logging.getLogger( '__main__' )
    loggerInit = logging.getLogger( '__Init__' )
    loggerProcess = logging.getLogger( '__Process__' )
    
    
    return loggerMain, loggerInit, loggerProcess
    
    
    
    
def custom_log(log_folder, log_format, log_name):
    
    
    # if the log_foramt string empty the format will be set to default 
    if log_format == '':
        log_format = 'Line: %(lineno)d - Time: %(asctime)s - Position: %(name)s - Status: %(levelname)s - Message: %(message)s'
        
        
    # create a log file with today's date and name of your log and define its format as specified and set the level to DEBUG
    logging.basicConfig(filename=log_folder + '__'+log_name+'__' +datetime.datetime.now().strftime( '%d-%m-%Y.log' ),
                        filemode='a',
                        format=log_format,
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
 
    
    #create the main log name
    customLog = logging.getLogger('__'+log_name+'__')
    
    return customLog


def get_config(Config_Path, SheetName, Key, Value):
    
    # Read the config file with sheet name and making sure all keys and values are string type
    df = pandas.read_excel(Config_Path,sheet_name = SheetName)
    df[Key] = df[Key].astype(str)+1
    df[Value] = df[Value].astype(str)
    
    #iterate through the config dataframe and initialize every Key with its value  
    for index,row in df.iterrows():
        Config = df.set_index(Key)[Value].to_dict()
            
        return Config
    