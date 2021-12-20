# sharepoint-online-python

Currently Under Development 

Allows users to access Sharepoint data within a locally running Python script. Supports Microsoft Active Directory SSO for SharePoint Online.

Will open a new browser window -> allow the user to login -> then produce an access token for the local Python script to authenticate for SharePoint. 

## Setup

1. Create a new .env file from .env.example
2. Create a new Active Directory app registration and get Client/Application ID from the Overview Page.
3. Get Auth and Token endpoints by clicking the "Endpoints" button on the top bar of the Overview Page. Use the "OAuth 2.0 authorization endpoint (v2)" and "OAuth 2.0 token endpoint (v2)" urls.
4. Click API Permissions -> add a permission -> Microsoft Graph -> Delegated Permissions -> Sites and select Sites.Read.All then click Add Permissions. You may need to get these permissions approved by the tenant administrator. 
5. Click Authentication -> add a platform -> Mobile and desktop applications -> and enter: http://localhost:3000




