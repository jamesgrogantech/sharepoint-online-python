from dotenv import load_dotenv
import os
from sharepoint_online import sharepoint

load_dotenv()

PORT = os.environ.get("PORT")
AUTH_URL = os.environ.get("AUTH_URL")
CLIENT_ID = os.environ.get("CLIENT_ID")
REDIRECT_URL = os.environ.get("REDIRECT_URL")
SCOPE = os.environ.get("SCOPE")
TOKEN_URL = os.environ.get("TOKEN_URL")
SITE_ID = os.environ.get("SITE_ID")
LIST_ID = os.environ.get("LIST_ID")

sp = sharepoint.Sharepoint(CLIENT_ID, AUTH_URL, TOKEN_URL, SITE_ID)

print(sp.get_list_items(LIST_ID, expand="fields"))