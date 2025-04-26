# Python program to create 
# a file explorer in Tkinter

# import all components
# from the tkinter library
from tkinter import *

# import filedialog module
from tkinter import filedialog
from tkinter import messagebox

import os

# Function for opening the 
# file explorer window

folderInputPath = ""
folderOutputPath = ""


def browseFilesInput():
	filename = filedialog.askdirectory(initialdir = "/",
										title = "Valitse kansio joiden sisältö tarkistetaan",
										)
	global folderInputPath 
	folderInputPath = filename
	
	# Change label contents
	label_selected_input_folder.configure(text="Valittu kansio: "+filename)

def browseFilesOutput():
	filename = filedialog.askdirectory(initialdir = "/",
										title = "Valitse kansio, jonne tarkistetut kuvat pistetään",
										)
	global folderOutputPath 
	folderOutputPath = filename
	
	# Change label contents
	label_selected_output_folder.configure(text="Valittu kansio: "+filename)

def openOutputFolder():
	path = folderOutputPath
	if path == "":
		messagebox.showerror('Virhe', 'Et ole valinnut kansiota')
		return
	os.startfile(path)
	
																								
# Create the root window
window = Tk()

# Set window title
window.title('Kuvien tarkistaja')

# Set window size
window.geometry("700x500")

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
						height=buttonsHeight
                        )
						#command = browseFiles) 
label_check_output_folder = Label(window, 
							text = "Tarkistetut kuvat",
							width = 100, height = 2,
							)

button_check_output_folder = Button(window, 
						text = "Näytä tarkistetut kuvat",
						height=buttonsHeight,
						command = openOutputFolder) 

button_exit = Button(window, 
					text = "Exit",
					command = exit) 

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

# Let the window wait for any events
window.mainloop()
