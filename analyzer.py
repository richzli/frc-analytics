"""
various functions that make data into actual stats
author: @richzli
"""

import pandas as pd
import numpy as np
from scipy import linalg as ela
import os
import accessor

# Function to parse the raw data and put it into a nice CSV file.
def compile_teams(year, eventcode):
    eventcode = eventcode.upper()
    
    # Add more endings if you want analyze more stats.
    relevant_stat_endings = ("Points", "Point", "Count")
    # These are hard coded, so in the event that the server changes the way the data is stored, well, you should change this.
    matches_headers = ["matchNumber", "blue1", "blue2", "blue3", "red1", "red2", "red3"]
    
    # Uses a previously-defined function to grab the data from the server.
    data_matches, data_scores_qual, data_scores_playoff = accessor.fetch_matches(year, eventcode)
    # Then gets a list of all the stat names...
    all_stats = list(data_scores_qual[0]["alliances"][0].keys())
    relevant_stats = []
    # ...and pulls out the ones that we want.
    for s in all_stats:
        if s.endswith(relevant_stat_endings):
            relevant_stats.append(s)
    
    data_matches_array = []
    
    # Parse the match data into 2D array format.
    for game in data_matches:
        # Gets a match name, like Qualification12 or Playoff3. Necessary for when pandas later sticks all the data together.
        matchNumber = game["tournamentLevel"]+str(game["matchNumber"])
        row = {"matchNumber": matchNumber}
        # Then for each match, pulls the list of teams that participated in that match.
        for team in game["teams"]:
            row[team["station"].lower()] = team["teamNumber"]
        data_matches_array.append([row[s] for s in matches_headers])
    
    score_headers = ["matchNumber"] + ["blue"+s for s in relevant_stats] + \
                  ["red"+s for s in relevant_stats]
    score_stats_array = []
    
    # Parsing the score details now.
    for game in data_scores_qual:
        # Same thing as before; pandas will use this column to match the right teams with the right data.
        matchNumber = game["matchLevel"]+str(game["matchNumber"])
        row = {"matchNumber": matchNumber}
        # Then for each match, pulls only the relevant stats.
        for team in game["alliances"]:
            for stat in relevant_stats:
                row[team["alliance"].lower()+stat] = int(team[stat])
        score_stats_array.append([row[s] for s in score_headers])
    
    # Ok so this one is sort of weird. Every data source I could find didn't use playoffs data in the OPR/DPR calculation.
    # I commented it out here so this program also doesn't include playoffs data, but if you ever want to include it, uncomment.
    """
    for game in data_scores_playoff:
        matchNumber = game["matchLevel"]+str(game["matchNumber"])
        row = {"matchNumber": matchNumber}
        for team in game["alliances"]:
            for stat in relevant_stats:
                row[team["alliance"].lower()+stat] = int(team[stat])
        score_stats_array.append([row[s] for s in score_headers])
    """
    
    # Turns all the parsed data into nice pandas DataFrames.
    matches_df = pd.DataFrame(data_matches_array, columns=matches_headers)
    scores_df = pd.DataFrame(score_stats_array, columns=score_headers)
    
    # First checks if the directory exists...
    if not os.path.exists("./data/raw"):
        # ...and if it doesn't, makes the directory.
        os.mkdir("./data/raw")
    
    # Smoosh the matches and scores DataFrames together...
    compiled = pd.concat([matches_df.set_index("matchNumber"),
                          scores_df.set_index("matchNumber")], axis=1,
                         join="inner").reset_index()
    # ...and stick the result into a CSV file and store it.
    compiled.to_csv("./data/raw/" + year + eventcode + ".csv", index=False)

# Function to get a list of team numbers from a list of teams.
def get_team_numbers(teams):
    nums = []
    for team in teams["teams"]:
        nums.append(team["teamNumber"])
    return nums

# Function to turn the raw data into OPRs and DPRs.
def calculate_ratings(year, eventcode):
    eventcode = eventcode.upper()
    
    # First, we need the team numbers.
    teamnums = get_team_numbers(accessor.fetch_teams(year, eventcode))
    teamnparray = np.array([teamnums])
    
    teamarray = []
    statarray = []
    
    # Then, we grab the raw data from the file we stored earlier.
    data = accessor.csv_to_2darray("./data/raw/" + year + eventcode + ".csv")
    colnames = data.pop(0)
    statnames = colnames[7:]
    # Changes the statnames from stuff like bluetotalPoints to totalPoints_OPR or redadjustPoints to adjustPoints_DPR.
    statnames = ["teamNum"] + [col[4:] + "_OPR" \
                 if col.startswith("blue") else \
                 col[3:] + "_DPR" for col in statnames]
    
    # Afterwards, puts data from each row in the right places for the math stuff to happen.
    for row in data:
        matchnumber = row[0]
        blueteams = row[1:4]
        blueteams = [int(t) for t in blueteams]
        redteams = row[4:7]
        redteams = [int(t) for t in redteams]
        stats = row[7:]
        bluestats = stats[:len(stats)//2]
        redstats = stats[len(stats)//2:]
        
        # Changes the teams from pure numbers into 1s (if the team is in the match) and 0s (if the team isn't in the match).
        teamarray.append([1 if team in blueteams else 0 for team in teamnums])
        teamarray.append([1 if team in redteams else 0 for team in teamnums])
        #i love python list comprehension
        
        # There are two teams, so we also have to flip the stats to analyze the other team.
        statarray.append(bluestats+redstats)
        statarray.append(redstats+bluestats)
    
    # Turns the two arrays made just above into numpy arrays.
    teammatrix = np.array(teamarray, dtype=int)
    statmatrix = np.array(statarray, dtype=float)
    
    # Math!
    ratings = do_math(teammatrix, statmatrix)
    # Once the math is done, puts the right data with the right team.
    ratings = np.concatenate((teamnparray.T, ratings), axis=1)
    
    # First checks if the directory exists...
    if not os.path.exists("./data/processed"):
        # ...and if it doesn't, makes the directory.
        os.mkdir("./data/processed")
    
    # Finally, sticks all the data in a nice CSV file and stores it.
    pd.DataFrame(ratings).to_csv("./data/processed/" + year + eventcode + ".csv",
                                 header=statnames, index=None)
    
    #return ratings

# I don't want to explain this, so just read these articles to understand what is going on:
#   https://blog.thebluealliance.com/2017/10/05/the-math-behind-opr-an-introduction/
#   https://imjac.in/ta/post/2017/10/08/oprs-and-least-squares-linear-algebra.html
def do_math(teams, stats):
    L = ela.cholesky((teams.T @ teams), lower = True, check_finite = False)
    ATb = (teams.T @ stats)
    y = ela.solve_triangular(L, ATb, lower = True, check_finite = False)
    x = ela.solve_triangular(L.T, y, check_finite = False)

    return x
