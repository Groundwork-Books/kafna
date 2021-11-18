import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename

import pandas as pd
from pandastable import Table

def on_closing():
    mainWindow.destroy()
    exit()

class KafnaGUI(Frame):

    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.master = master
        self.master.title("Kafna")
        self.master.maxsize(500, 500)
        self.master.minsize(500, 500)

        c = Canvas(self.master)
        c.configure(yscrollincrement='10c')

        # create all of the main containers
        top_frame = Frame(self.master, bg='grey', width=450, height=50, pady=3)

        # layout all of the main containers
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        top_frame.grid(row=0, sticky="ew")

        # Create container for table
        self.center = Frame(self.master, bg='gray2', width=450, height=500, pady=3)
        self.center.grid(row=1, sticky="nsew")

        # create the widgets for the top frame
        # self.fileButton = tkinter.Button(top_frame, text="Select cherrypick file", command=self.open_file)
        # self.backButton = tkinter.Button(top_frame, text="Previous well", command=self.previous_well)
        # self.nextButton = tkinter.Button(top_frame, text="Next well", command=self.next_well)

        # layout the widgets in the top frame
        # self.fileButton.grid(row=0, column=1)
        # top_frame.grid_columnconfigure(2, weight=3)
        # self.backButton.grid(row=0, column=3)
        # self.nextButton.grid(row=0, column=4)

if __name__ == '__main__':
    mainWindow = tkinter.Tk()
    lightPanelGUIInstance = KafnaGUI(mainWindow)
    mainWindow.protocol("WM_DELETE_WINDOW", on_closing)
    mainWindow.mainloop()