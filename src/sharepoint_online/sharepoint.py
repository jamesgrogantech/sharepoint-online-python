import requests
from .auth import Auth

class Sharepoint:
    def __init__(
        self,
        client_id,
        auth_url,
        token_url,
        site_id,
        redirect_uri="http://localhost:3000",
        scope="Sites.Read.All",
        port="3000",
    ):
        self.site_id = site_id

        self.auth = Auth(client_id, auth_url, token_url, redirect_uri, scope, port)

    def get_list_items(self, list_id, **query_params):
        access_token = self.auth.get_access_token()
        params = ""
        if query_params is not None:
            params = "?"
            for key, value in query_params.items():
                params += (key + "=" + value + "&")
                

        r = requests.get((
            "https://graph.microsoft.com/v1.0/sites/" 
            + self.site_id 
            + "/lists/"
            + list_id
            + "/items"
            + params), headers={"Authorization": "Bearer " + access_token["access_token"]}
        )
        
        return r.json()