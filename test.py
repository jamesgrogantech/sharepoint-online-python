from dotenv import load_dotenv
import os
from sharepoint_online import SharePoint

load_dotenv()

AUTH_URL = os.environ.get("AUTH_URL")
CLIENT_ID = os.environ.get("CLIENT_ID")
TOKEN_URL = os.environ.get("TOKEN_URL")
SITE_ID = os.environ.get("SITE_ID")
LIST_ID = os.environ.get("LIST_ID")

# initialise the SharePoint object
sp = SharePoint(CLIENT_ID, AUTH_URL, TOKEN_URL, SITE_ID)

# get the list as a dataframe
working_df = sp.get_list_df(LIST_ID, expand="fields")

# reassign the title column as "New Title"
working_df["Title"] = "New Title"

# update the list based on the modified dataframe
sp.update_rows(LIST_ID, working_df)

# get the updated list as a dataframe
print(sp.get_list_df(LIST_ID, expand="fields"))
