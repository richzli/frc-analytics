"""
various functions that get data from the api
"""

import base64
from urllib.request import Request, urlopen
import json
import csv
from time import time
import os

# Function to get the headers to pass into the API request function. Returns the header.
def get_headers():
    # Username and auth code should be located inside token.secret. See the README for help on that.
    tokenfile = open("token.secret", "r")
    # This converts the data into an encoded version that the server accepts.
    token = str(base64.b64encode(tokenfile.readline().encode()))[2:-1]

    headers = {
        # Tells the server to give back data in JSON format. Can replace "json" with "xml" if you want XML data, but XML is lame.
        "Accept": "application/json",
        "Authorization": "Basic " + token
    }

    return headers

# Function to get the data from the API. Returns the match data and score details.
def fetch_matches(year, eventcode):
    eventcode = eventcode.upper()
    headers = get_headers()
    
    history = get_fetch_history()
    
    # We are good digital citizens, so we limit the time between requests to 30 seconds to avoid flooding the server with requests.
    currtime = int(time())
    # Change this number if you want to call the API more frequently. Time is in seconds.
    if currtime - history < 30:
        # Also change this number so the error contains correct information.
        raise RateLimitError("Too fast! Try again in " + str(30-currtime+history) + " s.")
    else:
        update_fetch_history(currtime)
    
    # Requesting match data.
    request_matches = Request("https://frc-api.firstinspires.org/v2.0/"+year+"/matches/"+eventcode,
                      headers=headers)
    response_matches = urlopen(request_matches).read()
    data_matches = json.loads(response_matches)["Matches"]
    # Requesting qualifications score details.
    request_scores_qual = Request("https://frc-api.firstinspires.org/v2.0/"+year+"/scores/"+eventcode+"/qual",
                      headers=headers)
    response_scores_qual = urlopen(request_scores_qual).read()
    data_scores_qual = json.loads(response_scores_qual)["MatchScores"]
    # Requesting playoffs score details.
    request_scores_playoff = Request("https://frc-api.firstinspires.org/v2.0/"+year+"/scores/"+eventcode+"/playoff",
                      headers=headers)
    response_scores_playoff = urlopen(request_scores_playoff).read()
    data_scores_playoff = json.loads(response_scores_playoff)["MatchScores"]
    
    return [data_matches, data_scores_qual, data_scores_playoff]

# Function to get team details from the API. Returns a list of teams.
def fetch_teams(year, eventcode):
    eventcode = eventcode.upper()
    headers = get_headers()
    
    # Requesting teams.
    request = Request("https://frc-api.firstinspires.org/v2.0/"+year+"/teams?eventCode="+eventcode,
                      headers = headers)
    response = urlopen(request).read()
    teams = json.loads(response)

    return teams

# Function to turn a csv file into a 2D array.
def csv_to_2darray(csvfile):
    return list(csv.reader(open(csvfile)))

# Function to return the time of last API call. Creates a new file to store that data if it does not exist.
def get_fetch_history():
    # First checks if the directory exists...
    if not os.path.exists("./data"):
        # ...and if it doesn't, then creates the directory. Python is stupid and can't create a file if the directory doesn't exist.
        os.mkdir("./data")
    
    # Then checks if the actual file exists...
    if os.path.isfile("./data/history.txt"):
        # ...and if it does, then grab the number from it.
        file = open("./data/history.txt", "r")
        history = int(file.read())
        file.close()
        return history
    else:
        # ...and if it doesn't, then make a new file containing "0".
        file = open("./data/history.txt", "w")
        file.write("0")
        file.close()
        return 0

# Function to update the time of last API call.
def update_fetch_history(history):
    # First checks if the directory exists...
    if not os.path.exists("./data"):
        # ...and if it doesn't, then creates the directory.
        os.mkdir("./data")
    
    # Writes the number to a file.
    file = open("./data/history.txt", "w")
    file.write(str(history))
    file.close()

# A special exception that is passed when calls are made too quickly.
class RateLimitError(Exception):
    pass
