import csv

def json_to_csv(jsondict, csvfile):
    headers = list(jsondict[0].keys())[:-1] + \
              ["Red1", "Red1dq", "Red2", "Red2dq", "Red3", "Red3dq",
               "Blue1", "Blue1dq", "Blue2", "Blue2dq", "Blue3", "Blue3dq"]
                
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    
    for match in jsondict:
        teams = list(match["teams"])
        del match["teams"]
        for team in teams:
            match[team["station"]] = str(team["teamNumber"])
            match[team["station"]+"dq"] = team["dq"]
        writer.writerow(match)
