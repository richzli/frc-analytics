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

def calculate_ratings(year, eventcode):
    teamnums = get_team_numbers(accessor.fetch_teams(year, eventcode))
    teamarray = []
    statarray = []

    data = accessor.csv_to_2darray(year + eventcode + ".csv")
    colnames = data.pop(0)

    for row in data:
        matchnumber = row[0]
        redteams = row[1:4]
        blueteams = row[4:7]
        stats = row[7:]
        redstats = stats[len(stats)//2:]
        bluestats = stats[:len(stats)//2]

        teamarray.append([1 if team in redteams else 0 for team in teamnums])
        teamarray.append([1 if team in blueteams else 0 for team in teamnums]}
        #i love python list comprehension

        statarray.append(redstats+bluestats)
        statarray.append(bluestats+redstats)

    teammatrix = np.array(teamarray, dtype=int)
    statmatrix = np.array(statarray, dtype=float)

    ratings = do_math(teammatrix, statmatrix)
    return ratings
        
def do_math(teams, stats):
    
