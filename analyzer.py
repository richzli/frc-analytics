import pandas as pd
import numpy as np
from scipy import linalg as ela
import accessor

def compile_teams(rawdata):
    """
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
    """
    
    relevant_stat_endings = ("Points", "Point", "Count")
    headers = ["matchNumber", "red1", "red2", "red3", "blue1", "blue2", "blue3"]

    data_matches, data_scores_qual, data_scores_playoff = rawdata
    all_stats = data_scores_qual[0]["alliances"][0].keys()
    relevant_stats = [alliances[0][s] if s.endswith(relevant_stat_endings)
                      for s in all_stats]

    data_matches_array = [headers]

    for game in data_matches:
        matchNumber = game["tournamentLevel"]+str(game["matchNumber"])
        row = {"matchNumber": matchNumber}
        for team in game["teams"]:
            row[team["station"].lower()] = team["teamNumber"]
        data_matches_array.append([row[s] for s in headers])
    
    score_stats = ["matchNumber"] + ["red"+s for s in relevant_stats] + \
                  ["blue"+s for s in relevant_stats]
    
    
    

def get_team_numbers(teams):
    nums = []
    for team in teams["teams"]:
        nums.append(team["teamNumber"])
    return nums

def calculate_ratings(year, eventcode):
    teamnums = get_team_numbers(accessor.fetch_teams(year, eventcode))
    teamnparray = np.array([teamnums])
    teamarray = []
    statarray = []

    data = accessor.csv_to_2darray("data/raw/" + year + eventcode + ".csv")
    colnames = data.pop(0)
    statnames = colnames[7:]
    statnames = ["teamNum"] + [col[3:] + "_OPR" \
                 if col.startswith("red") else \
                 col[4:] + "_DPR" for col in statnames]
    
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
    ratings = np.concatenate((teamnparray.T, ratings), axis=1)

    pd.DataFrame(ratings).to_csv("data/processed/" + year + eventcode + ".csv",
                                 header=statnames, index=None)
    
    return ratings
        
def do_math(teams, stats):
    L = ela.cholesky(teams@teams.T,lower=True,check_finite=False)
    ATb = teams.T@stats
    y = ela.solve_triangular(L, ATb, lower = True, check_finite = False)
    x = ela.solve_triangular(L, y, trans = 'T', check_finite = False)

    return x
