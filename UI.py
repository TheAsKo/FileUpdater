# UI
##############################################################################################
# Imports
import MainCode as Code
import logging
import ConfigHandler as Config
from tkinter import *
from tkinter import ttk
##############################################################################################
# Declarations
logging.getLogger().setLevel(logging.DEBUG)
root = Tk()
root.title("File Version Handler")
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
        case 1 : pass # Download from server
        case 2 : pass # Upload to server
        case 3 : exit() # Force Quit
        case 4 : pass # Update the updater
        case 5 : pass # Update target file
    root.wm_state('iconic')
##############################################################################################
#  WindowCreation
mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

try: ####IDK WHERE TO PLACE THIS
    Code.FileVersionCheck.__run__(Code.InputFileToRead,Code.InputToken)
except:
    logging.critical('Failed to initialize code')
    
ttk.Label(mainframe, text="Sledovany subor: "+Config.Read('FILE','targetfile')).grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Lokalna verzia: "+Code.VersionStringRecreating.__run__(Code.FileVersionCheck.String[0])).grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, text='Verzia na servery: '+Code.VersionStringRecreating.__run__(Code.FileVersionCheck.String[1])).grid(column=1, row=3, sticky=W)
if Code.VersionCompare(Code.FileVersionCheck.Final)[1] <= 2 : ttk.Button(mainframe, text="Stiahnut subor zo servera",command=lambda:ButtonPress(1)).grid(column=1, row=4, sticky=N)
else : ttk.Button(mainframe, text="Stiahnut subor zo servera",command=lambda:ButtonPress(1),state=DISABLED).grid(column=1, row=4, sticky=N)
if Code.VersionCompare(Code.FileVersionCheck.Final)[1] != 2 : ttk.Button(mainframe, text="Nahrat subor na server",command=lambda:ButtonPress(2)).grid(column=2, row=4, sticky=N)
else : ttk.Button(mainframe, text="Nahrat subor na server",command=lambda:ButtonPress(2),state=DISABLED).grid(column=2, row=4, sticky=N)
ttk.Button(mainframe, text="Vypnut aplikaciu",command=lambda:ButtonPress(3)).grid(column=3, row=4, sticky=N)
ttk.Button(mainframe, text="Aktualizovat aplikaciu",command=lambda:ButtonPress(4),state=DISABLED).grid(column=1, row=5, sticky=N)
ttk.Button(mainframe, text="Zmenit sledovany subor",command=lambda:ButtonPress(5),state=DISABLED).grid(column=2, row=5, sticky=N)


#ttk.Label(mainframe, text="13376_400").grid(column=1, row=2, sticky=N)
#ttk.Label(mainframe, text="13376_401").grid(column=2, row=2, sticky=N)
#ttk.Label(mainframe, text="13114_402").grid(column=3, row=2, sticky=N)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)
##############################################################################################
center(root)

if __name__ == '__main__':
    logging.debug("UI Start")
    root.mainloop()