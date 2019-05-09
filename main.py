"""
Creates the Interface alongside the main excution of the other python files

The interface is where you input what Year and Competition code you are looking for into text entry boxes

Calls the methods to access and analyze the data from the given Year and Competition code
"""

import accessor
import analyzer
import pandas as pd
import tkinter as tk
import os

#Function to open the spreadsheet for the filled out data
def openfile(filename):
    os.startfile(filename, "open")

"""

StatsWindow Class creates the gui that you will input your specifications for Year and Competition code into

"""

class StatsWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Individual Team Analysis")
        #Loads NNHS robotics Logo
        self.iconbitmap("resources/logo.ico")
        self.resizable(False, False)
        #Loads in the used fonts
        self.font1 = ("Calibri Light",) # http://effbot.org/tkinterbook/tkinter-widget-styling.htm
        self.font2 = ("Consolas",)
        self.fontsize1 = 10
        self.fontsize2 = 12

        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=1)

        ### DATA LOADER ###

        """
        Creates the interface with the specifced layout given in each object
        """

        self.dataloader = tk.Frame(self)
        self.dataloader.grid(row=0, column=0, sticky="NW", padx=10, pady=10)

        self.dlheader = tk.Label(self.dataloader, text = "Data Fetcher",
                                         font = self.font2 + (self.fontsize2, "bold"))
        self.dlheader.grid(row=0, column=0, columnspan=2, sticky="N")

        self.dlyearlabel = tk.Label(self.dataloader, text = "Year:",
                                   font = self.font1 + (self.fontsize1,))
        self.dlyearlabel.grid(row=1, column=0, sticky="E")

        self.dlyearentry = tk.Entry(self.dataloader, width=8,
                                    font = self.font1 + (self.fontsize1,))
        self.dlyearentry.grid(row=1, column=1, sticky="W")
        
        self.dlcodelabel = tk.Label(self.dataloader, text = "Competition Code:",
                                   font = self.font1 + (self.fontsize1,))

        self.dlcodelabel.grid(row=2, column=0, sticky="E")
        
        #Input Year
        self.dlcodeentry = tk.Entry(self.dataloader, width=8,
                                    font = self.font1 + (self.fontsize1,))
        #Input Competition Code
        self.dlcodeentry.grid(row=2, column=1, sticky="W")

        self.dlload = tk.Button(self.dataloader, text = "Get Data",
                                font = self.font1 + (self.fontsize1,),
                                command = self.analyze_match)
        self.dlload.grid(row=3, column=0, columnspan=2)

        self.dlstatustext = tk.StringVar()
        self.dlstatus = tk.Entry(self.dataloader, textvariable=self.dlstatustext,
                                font = self.font1 + (self.fontsize1,), state="disabled",
                                justify="center")
        self.dlstatus.grid(row=4, column=0, columnspan=2)

"""
analyze_match function takes in the data you inputed for the competition code and year and calls both analzyer and accessor to pull and sort the data from the API
"""
    def analyze_match(self):
        self.dlload.config(state="disabled")
        self.dlstatustext.set("Loading...")

        #Year and Competition Code you entered
        year = self.dlyearentry.get()
        ecode = self.dlcodeentry.get()

        #Trys to find the data based on the year and competiton code enterted. If the data can not be found due to wrong Year or Competition code it displays the error message "Could not fetch data."
        try:
            analyzer.compile_teams(year, ecode)
            analyzer.calculate_ratings(year, ecode)
            self.dlstatustext.set("Done!")
        except accessor.RateLimitError as e:
            self.dlstatustext.set(str(e))
            self.dlload.config(state="normal")
            return
        except Exception:
            self.dlstatustext.set("Could not fetch data.")
            self.dlload.config(state="normal")
            return
        #Trys to open the file of the finished data. If the file is not made correctly displays the error message "Could not open file"
        try:
            openfile(".\\data\\processed\\" + year + ecode + ".csv")
        except:
            self.dlstatustext.set("Could not open file.")
            self.dlload.config(state="normal")
            return

        self.dlload.config(state="normal")

"""
Runs the full program
"""
def main():
    app = StatsWindow()
    app.mainloop()

main()
