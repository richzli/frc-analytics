import base64
from urllib.request import Request, urlopen
import json
import csv
from time import time
import os

def get_headers():
    tokenfile = open("token.secret", "r")
    token = str(base64.b64encode(tokenfile.readline().encode()))[2:-1]

    headers = {
        "Accept": "application/json",
        "Authorization": "Basic " + token
    }

    return headers

def fetch_matches(year, eventcode):
    eventcode = eventcode.upper()
    headers = get_headers()
    
    history = get_fetch_history()
    
    currtime = int(time())
    if currtime - history < 30:
        raise RateLimitError("Too fast! Try again in " + str(30-currtime+history) + " s.")
    else:
        update_fetch_history(currtime)
    
    request_matches = Request("https://frc-api.firstinspires.org/v2.0/"+year+"/matches/"+eventcode,
                      headers=headers)
    response_matches = urlopen(request_matches).read()
    data_matches = json.loads(response_matches)["Matches"]
    request_scores_qual = Request("https://frc-api.firstinspires.org/v2.0/"+year+"/scores/"+eventcode+"/qual",
                      headers=headers)
    response_scores_qual = urlopen(request_scores_qual).read()
    data_scores_qual = json.loads(response_scores_qual)["MatchScores"]
    request_scores_playoff = Request("https://frc-api.firstinspires.org/v2.0/"+year+"/scores/"+eventcode+"/playoff",
                      headers=headers)
    response_scores_playoff = urlopen(request_scores_playoff).read()
    data_scores_playoff = json.loads(response_scores_playoff)["MatchScores"]
    
    return [data_matches, data_scores_qual, data_scores_playoff]

def fetch_teams(year, eventcode):
    headers = get_headers()

    request = Request("https://frc-api.firstinspires.org/v2.0/"+year+"/teams?eventCode="+eventcode,
                      headers = headers)
    response = urlopen(request).read()
    teams = json.loads(response)

    return teams

def json_to_csv(jsondict, csvfile):
    headers = list(jsondict[0].keys())[:-1] + \
              ["red1", "red1dq", "red2", "red2dq", "red3", "red3dq",
               "blue1", "blue1dq", "blue2", "blue2dq", "blue3", "blue3dq"]
                
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    
    for match in jsondict:
        teams = list(match["teams"])
        del match["teams"]
        for team in teams:
            match[team["station"].lower()] = str(team["teamNumber"])
            match[team["station"].lower()+"dq"] = team["dq"]
        writer.writerow(match)

def csv_to_2darray(csvfile):
    return list(csv.reader(open(csvfile)))

def get_fetch_history():
    if not os.path.exists("./data"):
        os.mkdir("./data")
        
    if os.path.isfile("data/history.txt"):
        file = open("data/history.txt", "r")
        history = int(file.read())
        file.close()
        return history
    else:
        file = open("data/history.txt", "w")
        file.write("0")
        file.close()
        return 0

def update_fetch_history(history):
    if not os.path.exists("./data"):
        os.mkdir("./data")
    
    file = open("data/history.txt", "w")
    file.write(str(history))
    file.close()

class RateLimitError(Exception):
    pass
