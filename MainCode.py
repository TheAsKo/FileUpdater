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
from datetime import timedelta
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
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
    Final=[]
    #String=[]
    def LocalFileVersion(FileToRead):
        try :
            WB = openpyxl.load_workbook(FileToRead,data_only=True)['Main']
        except:
            logging.warning('Loading of local workbook '+FileToRead+' failed!')
            return -1
        logging.debug(str(WB.cell(1,1).value)[3:])
        #FileVersionCheck.String.append(str(WB.cell(1,1).value)[3:])
        return float(str(str(WB.cell(1,1).value)[3:]).replace(',','.'))
    
    def GithubFileVersion(FileToRead):
        DownloadFile('version.ini')
        try :
            value1=Config.Read('APP','version','float','version.ini')
        except :
            value1=-1
        try :
            value2=Config.Read('VERSION',FileToRead,'float','version.ini')
        except:
            value2=-1
        values=[value1,value2]
        for i in range(len(values)): #IDK what is writing None on error file input so this is quick fix
            if values[i] == None:
                values[i] = -1
        FileDeletion('version.ini')
        print(values)
        return values    
    
    def __run__(FileToRead):
        Result=[LocalVersion] #THIS FORMATTING COULD BE CLEANED UP ALSO DUAL RUNS DEF
        Result.append(FileVersionCheck.GithubFileVersion(FileToRead)[0])
        Result.append(FileVersionCheck.GithubFileVersion(FileToRead)[1])
        #FileVersionCheck.String.append(FileVersionCheck.GithubFileVersion()[1])
        Result.append(FileVersionCheck.LocalFileVersion(FileToRead))
        logging.info('Version Checks: '+str(Result))
        FileVersionCheck.Final=Result
        return Result
##############################################################################################
def VersionCompare(Data):
    for i in range(len(Data)): #Check for errors
        if Data[i] == -1:
            logging.warning('Something went wrong! Unable to verity version!')
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
    def __run__(Data):
        if Data == -1: return 'Neexistuje'
        Data = float(str(Data).replace(',','.'))
        days, time_fraction = divmod(Data, 1)
        date = datetime(1899, 12, 30) + timedelta(days + time_fraction)
        return str(date)[:-7]
##############################################################################################
def DownloadFile(File,ForceDelete=0):
        if '.xlsx' in File:
            FileP = File[:File.rfind('.')]+'.data' #BEATUFIL REPLACING OF FILETYPE
        else : FileP = File
        try :
            server=Github(InputToken)
            repo=server.get_repo('TheAsKo/FileUpdater')
        except Exception as e :
            logging.warning(e)
            logging.warning('Connecting to server failed!')
            return -1
        try :
            Content=repo.get_contents('data/'+FileP).decoded_content
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
def UploadFile(File1,VersionControlledFile=True):
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
    with open(File1, 'rb') as file:
        data = file.read()
    repo.update_file('data/'+FileP,'upload excel.data', data ,requests.get('https://api.github.com/repos/TheAsKo/FileUpdater/contents/data/'+FileP).json()['sha'],branch='main')
    if VersionControlledFile == True:
        DownloadFile('version.ini')
        Config.Write('VERSION',File1,FileVersionCheck.Final[3],file='version.ini')
        with open('version.ini', 'r') as file:
            data = file.read()
        repo.update_file('data/version.ini','upload version.ini',data,requests.get('https://api.github.com/repos/TheAsKo/FileUpdater/contents/data/version.ini').json()['sha'],branch='main')
    FileDeletion('version.ini')
    Github.close(server)
##############################################################################################
def SendEmail(RecipientEmail,File,Filepath):
    try:
        Filepath=r''+Filepath
        msg = MIMEMultipart()
        msg['From'] = 'theaskobot@outlook.com'
        msg['To'] = RecipientEmail
        msg['Subject'] = 'Odoslanie suboru '+str(File)
        body = "Tato sprava bola automaticky vygenerovana , prosim neodpovedajte na nu.\nV pripade akychkolvek otazok kontakujte dodavatela softveru."
        msg.attach(MIMEText(body, 'plain'))
        with open(Filepath, 'rb') as file:  # Attach a file
            attach = MIMEApplication(file.read(), _subtype=File[File.rfind('.'):])
            attach.add_header('Content-Disposition', 'attachment', filename=File)
            msg.attach(attach)
        with smtplib.SMTP('smtp.office365.com',587) as server:
            server.starttls()  # Use TLS encryption
            server.login('theaskobot@outlook.com', 'botting123')
            server.sendmail('theaskobot@outlook.com', RecipientEmail, msg.as_string())
    except Exception as e:
        logging.warning(str(e))
    finally:
        logging.info('Email with file '+str(File)+' was send to email '+str(RecipientEmail))






if __name__ == '__main__': #DEBUG
    logging.debug("Code Start")
    FileVersionCheck.__run__(Config.Read('FILE','targetfile'))
    #VersionCompare(FileVersionCheck.Final)
    #print(str(FileVersionCheck.String))
    #logging.debug(VersionStringRecreating.__run__(FileVersionCheck.Final[2]))
    #logging.debug(VersionStringRecreating.__run__(FileVersionCheck.Final[3]))
    #DownloadFile('Zoznam.xlsx')
    #UploadFile('Zoznam.xlsx',True)