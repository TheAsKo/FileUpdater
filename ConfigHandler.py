# Config File - Default Create + Reading + Writing
# V2.0
###############################################
# Changelog
# V1.0 - Initial commit
# V1.1 - Fixing error message handling of values
# V1.2 - Added some help texts
# V1.3 - Renaming of defs
# V1.4 - Adding support of reading multiple files
# V1.4.1 - Fixed writing in different files
# V1.4.2 - Fixed writing bug
# V2.0 - Full code cleanup/rewrite , better error handling , writing no longer uses anything other than str to write to .ini
###############################################
# Imports
import configparser
import logging
import json
import os
from typing import Union
###############################################
# Declarations
config=configparser.ConfigParser()
#configparser.BasicInterpolation() #NOT WORKING NEED TO FIX FOR ADDING %
logging.getLogger().setLevel(logging.DEBUG) #I THINK CUSTOM LOG NAME DONT WORK HERE TOO EVEN IT IS IN SEPARATE DEFS
###############################################
def DefaultConfigWrite(file='config.ini'):
    config=configparser.ConfigParser()
    config['APP'] = {'Logging' : '10',
                     'HelpKeys' : 'logging.DEBUG = 10 , logging.INFO = 20 , logging.WARNING = 30 , logging.CRITICAL = 50',
                     'Debug' : 'False',
                     'errorlogging' : 'False'}
    config['FILE'] = {'TargetFile' : 'Zoznam.xlsx',
                      'targetfilepath' : r'C:\Users\mobil\Desktop\VSCode-FileUpdater\Zoznam.xlsx'}
    config['GITHUB'] = {'Token' : ''}

    with open(file, 'w') as configfile:
        config.write(configfile)
    pass

def Read(value1: str, value2: str, ValType: Union[str,int,dict,list,float,bool] = str, file: str = 'config.ini'):
    """Read value from config file.

    Args:
        Value1 (str): Config Value Category.
        Value2 (str): Config Value Name.
        ValType (Union[str,int,dict,list,float,bool]): Config Value Type, available options are dict, list, int, float, bool, str; defaults to None.
        file (str): Config File to read, default is config.ini.

    Returns:
        The requested config value.

    """
    config = configparser.ConfigParser()
    log = logging.getLogger('ConfigRead')

    try:
        if os.path.isfile(file):
            config.read(file)
            ValueX = config[value1]
            match ValType:
                case 'dict' | 'list':
                    try:
                        return json.loads(ValueX[value2])
                    except:
                        log.warning(f"Requested value {value2} failed to load as dictionary/list from {file}!")
                case 'int':
                    try:
                        return ValueX.getint(value2)
                    except:
                        log.warning(f"Requested value {value2} is not an integer from {file}!")
                case 'float':
                    try:
                        return ValueX.getfloat(value2)
                    except:
                        log.warning(f"Requested value {value2} is not a float from {file}!")
                case 'bool':
                    try:
                        return ValueX.getboolean(value2)
                    except:
                        log.warning(f"Requested value {value2} is not a boolean from {file}!")
                case 'str' | _ : 
                    try:
                        return ValueX[value2]
                    except:
                        log.warning(f"Requested value {value2} failed to load from {file}!")
        else:
            #raise FileNotFoundError(f"Config file not found: {file}")
            log.warning(f"Config file not found: {file}")
            log.info("Generating default config...")
            DefaultConfigWrite(file)
            return Read(value1, value2, ValType, file)  # Retry after generating default config

    except Exception as e:
        log.error(f"An unexpected error occurred: {str(e)}")

def Write(data1: str, data2: str, value: str, file: str = 'config.ini'):
    """Write value into config file.

    Args:
        data1 (str): Config Value Category.
        data2 (str): Config Value Name.
        value (str): Value that will be written into.
        file (str): Config File to read, default is config.ini.

    """
    config = configparser.ConfigParser()
    log = logging.getLogger('ConfigWrite')

    try:
        if os.path.isfile(file):
            config.read(file)
            try:
                config[data1][data2] = str(value)
            except Exception as e:
                log.warning(f'Updating value of {data2} failed: {e}')
            else:
                log.debug(f'Edited value of {data2} to: {value}')

            with open(file, 'w') as configfile:
                config.write(configfile)
        else:
            raise FileNotFoundError(f"Config file not found: {file}")
    except Exception as e:
        log.error(f"An unexpected error occurred: {str(e)}")
        
        
if __name__ == '__main__': #USED FOR MY EASE OF GENERATING CONFIG FILE
    DefaultConfigWrite()
    logging.debug('Success')