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
import time
import os
##############################################################################################
# Declarations
logging.getLogger().setLevel(logging.DEBUG)
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
            Code.DownloadFile(Config.Read('FILE','targetfile'))
            if messagebox.askyesno('File Version Handler','Subor bol uspesne stiahnuty.\nChcete ho otvorit?') == 1 : 
                subprocess.Popen(r'explorer "'+Config.Read('FILE','targetfile'))
            create_gui('Main')
        case 2 :  # Upload to server
            root.wm_state('iconic')
            Code.UploadFile(Config.Read('FILE','targetfile'))
            if messagebox.askyesno('File Version Handler','Subor bol uspesne nahraty na server.\nChcete pokracovat v pouzivani aplikacie?') == 1 : 
                create_gui('Main')
            else : exit()
        case 3 : exit() # Force Quit
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
                Input = EmailEntry.get()
                Code.SendEmail(Input,Config.Read('FILE','targetfile'),Config.Read('FILE','targetfilepath'))
            except Exception as e:
                logging.warning(e)
                logging.warning('Failed to send email!')
                messagebox.showwarning('Email sa nepodarilo odoslat!')
            finally:
                if messagebox.askyesno('File Version Handler','Subor bol uspesne odoslany na email.\nChcete pokracovat v pouzivani aplikacie?') == 1 : 
                    create_gui('Main')
                else : exit()
        case 7 : pass # Manual mode download
        case 8 : pass # Manual mode upload
        case 9 :  # Manual mode email
            create_gui('Input',9)
        case 91 : # Process input window #NOT FINISHED
            root.wm_state('iconic')
            Input = EmailEntry.get()
            file=filedialog.askopenfilename(title='Vyberte subor na odoslanie:',initialdir=Config.Read('FILE','targetfilepath'))
            
##############################################################################################
def create_gui(WindowID,ID=0):
    global mainframe
    mainframe.destroy()
    match WindowID:
        case 'Main' : mainframe = MainWindow(root)
        case 'Input' : mainframe = InputWindow(root,ID)
    mainframe.pack(padx=10, pady=10)
##############################################################################################
#  WindowCreation
#  Main Window
def MainWindow(root):

    try: #### IDK WHERE TO PLACE THIS
        Code.FileVersionCheck.__run__(Config.Read('FILE','targetfile'))
    except:
        logging.critical('Failed to initialize code')

    frame = ttk.Frame(root, padding="12 12 12 12")
    frame.grid(column=0, row=0, sticky=(N, W, E, S))
    ttk.Label(frame, text="Sledovany subor: "+Config.Read('FILE','targetfile')).grid(column=1, row=1, sticky=W)
    ttk.Label(frame, text="Lokalna verzia: "+Code.VersionStringRecreating.__run__(Code.FileVersionCheck.Final[3])).grid(column=1, row=2, sticky=W)
    ttk.Label(frame, text='Verzia na servery: '+Code.VersionStringRecreating.__run__(Code.FileVersionCheck.Final[2])).grid(column=1, row=3, sticky=W)
    if Code.VersionCompare(Code.FileVersionCheck.Final)[1] <= 2 or Config.Read('APP','debug','bool') == True  : ttk.Button(frame, text="Stiahnut subor zo servera",command=lambda:ButtonPress(1),width=30).grid(column=1, row=4, sticky=N)
    else : ttk.Button(frame, text="Stiahnut subor zo servera",command=lambda:ButtonPress(1),state=DISABLED,width=30).grid(column=1, row=4, sticky=N)
    if Code.VersionCompare(Code.FileVersionCheck.Final)[1] != 2 or Config.Read('APP','debug','bool') == True  : ttk.Button(frame, text="Nahrat subor na server",command=lambda:ButtonPress(2),width=30).grid(column=2, row=4, sticky=N)
    else : ttk.Button(frame, text="Nahrat subor na server",command=lambda:ButtonPress(2),state=DISABLED,width=30).grid(column=2, row=4, sticky=N)
    ttk.Button(frame, text="Vypnut aplikaciu",command=lambda:ButtonPress(3),width=30).grid(column=3, row=4, sticky=N)
    ttk.Button(frame, text="Aktualizovat aplikaciu",command=lambda:ButtonPress(4),state=DISABLED,width=30).grid(column=1, row=5, sticky=N)
    ttk.Button(frame, text="Zmenit sledovany subor",command=lambda:ButtonPress(5),width=30).grid(column=2, row=5, sticky=N)
    ttk.Button(frame, text="Poslat sledovany subor emailom",command=lambda:ButtonPress(6),width=30).grid(column=3, row=5, sticky=N)
    ttk.Button(frame, text="Manual stiahnutie",command=lambda:ButtonPress(7),state=DISABLED,width=30).grid(column=1, row=6, sticky=N)
    ttk.Button(frame, text="Manual nahratie",command=lambda:ButtonPress(8),state=DISABLED,width=30).grid(column=2, row=6, sticky=N)
    ttk.Button(frame, text="Manual email",command=lambda:ButtonPress(9),state=DISABLED,width=30).grid(column=3, row=6, sticky=N)
    
    for child in frame.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    return frame

###
def InputWindow(root,ButtonID):
    global EmailEntry
    frame = ttk.Frame(root, padding="12 12 12 12")
    frame.grid(column=0, row=0, sticky=(N, W, E, S))
    ttk.Label(frame, text='Zadajte prosim email:').grid(column=2, row=1)
    EmailEntry = ttk.Entry(frame)
    EmailEntry.grid(row=2, column=2)
    ttk.Button(frame, text="Get Input", command=lambda:ButtonPress(61)).grid(row=3, column=2)
    ttk.Label(frame, text='Vyberte si aky subor sa ma pouzit:').grid(column=2, row=4)
    match ButtonID :
        case 6 :
            EmailCombobox = ttk.Combobox(frame, values=["Zo servera", "Lokalny subor"])
            EmailCombobox.grid(row=5, column=2)
        case 9 | _ :
            pass
    for child in frame.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    return frame
###  
##############################################################################################


if __name__ == '__main__':
    logging.debug("UI Start")
    root = Tk()
    root.title("File Version Handler") 
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe = ttk.Frame() # LAZY FIXING OF ERROR
    create_gui('Main')
    center(root)
    root.wm_state('normal')
    root.mainloop()