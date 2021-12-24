# SharePoint Online Python

Currently Under Development 

Allows users to access Sharepoint data within a locally running Python script. Supports Microsoft Active Directory SSO for SharePoint Online.

Will open a new browser window -> allow the user to login -> then produce an access token for the local Python script to authenticate for SharePoint. 

This is only suitable for python scripts running on a local machine as it requires user input to authenticate. Ideal for running in a Jupyter Notebook environment and integrating with Pandas.

## Setup

1. Install package:

    ```shell
    pip install sharepoint-online-python
    ```
2. Import:

    ```python
    from sharepoint-online-python import sharepoint
    ```

## Example

```python
from sharepoint_online import sharepoint

# Create an instance of 'Sharepoint'
sp = sharepoint.Sharepoint(CLIENT_ID, AUTH_URL, TOKEN_URL, SITE_ID)

# Use 'get_list_items' to make a get request to the list and retrieve the items in JSON format.
# You can also add query parameters as kwargs as shown with 'expand="fields" to get the field data' 
print(sp.get_list_items(LIST_ID, expand="fields"))
```

### With Pandas 

```python
items = sp.get_list_items(LIST_ID, expand="fields")["value"]

simple_list = []

for item in items:
    simple_list.append(item["fields"])

df = pd.DataFrame(simple_list)

## Removes the unique id provided by Sharepoint as this is often unwanted.
df.drop('@odata.etag', axis=1, inplace=True)

print(df) ## or simply df to produce a formatted table if used in Jupyter Notebooks
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
