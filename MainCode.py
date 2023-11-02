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
import requests
##############################################################################################
# Declarations
logging.getLogger().setLevel(Config.Read('APP','logging','int')) #logging.DEBUG = 10 , logging.INFO = 20 , logging.WARNING = 30 , logging.CRITICAL = 50
InputFileToRead=Config.Read('FILE','targetfile')
#InputToken=Config.Read('GITHUB','token')
InputToken='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'
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
        logging.debug(str(WB.cell(1,1).value)[3:])
        FileVersionCheck.String.append(str(WB.cell(1,1).value)[3:])
        return float(str(str(WB.cell(1,1).value)[3:]).replace(',','.'))
    
    def GithubFileVersion():
        DownloadFile('version.ini')
        values=[Config.Read('APP','version','float','version.ini'),Config.Read('EXCEL','version','float','version.ini')]    
        FileDeletion('version.ini')
        return values    
    
    def __run__(FileToRead,Token):
        Result=[LocalVersion] #THIS FORMATTING COULD BE CLEANED UP 
        Result.append(FileVersionCheck.GithubFileVersion()[0])
        Result.append(FileVersionCheck.GithubFileVersion()[1])
        FileVersionCheck.String.append(FileVersionCheck.GithubFileVersion()[1])
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
def DownloadFile(File,ForceDelete=0):
        if '.xlsx' in File:
            FileP = File[:File.rfind('.')]+'.data' #BEATUFIL REPLACING OF FILETYPE
        else : FileP = File
        try :
            server=Github(InputToken)
            repo=server.get_repo('TheAsKo/FileUpdater')
        except :
            logging.warning('Connecting to server failed!')
            return -1
        try :
            Content=repo.get_contents(FileP).decoded_content
        except Exception as e :
            logging.warning(e)
            return -1
        Github.close(server)
        if ForceDelete == 1:
            FileDeletion(File)
        try:
            with open(File,'wb') as file:
                file.write(Content)
        except: 
            logging.warning('Failed to write file')
            return -1
##############################################################################################  
def UploadFile(File1,VersionControlledFile):
    if '.xlsx' in File1:
        FileP = File1[:File1.rfind('.')]+'.data' #BEATUFIL REPLACING OF FILETYPE
    else : FileP = File1
    try :
        server=Github(InputToken)
        repo=server.get_repo('TheAsKo/FileUpdater')
    except Exception as e :
        logging.warning('Connecting to server failed!')
        logging.warning(e)
        return -1
    with open('Zoznam.xlsx', 'rb') as file:
        data = file.read()
    repo.update_file(FileP,'upload excel.data', data ,requests.get('https://api.github.com/repos/TheAsKo/FileUpdater/contents/'+FileP).json()['sha'],branch='main')
    if VersionControlledFile == True:
        DownloadFile('version.ini')
        Config.Write('EXCEL','version',FileVersionCheck.Final[3],file='version.ini')
        with open('version.ini', 'r') as file:
            data = file.read()
        repo.update_file('version.ini','dekete old version.ini',data,requests.get('https://api.github.com/repos/TheAsKo/FileUpdater/contents/version.ini').json()['sha'],branch='main')
    Github.close(server)






if __name__ == '__main__': #DEBUG
    logging.debug("Code Start")
    FileVersionCheck.__run__(InputFileToRead,InputToken)
    #VersionCompare(FileVersionCheck.Final)
    #print(str(FileVersionCheck.String))
    #logging.debug(VersionStringRecreating.__run__(FileVersionCheck.String[0]))
    #logging.debug(VersionStringRecreating.__run__(FileVersionCheck.String[1]))
    #DownloadFile('Zoznam.xlsx')
    UploadFile('Zoznam.xlsx',True)