"""
run this to make the gui
"""

import accessor
import analyzer
import pandas as pd
import tkinter as tk
import os

def openfile(filename):
    os.startfile(filename, "open")

class StatsWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Individual Team Analysis")
        self.iconbitmap("resources/logo.ico")
        self.resizable(False, False)
        self.font1 = ("Calibri Light",) # http://effbot.org/tkinterbook/tkinter-widget-styling.htm
        self.font2 = ("Consolas",)
        self.fontsize1 = 10
        self.fontsize2 = 12

        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=1)

        ### DATA LOADER ###

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

        self.dlcodeentry = tk.Entry(self.dataloader, width=8,
                                    font = self.font1 + (self.fontsize1,))
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

    def analyze_match(self):
        self.dlload.config(state="disabled")
        self.dlstatustext.set("Loading...")
        
        year = self.dlyearentry.get()
        ecode = self.dlcodeentry.get()

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

        try:
            openfile(".\\data\\processed\\" + year + ecode + ".csv")
        except:
            self.dlstatustext.set("Could not open file.")
            self.dlload.config(state="normal")
            return

        self.dlload.config(state="normal")

def main():
    app = StatsWindow()
    app.mainloop()

main()
