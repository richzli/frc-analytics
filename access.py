import base64
from urllib.request import Request, urlopen
import json

tokenfile = open("token.secret", "r")
token = str(base64.b64encode(tokenfile.readline().encode()))[2:-1]

headers = {
    "Accept": "application/json",
    "Authorization": "Basic " + token
}

request = Request("https://frc-api.firstinspires.org/v2.0/2017/matches/CMPMO", headers=headers)
response = urlopen(request).read()

data = json.loads(response)["Matches"]
