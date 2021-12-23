from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, HTTPError
from webbrowser import open_new
import requests
import pkce
import os
import urllib.parse
import datetime
import json
import os.path
from os import path


class HTTPServerHandler(BaseHTTPRequestHandler):
    def __init__(self, request, address, server):
        super().__init__(request, address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if "code" in self.path:
            self.auth_code = self.path.split("=")[1]
            self.wfile.write(
                bytes(
                    '<html><h1 style="font-family: Arial;">You may now close this window.'
                    + "</h1></html>",
                    "utf-8",
                )
            )
            self.server.auth_code = self.auth_code.replace("&session_state", "")

    def log_request(self, format, *args):
        return


class Auth:
    def __init__(
        self,
        client_id,
        auth_url,
        token_url,
        redirect_uri="http://localhost:3000",
        scope="Sites.Read.All",
        port="3000",
    ):
        self.client_id = client_id
        self.auth_url = auth_url
        self.token_url = token_url
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.port = port

        dir_path = os.path.dirname(os.path.realpath(__file__))

        folder_exists = os.path.exists(dir_path + "/.cache")

        if not folder_exists:
            os.makedirs(dir_path + "/.cache")

        self.cache_file = dir_path + "/.cache/oauth.json"

    def get_access_token(self):
        if path.exists(self.cache_file):
            # Reading cache
            with open(self.cache_file, "r") as infile:
                access_token = json.load(infile)
            if (
                int(datetime.datetime.now().timestamp())
                < access_token["expiration_date"]
            ):
                return access_token

        code_verifier, code_challenge = pkce.generate_pkce_pair()
        ACCESS_URI = (
            self.auth_url
            + "?client_id="
            + self.client_id
            + "&redirect_uri="
            + urllib.parse.quote(self.redirect_uri, safe="")
            + "&scope="
            + self.scope
            + "&response_type=code"
            + "&code_challenge="
            + code_challenge
            + "&code_challenge_method=S256"
        )

        open_new(ACCESS_URI)
        httpServer = HTTPServer(
            ("localhost", int(self.port)),
            lambda request, address, server: HTTPServerHandler(
                request, address, server
            ),
        )
        httpServer.handle_request()
        r = requests.post(
            self.token_url,
            data={
                "grant_type": "authorization_code",
                "code": httpServer.auth_code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
                "code_verifier": code_verifier,
            },
        )
        data = r.json()
        expiration_time = datetime.datetime.now() + datetime.timedelta(
            seconds=data["expires_in"]
        )
        data["expiration_date"] = int(expiration_time.timestamp())

        with open(self.cache_file, "w+") as outfile:
            json.dump(data, outfile)

        return data
