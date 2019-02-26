import base64
from urllib.request import Request, urlopen
import json
import csv

tokenfile = open("token.secret", "r")
token = str(base64.b64encode(tokenfile.readline().encode()))[2:-1]

headers = {
    "Accept": "application/json",
    "Authorization": "Basic " + token
}

request = Request("https://frc-api.firstinspires.org/v2.0/2017/matches/ILCH", headers=headers)

response = urlopen(request).read()
matchdata = json.loads(response)["Matches"]


with open('data2017ILCH.csv', 'w+') as csvfile:
    headers = list(matchdata[0].keys()) + \
              ["red1", "red1dq", "red2", "red2dq", "red3", "red3dq",
               "blue1", "blue1dq", "blue2", "blue2dq", "blue3", "blue3dq"] #Copied from RLi
    writer = csv.DictWriter(csvfile, fieldnames = headers)
    writer.writeheader()
    for match in matchdata:
       writer.writerow(match)
    
    


csvfile.close()
