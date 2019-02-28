import pandas as pd

def compile_teams(rawdata):
    datadict = {}
    for rawrow in rawdata.iterrows():
        for alliance in ("red", "blue"):
            for num in ("1", "2", "3"):
                teamnum = rawrow[1][alliance+num]
                datarow = datadict.get(teamnum, None)
                match = {"gamesPlayed":1,
                         "totalScored":rawrow[1]["score"+alliance.title()+"Final"],
                         "totalFouled":rawrow[1]["score"+alliance.title()+"Foul"],
                         "totalAuto":rawrow[1]["score"+alliance.title()+"Auto"]}
                if datarow == None:
                    datarow = match
                else:
                    datarow = {key:datarow[key]+match[key] for key in datarow.keys()}
                datadict[teamnum] = datarow
    compileddata = pd.DataFrame(data=datadict.values(), index=datadict.keys())
    compileddata["avgScored"] = round(compileddata["totalScored"]/compileddata["gamesPlayed"], 2)
    compileddata["avgFouled"] = round(compileddata["totalFouled"]/compileddata["gamesPlayed"], 2)
    compileddata["avgAuto"] = round(compileddata["totalAuto"]/compileddata["gamesPlayed"], 2)
    return compileddata
