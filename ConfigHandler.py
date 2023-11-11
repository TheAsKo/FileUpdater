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
                     'Debug' : 'False'}
    config['FILE'] = {'TargetFile' : 'Zoznam.xlsx'}
    config['GITHUB'] = {'Token' : ''}
    #config['MAIN'] = {'OnlyRootDebug':'True',
    #                'tess_cmd':'C:/Users/nsz.fu.montaz/AppData/Local/Tesseract-OCR/tesseract.exe',
    #                'tessdefault_config':'--psm 7 --oem 3',
    #                'tessnumber_config':'--psm 3 --oem 3 -c tessedit_char_whitelist=0123456789 tessedit_char_blacklist ,._/',
    #                'tessadvnumber_config':'--psm 3 --oem 3 -c tessedit_char_whitelist=0123456789., tessedit_char_blacklist _/',
    #                'DeleteImagesAfterUsage':'True',
    #                'LoggerLevel':'DEBUG',
    #                'TimeDEBUG':'True'}
    #config['MAIN']['URLList'] = '["https://wf-nsm.neuman.at/clients/wf-login/#/","http://wf-nsm.neuman.at/clients/wf-mes/sk/#/wfmes/view/(mainview:msc/349)","http://wf-nsm.neuman.at/clients/wf-mes/sk/#/wfmes/view/(mainview:msc/346)"]'
    #config['MAIN']['SheetDict'] = '{"TimeFlag":["A2","1"],"TimeSend":["B2","1"],"OEE":["C2","1"],"OK":["D2","1"],"NOK":["E2","1"],"Product":["F2","1"],"Scrap":["G2","1"],"Norm":["H2","1"]}'
    #config['MAIN']['LoadCheck'] = '{"LoadCheck":[0,980,180,40],"ScrapLoadCheck":[1820,230,70,70]}'
    #config['TIMECODE']['ThreadDict'] = '{"MachineName":["FILL","PETIG2"],"MachineURL":[1,2],"ShiftCheck":[8,12],"MachineActive":[1,1]}'

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
            raise FileNotFoundError(f"Config file not found: {file}")
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
