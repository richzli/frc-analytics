import pandas as pd
import numpy as np
import accessor

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

def get_team_numbers(teams):
    nums = []
    for team in teams["teams"]:
        nums.append(team["teamNumber"])
    return nums

def calculate_OPR(year, eventcode):
    teamnums = get_team_numbers(accessor.fetch_teams(year, eventcode))
    teamarray = []

    
    
    for 
    
    headers = [h for h in list(rawdata) if h.endswith(("Points", "Count"))]
    for rawrow in rawdata.iterrows():
        pass
        
