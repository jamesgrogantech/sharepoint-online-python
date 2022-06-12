# SharePoint Online Python

Currently Under Development, PRs are welcome.

Allows users to access SharePoint List data within a locally running Python script. Supports Microsoft Active Directory SSO for SharePoint Online.

Will open a new browser window -> allow the user to login -> then produce an access token for the local Python script to authenticate for SharePoint.

This is only suitable for python scripts running on a local machine as it requires user input to authenticate. This library is tightly integrated with Pandas to allow simple read write between a SharePoint List and a Pandas dataframe.

## Setup

1. Install package:

   ```shell
   pip install sharepoint-online-python
   ```

2. Import:

   ```python
   from sharepoint_online import SharePoint
   ```

## Example

```python
from dotenv import load_dotenv
import os
from sharepoint_online import SharePoint

load_dotenv()

# it is advisable to load these details in from an .env file
AUTH_URL = os.environ.get("AUTH_URL")
CLIENT_ID = os.environ.get("CLIENT_ID")
TOKEN_URL = os.environ.get("TOKEN_URL")
SITE_ID = os.environ.get("SITE_ID")
LIST_ID = os.environ.get("LIST_ID")

# initialize the SharePoint object
sp = SharePoint(CLIENT_ID, AUTH_URL, TOKEN_URL, SITE_ID)

# get the list as a pandas dataframe
working_df = sp.get_list_df(LIST_ID, expand="fields")

# reassign the title column as "New Title"
working_df["Title"] = "New Title"

# update the list based on the modified dataframe
sp.update_rows(LIST_ID, working_df)

# get the updated list as a dataframe
print(sp.get_list_df(LIST_ID, expand="fields"))

```

This is based on the Microsoft Graph API and the docs for the currently supported request is here:
https://docs.microsoft.com/en-us/graph/api/list-get?view=graph-rest-1.0&tabs=http

In order to use this, you must first have access to the Azure Active Directory in your tenant and have permission to create App Registrations.

Follow the steps below to gain access to setup the app registration and find the necessary details:

1. Create a new Active Directory app registration and get Client/Application ID from the Overview Page.
2. Get Auth and Token endpoints by clicking the "Endpoints" button on the top bar of the Overview Page. Use the "OAuth 2.0 authorization endpoint (v2)" and "OAuth 2.0 token endpoint (v2)" urls.
3. Click API Permissions -> add a permission -> Microsoft Graph -> Delegated Permissions -> Sites and select Sites.Read.All then click Add Permissions. You may need to get these permissions approved by the tenant administrator.
4. Click Authentication -> add a platform -> Mobile and desktop applications -> and enter: http://localhost:3000
5. Find the site ID from this tutorial: https://www.sharepointdiary.com/2018/04/sharepoint-online-powershell-to-get-site-collection-web-id.html
6. Find the list ID by going to the list sharepoint page, click the cog on the top right, then click "List Settings". In the URL should be a parameter List=%7B..................%7D. Copy everything between the %7B and %7D but not including.

## To-do List

- Add new rows to list
- Add new columns
- Testing
