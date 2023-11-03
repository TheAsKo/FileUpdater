# Config File - Default Create + Reading + Writing
# V1.4.1
###############################################
# Changelog
# V1.0 - Initial commit
# V1.1 - Fixing error message handling of values
# V1.2 - Added some help texts
# V1.3 - Renaming of defs
# V1.4 - Adding support of reading multiple files
# V1.4.1 - Fixed writing in different files
###############################################
# Imports
import configparser
import logging
import json
import os
import time
###############################################
# Declarations
configparser.BasicInterpolation() #NOT WORKING NEED TO FIX FOR ADDING %
logging.getLogger().setLevel(logging.DEBUG) #I THINK CUSTOM LOG NAME DONT WORK HERE TOO EVEN IT IS IN SEPARATE DEFS
###############################################
def DefaultConfigWrite(file='config.ini'): #AUTO RECOVERY DOESNT WORK BCS LIB LOADS FASTER THAN I CAN REFRESH FILE I THINK , MAYBE I CAN MOVE ALL VARS OUT OF LIBS
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

def Read(value1,value2,Type=None,file='config.ini'):
    """ Read value from file
    :param value1: Config Value Category
    :type value1: str

    :param value2: Config Value Name
    :type value2: str
    
    :param Type: Config Value Type , available dict,list,int,float,bool,str if not defined otherwise 
    :type Type: str

    :param file: Config File to read , default is config.ini
    :type file: str
    """ 
    config=configparser.ConfigParser()
    log=logging.getLogger('ConfigRead')
    if os.path.isfile(file) == True :
        config.read(file)
        ValueX=config[value1]
        match Type:
            case 'dict' | 'list' : 
                try : 
                    return json.loads(ValueX[value2])
                except:
                    log.warning("Requested value "+str(value2)+" failed to load as dictionary/list!")
            case 'int' : 
                try:
                    return ValueX.getint(value2)
                except:
                    log.warning("Requested value "+str(value2)+" is not integer!")
            case 'float' : 
                try:
                    return ValueX.getfloat(value2)
                except:
                    log.warning("Requested value "+str(value2)+" is not float!")
            case 'bool' : 
                try:
                    return ValueX.getboolean(value2)
                except:
                    log.warning("Requested value "+str(value2)+" is not bool!")
            case _ : 
                try:
                    return ValueX[value2]
                except:
                    log.warning("Requested value "+str(value2)+" failed to load!")
    else :
        log.critical('Missing config file')
        time.sleep(10)

def Write(data1,data2,value,Type=None,file='config.ini'):
    config=configparser.ConfigParser()
    log=logging.getLogger('ConfigWrite')
    if os.path.isfile(file) == True :
        config.read(file)
        match Type:
            case 'list' | 'dict':
                log.critical('Not Finished') #NEED TO FINISH
            case 'int' | 'float' | 'bool' | 'str' | 'listfull' | 'dictfull' : #full not tested
                try :
                    config[data1][data2]=str(value)
                except:
                    log.warning('Updating value of '+str(data2)+' failed!')
                else:
                    log.debug('Edited value of '+str(data2)+' to: '+str(value))
        with open(file, 'w') as configfile:
            config.write(configfile)
    else :
        log.critical('Missing config file')
        time.sleep(10)
        
        
if __name__ == '__main__': #USED FOR MY EASE OF GENERATING CONFIG FILE
    DefaultConfigWrite()
