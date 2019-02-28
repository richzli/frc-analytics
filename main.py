import accessor
import analyzer
import pandas as pd
import tkinter as tk
from os.path import isfile

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

        self.dlcodelabel = tk.Label(self.dataloader, text = "Competition Code:",
                                   font = self.font1 + (self.fontsize1,))
        self.dlcodelabel.grid(row=1, column=0, sticky="E")

        self.dlcodeentry = tk.Entry(self.dataloader, width=8,
                                    font = self.font1 + (self.fontsize1,))
        self.dlcodeentry.grid(row=1, column=1, sticky="W")

        self.dlyearlabel = tk.Label(self.dataloader, text = "Year:",
                                   font = self.font1 + (self.fontsize1,))
        self.dlyearlabel.grid(row=2, column=0, sticky="E")

        self.dlyearentry = tk.Entry(self.dataloader, width=8,
                                    font = self.font1 + (self.fontsize1,))
        self.dlyearentry.grid(row=2, column=1, sticky="W")

        self.dlload = tk.Button(self.dataloader, text = "Load Data",
                                font = self.font1 + (self.fontsize1,),
                                command = self.get_data)
        self.dlload.grid(row=3, column=0, columnspan=2)

        self.dlstatustext = tk.StringVar()
        self.dlstatus = tk.Entry(self.dataloader, textvariable=self.dlstatustext,
                                font = self.font1 + (self.fontsize1,), state="disabled",
                                justify="center")
        self.dlstatustext.set("No data loaded.")
        self.dlstatus.grid(row=4, column=0, columnspan=2)

        ### DATA VIEWER ###

        self.dataviewer = tk.Frame(self)
        self.dataviewer.grid(row=0, column=1, sticky="NE", pady=10, padx=10)

        self.dvheader = tk.Label(self.dataviewer, text = "Statistics",
                                         font = self.font2 + (self.fontsize2, "bold"))
        self.dvheader.grid(row=0, column=0, columnspan=2, sticky="S")

        self.dvteamlabel = tk.Label(self.dataviewer, text = "Team Number:",
                                    font = self.font1 + (self.fontsize1,))
        self.dvteamlabel.grid(row=1, column=0, sticky="E")

        self.dvteamentry = tk.Entry(self.dataviewer, width=8,
                                    font = self.font1 + (self.fontsize1,),
                                    state="disabled")
        self.dvteamentry.grid(row=1, column=1, sticky="W")

        self.dvload = tk.Button(self.dataviewer, text = "Get Stats",
                                font = self.font1 + (self.fontsize1,),
                                state="disabled", command=self.display_data)
        self.dvload.grid(row=2, column=0, columnspan=2)

        self.dvgplabel = tk.Label(self.dataviewer, text = "Games Played:",
                                 font = self.font1 + (self.fontsize1,))
        self.dvgplabel.grid(row=3, column=0, sticky="E")

        self.dvgptext = tk.StringVar()
        self.dvgp = tk.Entry(self.dataviewer, textvariable=self.dvgptext,
                             font = self.font1 + (self.fontsize1,), width=8,
                             state="disabled", justify="center")
        self.dvgp.grid(row=3, column=1, sticky="W")

        self.dvaplabel = tk.Label(self.dataviewer, text = "Average Points:",
                                 font = self.font1 + (self.fontsize1,))
        self.dvaplabel.grid(row=4, column=0, sticky="E")

        self.dvaptext = tk.StringVar()
        self.dvap = tk.Entry(self.dataviewer, textvariable=self.dvaptext,
                             font = self.font1 + (self.fontsize1,), width=8,
                             state="disabled", justify="center")
        self.dvap.grid(row=4, column=1, sticky="W")

        self.dvaflabel = tk.Label(self.dataviewer, text = "Average Fouls:",
                                 font = self.font1 + (self.fontsize1,))
        self.dvaflabel.grid(row=5, column=0, sticky="E")

        self.dvaftext = tk.StringVar()
        self.dvaf = tk.Entry(self.dataviewer, textvariable=self.dvaftext,
                             font = self.font1 + (self.fontsize1,), width=8,
                             state="disabled", justify="center")
        self.dvaf.grid(row=5, column=1, sticky="W")


    def get_data(self):
        self.dfraw = None
        self.dfcompiled = None
        self.lock_stats()
        self.dlstatustext.set("Loading...")
        
        year = self.dlyearentry.get()
        ecode = self.dlcodeentry.get()

        if isfile("data/"+year+ecode+".csv"):
            self.dfraw = pd.read_csv("data/"+year+ecode+".csv")
            self.dfcompiled = analyzer.compile_teams(self.dfraw)
            self.dlstatustext.set(year+ecode+".csv loaded.")
            self.unlock_stats()
        else:
            try:
                accessor.fetch_match(year, ecode)
                self.dfraw = pd.read_csv("data/"+year+ecode+".csv")
                self.dfcompiled = analyzer.compile_teams(self.dfraw)
                self.dlstatustext.set(year+ecode+".csv loaded.")
                self.unlock_stats()
            except:
                self.dlstatustext.set("Unable to fetch data.")

    def display_data(self):
        if int(self.dvteamentry.get()) in self.dfcompiled.index:
            self.dvgptext.set(str(int(self.dfcompiled.loc[int(self.dvteamentry.get())]["gamesPlayed"])))
            self.dvaptext.set(str(self.dfcompiled.loc[int(self.dvteamentry.get())]["avgScored"]))
            self.dvaftext.set(str(self.dfcompiled.loc[int(self.dvteamentry.get())]["avgFouled"]))
        else:
            self.dvgptext.set("N/A")
            self.dvaptext.set("N/A")
            self.dvaftext.set("N/A")
    
    def lock_stats(self):
        self.dvteamentry.delete(0, "end")
        self.dvteamentry.config(state="disabled")
        self.dvload.config(state="disabled")

    def unlock_stats(self):
        self.dvteamentry.config(state="normal")
        self.dvload.config(state="normal")

def main():
    app = StatsWindow()
    app.mainloop()

main()
