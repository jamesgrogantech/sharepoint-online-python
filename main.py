from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, HTTPError
from webbrowser import open_new
import requests
import pkce
from dotenv import load_dotenv
import os
import urllib.parse
import datetime
import json
import os.path
from os import path

load_dotenv()

PORT = os.environ.get("PORT")
AUTH_URL = os.environ.get("AUTH_URL")
CLIENT_ID = os.environ.get("CLIENT_ID")
REDIRECT_URL = os.environ.get("REDIRECT_URL")
SCOPE = os.environ.get("SCOPE")
TOKEN_URL = os.environ.get("TOKEN_URL")

dir_path = os.path.dirname(os.path.realpath(__file__))

folder_exists = os.path.exists(dir_path + "/.cache")

if not folder_exists:
    os.makedirs(dir_path + "/.cache")

cache_file = dir_path + "/.cache/oauth.json"

class HTTPServerHandler(BaseHTTPRequestHandler):
    def __init__(self, request, address, server):
        super().__init__(request, address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if 'code' in self.path:
            self.auth_code = self.path.split('=')[1]
            self.wfile.write(bytes('<html><h1 style="font-family: Arial;">You may now close this window.'
                              + '</h1></html>', 'utf-8'))
            self.server.auth_code = self.auth_code.replace("&session_state", "")

    def log_request(self, format, *args):
        return
          


def get_access_token():
    code_verifier, code_challenge = pkce.generate_pkce_pair()
    ACCESS_URI = (
        AUTH_URL +  
        "?client_id=" + 
        CLIENT_ID + 
        "&redirect_uri=" + 
        urllib.parse.quote(REDIRECT_URL, safe='') + 
        "&scope=" +
        SCOPE + 
        "&response_type=code" + 
        "&code_challenge=" + 
        code_challenge + 
        "&code_challenge_method=S256"
    )

    open_new(ACCESS_URI)
    httpServer = HTTPServer(
            ('localhost', int(PORT)),
            lambda request, address, server: HTTPServerHandler(
                request, address, server))
    httpServer.handle_request()
    r = requests.post(TOKEN_URL, 
        data={
            'grant_type': 'authorization_code',
            'code': httpServer.auth_code,
            'redirect_uri': REDIRECT_URL,
            'client_id': CLIENT_ID,
            'code_verifier': code_verifier
        })
    data = r.json()
    expiration_time =  datetime.datetime.now() + datetime.timedelta(seconds=data['expires_in'])
    data['expiration_date'] =   int(expiration_time.timestamp())

    with open(cache_file, "w+") as outfile:
        json.dump(data, outfile)

    return data

 
if path.exists(cache_file):
    print("Exists")
    #Reading cache
    with open(cache_file, "r") as infile:
        access_token = json.load(infile)
    if int(datetime.datetime.now().timestamp()) > access_token['expiration_date']:
        print("Out of date")
        #Token expired, get new
        access_token = get_access_token()
else:
    #No cached value, get and cache
    access_token = get_access_token()

r = requests.get("https://graph.microsoft.com/v1.0/sites/fc750661-1d01-4881-8d31-2fc88ef07d90/lists" + "/1aef1485-f4be-4d05-8ca8-e4f7c26266fa/items?expand=fields", headers={'Authorization': "Bearer " + access_token["access_token"]})

