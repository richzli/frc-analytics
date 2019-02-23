import access
import tkinter as tk
from os.path import isfile

class StatsWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.overrideredirect(1)
        #self.title("Team 3061 Data Analytics")
        self.font1 = ("Calibri Light",) # http://effbot.org/tkinterbook/tkinter-widget-styling.htm
        self.font2 = ("Consolas",)
        self.fontsize1 = 10
        self.fontsize2 = 12

        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=1)
        
        ### TITLE BAR ###
        
        self.titlebar = tk.Frame(self)
        self.titlebar.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        
        self.tbheader = tk.Label(self.titlebar, text = "Team 3061 Data Analytics",
                       font = self.font1 + (self.fontsize1,), justify="center")
        self.tbheader.pack(fill=tk.X, side="left")

         # the following is adapted from Bryan Oakley on StackOverflow
         # what it does is allow movement of the screen by dragging the top label
        self.titlebar.bind("<ButtonPress-1>", self.start_move)
        self.titlebar.bind("<ButtonRelease-1>", self.stop_move)
        self.titlebar.bind("<B1-Motion>", self.on_move)

        self.tbheader.bind("<ButtonPress-1>", self.start_move)
        self.tbheader.bind("<ButtonRelease-1>", self.stop_move)
        self.tbheader.bind("<B1-Motion>", self.on_move)

        self.tbquitbutton = tk.Button(self.titlebar, text = "QUIT", fg = "red",
                             font = self.font2 + (10, "bold"), command = self.quit)
        self.tbquitbutton.pack(side="right")

        ### DATA LOADER ###

        self.dataloader = tk.Frame(self)
        self.dataloader.grid(row=1, column=0, sticky="NW")

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
                                font = self.font1 + (self.fontsize1,))
        self.dlload.grid(row=3, column=0, columnspan=2)

        self.dlstatustext = tk.StringVar()
        self.dlstatus = tk.Entry(self.dataloader, textvariable=self.dlstatustext,
                                font = self.font1 + (self.fontsize1,), state="disabled",
                                justify="center")
        self.dlstatustext.set("No data loaded.")
        self.dlstatus.grid(row=4, column=0, columnspan=2)

        ### DATA VIEWER ###

        self.dataviewer = tk.Frame(self)
        self.dataviewer.grid(row=1, column=1, sticky="NE")

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
                                font = self.font1 + (self.fontsize1,))
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
        self.dvap = tk.Entry(self.dataviewer, textvariable=self.dvgptext,
                             font = self.font1 + (self.fontsize1,), width=8,
                             state="disabled", justify="center")
        self.dvap.grid(row=4, column=1, sticky="W")

        self.dvaflabel = tk.Label(self.dataviewer, text = "Average Fouls:",
                                 font = self.font1 + (self.fontsize1,))
        self.dvaflabel.grid(row=5, column=0, sticky="E")

        self.dvaftext = tk.StringVar()
        self.dvaf = tk.Entry(self.dataviewer, textvariable=self.dvgptext,
                             font = self.font1 + (self.fontsize1,), width=8,
                             state="disabled", justify="center")
        self.dvaf.grid(row=5, column=1, sticky="W")


    def acquire(self):
        pass

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x,y))

def main():
    app = StatsWindow()
    app.mainloop()
    app.destroy()

main()
