# Main Code - File Update Checker
LocalVersion=1.0
# 1. Check if this code didnt updated (IDK IF REALLY NEEDED)
# 1.1 (Display message if necessary)
# 2. Check if targeted file updated
# 2.0 UI INTRODUCTION # Every step afterwards needs UI Element
# 2.1 (Update file from server if needed)
# 2.2 (Update file on server if local is newer)
# 2.3 (Be able to sync file or notify on my phone)
##############################################################################################
# Imports
import ConfigHandler as Config
import openpyxl
import logging
import os
from github import Github
from datetime import datetime
import xlrd
##############################################################################################
# Declarations
logging.getLogger().setLevel(Config.Read('APP','logging','int')) #logging.DEBUG = 10 , logging.INFO = 20 , logging.WARNING = 30 , logging.CRITICAL = 50
InputFileToRead=Config.Read('FILE','targetfile')
InputToken=Config.Read('GITHUB','token')
##############################################################################################
logging.debug('Loading Main Code') # :)
##############################################################################################
# Classes and Definitions
def FileDeletion(file):
    if os.path.exists(file):
        try:
            os.remove(file)
        except:
            logging.debug('Deleting of file '+file+' failed!')
    else:
        logging.debug('Unable to locate file '+file)
##############################################################################################
class FileVersionCheck():
    Final=0
    String=[]
    def LocalFileVersion(FileToRead):
        try :
            WB = openpyxl.load_workbook(FileToRead,data_only=True)['Main']
        except:
            logging.warning('Loading of local workbook '+FileToRead+' failed!')
            return -1
        print(str(WB.cell(1,1).value)[3:])
        FileVersionCheck.String.append(str(WB.cell(1,1).value)[3:])
        #return int(''.join(filter(str.isdigit,str(WB.cell(1,1).value)[2:])))
        return float(str(str(WB.cell(1,1).value)[3:]).replace(',','.'))
    
    def GithubFileVersion(Token):
        try :
            Repo=Github(Token).get_repo('TheAsKo/FileUpdater')
        except :
            logging.warning('Connecting to server failed!')
            return -1
        Content=Repo.get_contents('version.ini').decoded_content
        try:
            with open('temp.ini','wb') as f:
                f.write(Content)
        except Exception as e:
            logging.warning('Failed to write file')
            return -1
        values=[Config.Read('APP','version','float','temp.ini'),Config.Read('EXCEL','version','float','temp.ini')]    
        FileDeletion('temp.ini')
        return values    
    
    def __run__(FileToRead,Token):
        Result=[LocalVersion] #THIS FORMATTING COULD BE CLEANED UP 
        Result.append(FileVersionCheck.GithubFileVersion(Token)[0])
        Result.append(FileVersionCheck.GithubFileVersion(Token)[1])
        FileVersionCheck.String.append(FileVersionCheck.GithubFileVersion(Token)[1])
        Result.append(FileVersionCheck.LocalFileVersion(FileToRead))
        logging.info('Version Checks: '+str(Result))
        FileVersionCheck.Final=Result
        return Result
##############################################################################################
def VersionCompare(Data):
    for i in range(len(Data)): #Check for errors
        if Data[i] == -1:
            logging.critical('Something went wrong! Unable to verity version!')
            return None
    if Data[0]==Data[1]:Result=[0]
    elif Data[0]>Data[1]:Result=[1]
    elif Data[0]<Data[1]:Result=[2]
    if Data[2]==Data[3]:Result.append(0)
    elif Data[2]>Data[3]:Result.append(1)
    elif Data[2]<Data[3]:Result.append(2)
    logging.debug('Version Compare: App-'+str(Result[0])+' File-'+str(Result[1]))
    logging.debug('0=Same,1=Remote is newer,2=Local is newer')
    return Result
##############################################################################################
class VersionStringRecreating():
    def floatHourToTime(fh): #HOURS ARE BUGGED
        hours, hourSeconds = divmod(fh, 1)
        minutes, seconds = divmod(hourSeconds * 60, 1)
        return (
            int(hours),
            int(minutes),
            int(seconds * 60),
        )
    def __run__(Data):
        Data = float(str(Data).replace(',','.'))
        dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(Data) - 2)
        hour, minute, second = VersionStringRecreating.floatHourToTime(Data % 1)
        dt = dt.replace(hour=hour, minute=minute, second=second)     
        return str(dt)
##############################################################################################






if __name__ == '__main__': #DEBUG
    logging.debug("Code Start")
    FileVersionCheck.__run__(InputFileToRead,InputToken)
    VersionCompare(FileVersionCheck.Final)
    print(str(FileVersionCheck.String))
    logging.debug(VersionStringRecreating.__run__(FileVersionCheck.String[0]))
    logging.debug(VersionStringRecreating.__run__(FileVersionCheck.String[1]))