# Python program to create 
# a file explorer in Tkinter

# import all components
# from the tkinter library
from tkinter import *

# import filedialog module
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from imageDetector import *

import os
import sys
import configparser

# Function for opening the 
# file explorer window

folderInputPath = ""
folderOutputPath = ""

def	create_config():
    config = configparser.ConfigParser()
    
    config['Folders'] = {'FolderInput'	: folderInputPath, 
                                  'folderOutput' : folderOutputPath}
    
    with open('config.ini', 'w') as configFile:
        config.write(configFile)
        
def read_config():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        global folderInputPath
        folderInputPath = config.get('Folders', 'FolderInput')
        label_selected_input_folder.configure(text="Kansio jonka kuvat tarkistetaan: "+folderInputPath)
        global folderOutputPath
        folderOutputPath = config.get('Folders', 'FolderOutput')
        label_selected_output_folder.configure(text="Kansio, minne pistetään tarkistetut kuvat: "+folderOutputPath)
    except:
        pass


def checkFolders():
	if folderOutputPath == "" or folderInputPath == "":
		messagebox.showerror('Virhe', 'Et ole valinnut kansiota')
		return False
	return True
	
def browseFilesInput():
	filename = filedialog.askdirectory(initialdir = "/",
										title = "Valitse kansio joiden sisältö tarkistetaan",
										)
	global folderInputPath 
	if os.path.isdir(filename):
		folderInputPath = filename
		label_selected_input_folder.configure(text="Valittu kansio: "+filename)

def browseFilesOutput():
	filename = filedialog.askdirectory(initialdir = "/",
										title = "Valitse kansio, jonne tarkistetut kuvat pistetään",
										)
	global folderOutputPath 
	if os.path.isdir(filename):
		folderOutputPath = filename
		label_selected_output_folder.configure(text="Valittu kansio: "+filename)

def openOutputFolder():
	path = folderOutputPath
	if checkFolders():
		os.startfile(path)

def startDetector():
	if checkFolders():
		if messagebox.askokcancel('Varoitus', 'Tämä lisää kuvia kansioon ' + folderOutputPath):
			window.title('Tarkistetaan kuvat. älä sulje ikkunaa...')
			detector = imageDetector(folderInputPath, folderOutputPath, window, updateProgressBar)
			
   
def quitProgram():
    create_config()
    sys.exit()
    
def quit_event():
    quitProgram()
    pass

def updateProgressBar(value):
    progress_bar_text.configure(text = str(value) + "%")
    progress_bar['value'] = value

def CenterWindowToDisplay(Screen: Tk, width: int, height: int):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/1.5))
    return f"{width}x{height}+{x}+{y}"

																								
# Create the root window
window = Tk()

window.geometry(CenterWindowToDisplay(window,700,500))

# Set window title
window.title('Kuvien tarkistaja')

p1 = PhotoImage(file= os.getcwd() +'/Kuvientarkastajalogo.png')
window.iconphoto(False, p1)

window.protocol("WM_DELETE_WINDOW", quit_event)


#Set window background color
window.config(background = "white")

buttonsHeight = 2

# Create a File Explorer label
label_file_explorer = Label(window, 
							text = "Kuvien tarkistaja",
							width = 100, height = 4, 
							)

label_selected_input_folder = Label(window, 
							text = "Valittu kansio, joiden kuvien sisältö tarkistetaan",
							width = 100, height = 2, 
							
							)
	
button_input_explore = Button(window, 
						text = "Valitse kansio",
						command = browseFilesInput,
						height=buttonsHeight) 

label_selected_output_folder = Label(window, 
							text = "Valittu kansio, minne tarkistetut kuvat viedään",
							width = 100, height = 2,
							)

button_output_explore = Button(window, 
						text = "Valitse kansio",
						command = browseFilesOutput,
						height=buttonsHeight) 

label_check_for_detections = Label(window, 
							text = "Tarkista kuvat",
							width = 100, height = 2,
							)

button_check_for_detections = Button(window, 
						text = "Tarkista kuvat",
						height=buttonsHeight,
                        
						command = startDetector) 
label_check_output_folder = Label(window, 
							text = "Tarkistetut kuvat",
							width = 100, height = 2,
							)

button_check_output_folder = Button(window, 
						text = "Näytä tarkistetut kuvat",
						height=buttonsHeight,
						command = openOutputFolder) 

button_exit = Button(window,
					text = "Sulje ohjelma",
					command = quitProgram) 

progress_bar_text = Label(window,
                         text= "ei olla aloitettu kuvien takastamista!"
                         )
progress_bar = ttk.Progressbar(window, maximum=100)
progress_bar.place(width=600)

# Grid method is chosen for placing
# the widgets at respective positions 
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column=1, row=1)

label_selected_input_folder.grid(column = 1, row = 2)

button_input_explore.grid(column = 1, row = 3)

label_selected_output_folder.grid(column=1, row=4)

button_output_explore.grid(column=1, row=5)

label_check_for_detections.grid(column=1, row=6)

button_check_for_detections.grid(column=1, row=7)

label_check_output_folder.grid(column=1,row=8)

button_check_output_folder.grid(column=1,row=9)

button_exit.grid(column = 1, row = 10)

progress_bar_text.grid(column= 1, row = 11, pady= 10)

progress_bar.grid(column= 1, row = 12, sticky=(N, S, E, W))

read_config()
# Let the window wait for any events
window.mainloop()
