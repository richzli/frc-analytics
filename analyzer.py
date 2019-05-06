"""
various functions that make data into actual stats
"""

import pandas as pd
import numpy as np
from scipy import linalg as ela
import os
import accessor

def compile_teams(year, eventcode):
    eventcode = eventcode.upper()
    
    relevant_stat_endings = ("Points", "Point", "Count")
    matches_headers = ["matchNumber", "blue1", "blue2", "blue3", "red1", "red2", "red3"]

    data_matches, data_scores_qual, data_scores_playoff = accessor.fetch_matches(year, eventcode)
    all_stats = list(data_scores_qual[0]["alliances"][0].keys())
    relevant_stats = []
    for s in all_stats:
        if s.endswith(relevant_stat_endings):
            relevant_stats.append(s)

    data_matches_array = []

    for game in data_matches:
        matchNumber = game["tournamentLevel"]+str(game["matchNumber"])
        row = {"matchNumber": matchNumber}
        for team in game["teams"]:
            row[team["station"].lower()] = team["teamNumber"]
        data_matches_array.append([row[s] for s in matches_headers])

    score_headers = ["matchNumber"] + ["blue"+s for s in relevant_stats] + \
                  ["red"+s for s in relevant_stats]
    score_stats_array = []
    
    for game in data_scores_qual:
        matchNumber = game["matchLevel"]+str(game["matchNumber"])
        row = {"matchNumber": matchNumber}
        for team in game["alliances"]:
            for stat in relevant_stats:
                row[team["alliance"].lower()+stat] = int(team[stat])
        score_stats_array.append([row[s] for s in score_headers])
    
    """
    for game in data_scores_playoff:
        matchNumber = game["matchLevel"]+str(game["matchNumber"])
        row = {"matchNumber": matchNumber}
        for team in game["alliances"]:
            for stat in relevant_stats:
                row[team["alliance"].lower()+stat] = int(team[stat])
        score_stats_array.append([row[s] for s in score_headers])
    """
    
    matches_df = pd.DataFrame(data_matches_array, columns=matches_headers)
    scores_df = pd.DataFrame(score_stats_array, columns=score_headers)

    if not os.path.exists("./data/raw"):
        os.mkdir("./data/raw")
    
    compiled = pd.concat([matches_df.set_index("matchNumber"),
                          scores_df.set_index("matchNumber")], axis=1,
                         join="inner").reset_index()
    compiled.to_csv("./data/raw/" + year + eventcode + ".csv", index=False)

def get_team_numbers(teams):
    nums = []
    for team in teams["teams"]:
        nums.append(team["teamNumber"])
    return nums

def calculate_ratings(year, eventcode):
    eventcode = eventcode.upper()
    
    teamnums = get_team_numbers(accessor.fetch_teams(year, eventcode))
    teamnparray = np.array([teamnums])
    teamarray = []
    statarray = []

    data = accessor.csv_to_2darray("./data/raw/" + year + eventcode + ".csv")
    colnames = data.pop(0)
    statnames = colnames[7:]
    statnames = ["teamNum"] + [col[4:] + "_OPR" \
                 if col.startswith("blue") else \
                 col[3:] + "_DPR" for col in statnames]
    
    for row in data:
        matchnumber = row[0]
        blueteams = row[1:4]
        blueteams = [int(t) for t in blueteams]
        redteams = row[4:7]
        redteams = [int(t) for t in redteams]
        stats = row[7:]
        bluestats = stats[:len(stats)//2]
        redstats = stats[len(stats)//2:]

        teamarray.append([1 if team in blueteams else 0 for team in teamnums])
        teamarray.append([1 if team in redteams else 0 for team in teamnums])
        #i love python list comprehension
        
        statarray.append(bluestats+redstats)
        statarray.append(redstats+bluestats)

    teammatrix = np.array(teamarray, dtype=int)
    statmatrix = np.array(statarray, dtype=float)
    
    ratings = do_math(teammatrix, statmatrix)
    ratings = np.concatenate((teamnparray.T, ratings), axis=1)

    if not os.path.exists("./data/processed"):
        os.mkdir("./data/processed")
    
    pd.DataFrame(ratings).to_csv("./data/processed/" + year + eventcode + ".csv",
                                 header=statnames, index=None)
    
    #return ratings
        
def do_math(teams, stats):
    L = ela.cholesky((teams.T @ teams), lower = True, check_finite = False)
    ATb = (teams.T @ stats)
    y = ela.solve_triangular(L, ATb, lower = True, check_finite = False)
    x = ela.solve_triangular(L.T, y, check_finite = False)

    return x
