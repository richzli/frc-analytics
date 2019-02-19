import base64
from urllib.request import Request, urlopen
import json

tokenfile = open("token.secret", "r")
token = str(base64.b64encode(tokenfile.readline().encode()))[2:-1]

headers = {
    "Accept": "application/json",
    "Authorization": "Basic " + token
}

request = Request("URL HERE", headers=headers)
response = urlopen(request).read()
