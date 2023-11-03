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
            root.destroy()
            Code.DownloadFile(Config.Read('FILE','targetfile'))
            if messagebox.askyesno('File Version Handler','Subor bol uspesne stiahnuty') == 1 : 
                subprocess.Popen(r'explorer "'+Config.Read('FILE','targetfile'))
            root.mainloop()
        case 2 :  # Upload to server
            root.destroy()
            Code.UploadFile(Config.Read('FILE','targetfile')) 
            root.mainloop()
        case 3 : exit() # Force Quit
        case 4 : pass # Update the updater
        case 5 : # Update target file
            root.wm_state('iconic')
            file=filedialog.askopenfilename()
            Config.Write('FILE','targetfile',file[file.rfind('/')+1:])
            Config.Write('FILE','targetfilepath',os.path.abspath(file))
            reset_gui()
            root.wm_state('normal') 
        case 6 : pass # Send email with file
        case 7 : pass # Manual mode download
        case 8 : pass # Manual mode upload
    #root.wm_state('iconic')
##############################################################################################
def reset_gui():
    global mainframe
    mainframe.destroy()
    mainframe = create_frame(root)
    mainframe.pack()
##############################################################################################
#  WindowCreation

def create_frame(root):

    try: #### IDK WHERE TO PLACE THIS
        Code.FileVersionCheck.__run__(Config.Read('FILE','targetfile'))
    except:
        logging.critical('Failed to initialize code')

    mainframe = ttk.Frame(root, padding="12 12 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    ttk.Label(mainframe, text="Sledovany subor: "+Config.Read('FILE','targetfile')).grid(column=1, row=1, sticky=W)
    ttk.Label(mainframe, text="Lokalna verzia: "+Code.VersionStringRecreating.__run__(Code.FileVersionCheck.Final[3])).grid(column=1, row=2, sticky=W)
    ttk.Label(mainframe, text='Verzia na servery: '+Code.VersionStringRecreating.__run__(Code.FileVersionCheck.Final[2])).grid(column=1, row=3, sticky=W)
    if Code.VersionCompare(Code.FileVersionCheck.Final)[1] <= 2 or Config.Read('APP','debug','bool') == True  : ttk.Button(mainframe, text="Stiahnut subor zo servera",command=lambda:ButtonPress(1),width=30).grid(column=1, row=4, sticky=N)
    else : ttk.Button(mainframe, text="Stiahnut subor zo servera",command=lambda:ButtonPress(1),state=DISABLED,width=30).grid(column=1, row=4, sticky=N)
    if Code.VersionCompare(Code.FileVersionCheck.Final)[1] != 2 or Config.Read('APP','debug','bool') == True  : ttk.Button(mainframe, text="Nahrat subor na server",command=lambda:ButtonPress(2),width=30).grid(column=2, row=4, sticky=N)
    else : ttk.Button(mainframe, text="Nahrat subor na server",command=lambda:ButtonPress(2),state=DISABLED,width=30).grid(column=2, row=4, sticky=N)
    ttk.Button(mainframe, text="Vypnut aplikaciu",command=lambda:ButtonPress(3),width=30).grid(column=3, row=4, sticky=N)
    ttk.Button(mainframe, text="Aktualizovat aplikaciu",command=lambda:ButtonPress(4),state=DISABLED,width=30).grid(column=1, row=5, sticky=N)
    ttk.Button(mainframe, text="Zmenit sledovany subor",command=lambda:ButtonPress(5),width=30).grid(column=2, row=5, sticky=N)
    ttk.Button(mainframe, text="Poslat sledovany subor emailom",command=lambda:ButtonPress(6),state=DISABLED,width=30).grid(column=3, row=5, sticky=N)
    ttk.Button(mainframe, text="Manual stiahnutie",command=lambda:ButtonPress(7),state=DISABLED,width=30).grid(column=1, row=6, sticky=N)
    ttk.Button(mainframe, text="Manual nahratie",command=lambda:ButtonPress(8),state=DISABLED,width=30).grid(column=2, row=6, sticky=N)

    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    return mainframe
##############################################################################################


if __name__ == '__main__':
    logging.debug("UI Start")
    root = Tk()
    root.title("File Version Handler") 
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe = create_frame(root)
    mainframe.pack()
    center(root)
    root.mainloop()