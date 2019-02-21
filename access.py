import base64
from urllib.request import Request, urlopen
import json
import csv #https://docs.python.org/3/library/csv.html
import dataparser

tokenfile = open("token.secret", "r")
token = str(base64.b64encode(tokenfile.readline().encode()))[2:-1]

headers = {
    "Accept": "application/json",
    "Authorization": "Basic " + token
}

year = input("Season Year: ")
eventcode = input("Event Code: ")

request = Request("https://frc-api.firstinspires.org/v2.0/"+year+"/matches/"+eventcode,
                  headers=headers) #This is the prod server! Change to staging once fixed.
response = urlopen(request).read()

matchdata = json.loads(response)["Matches"]

datafile = open("data/"+year+eventcode+".csv", "w+", newline="")

dataparser.json_to_csv(matchdata, datafile)

datafile.close()
