# UI
##############################################################################################
# Imports
import MainCode as Code
import logging
import ConfigHandler as Config
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import subprocess
import os
import sys
##############################################################################################
# Logging
def Logging():
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)
        handler.close()
    if not root_logger.hasHandlers():
        root_logger.setLevel(Config.Read('APP', 'logging', 'int'))
        if Config.Read('APP', 'errorlogging', 'bool'):
            file_handler = logging.FileHandler("app.log")
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)
        if os.path.exists("app.log") and Config.Read('APP', 'errorlogging', 'bool') == False :
            os.remove("app.log")
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
##############################################################################################
# Classes and Definitions
def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()
##############################################################################################
def ButtonPress(arg):
    logging.debug("Assigning Button ID: "+str(arg))
    match arg:
        case 1 : # Download from server
            root.wm_state('iconic')
            Code.DownloadFile(Config.Read('FILE','targetfile'),Config.Read('FILE','targetfilepath'),Code.FileVersionCheck.Final['Time'][1])
            if messagebox.askyesno('File Version Handler','Subor bol uspesne stiahnuty.\nChcete ho otvorit?') == 1 : 
                subprocess.Popen(r'explorer "'+Config.Read('FILE','targetfile'))
            create_gui('Main')
        case 2 :  # Upload to server
            root.wm_state('iconic')
            Code.UploadFile(Config.Read('FILE','targetfile'),Config.Read('FILE','targetfilepath'))
            if messagebox.askyesno('File Version Handler','Subor bol uspesne nahraty na server.\nChcete pokracovat v pouzivani aplikacie?') == 1 : 
                create_gui('Main')
            else : sys.exit()
        case 3 : sys.exit() # Force Quit
        case 4 : pass # Update the updater
        case 5 : # Update target file
            root.wm_state('iconic')
            file=filedialog.askopenfilename(title='Vyberte subor na sledovanie:',initialdir=Config.Read('FILE','targetfilepath'))
            Config.Write('FILE','targetfile',file[file.rfind('/')+1:])
            Config.Write('FILE','targetfilepath',os.path.abspath(file))
            create_gui('Main')
            root.wm_state('normal') 
        case 6 :  # Send email with file
            create_gui('Input',6)
        case 61 : # Process input window
            try:
                Input = InputEntry1.get()
                if InputCombo1_var.get() == 'Zo servera' :
                    pass #IDK if this is reaaaaaly needed 
                elif InputCombo1_var.get() == 'Lokalny subor' :
                    Code.SendEmail(Input,Config.Read('FILE','targetfile'),Config.Read('FILE','targetfilepath'))
            except Exception as e:
                logging.debug(e)
                logging.warning('Failed to send email!')
                if Config.Read('APP','debug','bool') == True :
                    messagebox.showwarning('File Version Handler','Email sa nepodarilo odoslat! \n '+str(e))
                else:
                    messagebox.showwarning('File Version Handler','Email sa nepodarilo odoslat!')
                create_gui('Main')
            else:
                if messagebox.askyesno('File Version Handler','Subor bol uspesne odoslany na email.\nChcete pokracovat v pouzivani aplikacie?') == 1 : 
                    create_gui('Main')
                else : exit()
        case 7 : pass # Manual mode download
        case 8 : pass # Manual mode upload
        case 9 :  # Manual mode email
            create_gui('Input',9)
        case 91 : # Process input window
            root.wm_state('iconic')
            file=filedialog.askopenfilename(title='Vyberte subor na odoslanie:',initialdir=Config.Read('FILE','targetfilepath'))
            Input = InputEntry1.get()
            root.wm_state('normal')
            try :
                Code.SendEmail(Input,os.path.relpath(file),file)
            except Exception as e:
                logging.debug(e)
                logging.warning('Failed to send email!')
                if Config.Read('APP','debug','bool') == True :
                    messagebox.showwarning('File Version Handler','Email sa nepodarilo odoslat! \n '+str(e))
                else:
                    messagebox.showwarning('File Version Handler','Email sa nepodarilo odoslat!')
                create_gui('Main')
            else:
                if messagebox.askyesno('File Version Handler','Subor bol uspesne odoslany na email.\nChcete pokracovat v pouzivani aplikacie?') == 1 : 
                    create_gui('Main')
                else : exit()
        case 10 : #Update Github Token
            Input = InputEntry1.get()
            Config.Write('GITHUB','token',Input)
            create_gui('Main')
        case 11 : # Turn debugging on/off
            create_gui('Input',11)
        case 111 : 
            if InputEntry1.get() == '6679' : create_gui('Input',111)
            else : 
                messagebox.showwarning('File Version Handler','Nespravne heslo!')
                create_gui('Main')
        case 112 :
            Config.Write('APP','debug',InputCombo1_var.get())
            Config.Write('APP','errorlogging',InputCombo2_var.get())
            Logging()
            create_gui('Main')

            
##############################################################################################
def create_gui(WindowID,ID=0):
    global mainframe
    mainframe.destroy()
    match WindowID:
        case 'Main' : mainframe = MainWindow(root)
        case 'Input' : mainframe = InputWindow(root,ID)
    mainframe.pack(padx=10, pady=10)
    root.wm_state('normal')
##############################################################################################
#  WindowCreation
#  Main Window
def MainWindow(root):
    
    try: #### IDK WHERE TO PLACE THIS
        Code.FileVersionCheck.__runos__(Config.Read('FILE','targetfile'),Config.Read('FILE','targetfilepath'))
    except Exception as e: #IF THIS HAPPENS SOMETHING IS VERY BAD
        logging.critical('Failed to initialize code')
        
    frame = ttk.Frame(root, padding="12 12 12 12")
    frame.grid(column=0, row=0, sticky=(N, W, E, S))
    ttk.Label(frame, text="Sledovany subor: "+Config.Read('FILE','targetfile')).grid(column=1, row=1, sticky=W)
    ttk.Label(frame, text="Lokalna verzia: "+str(Code.FileVersionCheck.Final['Time'][1])).grid(column=1, row=2, sticky=W)
    ttk.Label(frame, text='Verzia na servery: '+str(Code.FileVersionCheck.Final['Time'][0])).grid(column=1, row=3, sticky=W)
    if Code.FileVersionCheck.VersionFinal[1] == 1 or Config.Read('APP','debug','bool') == True  : ttk.Button(frame, text="Stiahnut subor zo servera",command=lambda:ButtonPress(1),width=30).grid(column=1, row=4, sticky=N)
    else : ttk.Button(frame, text="Stiahnut subor zo servera",command=lambda:ButtonPress(1),state=DISABLED,width=30).grid(column=1, row=4, sticky=N)
    if Code.FileVersionCheck.VersionFinal[1] == 2 or Config.Read('APP','debug','bool') == True  : ttk.Button(frame, text="Nahrat subor na server",command=lambda:ButtonPress(2),width=30).grid(column=2, row=4, sticky=N)
    else : ttk.Button(frame, text="Nahrat subor na server",command=lambda:ButtonPress(2),state=DISABLED,width=30).grid(column=2, row=4, sticky=N)
    ttk.Button(frame, text="Vypnut aplikaciu",command=lambda:ButtonPress(3),width=30).grid(column=3, row=4, sticky=N)
    ttk.Button(frame, text="Aktualizovat aplikaciu",command=lambda:ButtonPress(4),state=DISABLED,width=30).grid(column=1, row=5, sticky=N)
    ttk.Button(frame, text="Zmenit sledovany subor",command=lambda:ButtonPress(5),width=30).grid(column=2, row=5, sticky=N)
    ttk.Button(frame, text="Poslat sledovany subor emailom",command=lambda:ButtonPress(6),width=30).grid(column=3, row=5, sticky=N)
    ttk.Button(frame, text="Manual stiahnutie",command=lambda:ButtonPress(7),state=DISABLED,width=30).grid(column=1, row=6, sticky=N)
    ttk.Button(frame, text="Manual nahratie",command=lambda:ButtonPress(8),state=DISABLED,width=30).grid(column=2, row=6, sticky=N)
    ttk.Button(frame, text="Manual email",command=lambda:ButtonPress(9),width=30).grid(column=3, row=6, sticky=N)
    ttk.Button(frame, text="Obnovenie",command=lambda:create_gui('Main'),width=30).grid(column=3, row=2, sticky=N)
    ttk.Button(frame, text='Debug: '+str(Config.Read('APP','debug','bool')),command=lambda:ButtonPress(11),width=30).grid(column=3, row=3, sticky=N)
        
    for child in frame.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    return frame

###
def InputWindow(root,WindowID):
    global InputEntry1
    global InputCombo1_var
    global InputCombo2_var
    frame = ttk.Frame(root, padding="12 12 12 12")
    frame.grid(column=0, row=0, sticky=(N, W, E, S))
    match WindowID :
        case 6 :
            ttk.Label(frame, text='Zadajte prosim email:').grid(column=2, row=1,sticky=N)
            InputEntry1 = ttk.Entry(frame , width=40)
            InputEntry1.grid(row=2, column=2,sticky=N)
            ttk.Label(frame, text='Vyberte si aky subor sa ma pouzit:').grid(column=2, row=4)
            ttk.Button(frame, text="Potvrdit email", command=lambda:ButtonPress(WindowID*10+1)).grid(row=3, column=2,sticky=N)
            InputCombo1_var = StringVar()
            InputCombo1_var.set('Lokalny subor')
            InputCombo1 = ttk.Combobox(frame,textvariable=InputCombo1_var,values=["Zo servera", "Lokalny subor"])
            InputCombo1.grid(row=5, column=2)
        case 9 :
            ttk.Label(frame, text='Zadajte prosim email:').grid(column=2, row=1,sticky=N)
            InputEntry1 = ttk.Entry(frame , width=40)
            InputEntry1.grid(row=2, column=2,sticky=N)            
            ttk.Button(frame, text="Potvrdit email", command=lambda:ButtonPress(WindowID*10+1)).grid(row=3, column=2,sticky=N)
        case 'GithubToken' :
            ttk.Label(frame, text='Zadajte prosim token:').grid(column=2, row=1,sticky=N)
            InputEntry1 = ttk.Entry(frame , width=40)
            InputEntry1.grid(row=2, column=2,sticky=N)          
            ttk.Button(frame, text="Potvrdit", command=lambda:ButtonPress(10)).grid(row=3, column=2,sticky=N)
        case 11 :
            ttk.Label(frame, text='Zadajte prosim heslo:').grid(column=2, row=1,sticky=N)
            InputEntry1 = ttk.Entry(frame , width=40 , show='*')
            InputEntry1.grid(row=2, column=2,sticky=N)          
            ttk.Button(frame, text="Potvrdit", command=lambda:ButtonPress(111)).grid(row=3, column=2,sticky=N)
        case 111 :
            InputCombo1_var = StringVar()
            InputCombo1_var.set('False')
            ttk.Label(frame, text='DEBUG:').grid(column=2, row=2,sticky=N)
            InputCombo1 = ttk.Combobox(frame,textvariable=InputCombo1_var,values=['True','False'])
            InputCombo1.grid(row=3, column=2)
            InputCombo2_var = StringVar()
            InputCombo2_var.set('False')
            ttk.Label(frame, text='ERROR LOGGING:').grid(column=2, row=4,sticky=N)
            InputCombo2 = ttk.Combobox(frame,textvariable=InputCombo2_var,values=['True','False'])
            InputCombo2.grid(row=5, column=2)
            ttk.Button(frame, text="Potvrdit", command=lambda:ButtonPress(112)).grid(row=6, column=2,sticky=N)
            
    for child in frame.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    return frame
###  
##############################################################################################


if __name__ == '__main__':
    Logging()
    logging.debug("UI Start")
    root = Tk()
    root.title("File Version Handler")
    root.resizable(False, False) 
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe = ttk.Frame() # LAZY FIXING OF ERROR
    try: #### FIRST LAUNCH
        Code.FileVersionCheck.__runos__(Config.Read('FILE','targetfile'),Config.Read('FILE','targetfilepath'))
    except Exception as e: 
        logging.critical('First run failed , requesting new token')
        if '401' in str(e) :
            print(e)
            create_gui('Input','GithubToken')
        else : create_gui('Main')
    else : create_gui('Main')
    root.update_idletasks()
    #root.geometry(f"{mainframe.winfo_reqwidth()}x{mainframe.winfo_reqheight()}") #I would like to have this on but idk how to autoupdate depending on window + even first window is somehow broken
    center(root)
    root.wm_state('normal')
    root.mainloop()