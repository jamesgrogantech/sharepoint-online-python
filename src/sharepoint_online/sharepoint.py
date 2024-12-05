import requests
from .auth import Auth
import pandas as pd
from typing import Union


class SharePoint:
    def __init__(
        self,
        client_id: str,
        auth_url: str,
        token_url: str,
        site_id: str,
        redirect_uri: str = "http://localhost:3000",
        scope: str = "Sites.ReadWrite.All",
        port: str = "3000",
    ):
        self.site_id = site_id

        self.auth = Auth(client_id, auth_url, token_url,
                         redirect_uri, scope, port)

    def get_columns(self, list_id: str, return_ids: bool = True):
        access_token = self.auth.get_access_token()
        r = requests.get(
            (
                "https://graph.microsoft.com/v1.0/sites/"
                + self.site_id
                + "/lists/"
                + list_id
                + "/columns"
            ),
            headers={"Authorization": "Bearer " +
                     access_token["access_token"]},
        )
        data = r.json()["value"]
        if return_ids:
            newDict = {}
            for column in data:
                if column["displayName"] in newDict.values():
                    newDict[column["name"]] = column["displayName"] + \
                        " " + column["name"]
                else:
                    newDict[column["name"]] = column["displayName"]
            data = newDict
        return data

    def get_list_df(self, list_id: str, returnRaw: bool = False, **query_params) -> Union[pd.DataFrame, dict]:
        """
        Return a Pandas dataframe using the list display name,
        or return the raw data if returnRaw set to true
        """

        access_token = self.auth.get_access_token()
        params = ""
        if query_params is not None:
            params = "?"
            for key, value in query_params.items():
                params += key + "=" + value + "&"

        all_data = []
        url = (
            "https://graph.microsoft.com/v1.0/sites/"
            + self.site_id
            + "/lists/"
            + list_id
            + "/items"
            + params
        )
        
        while url:
            r = requests.get(
            url,
            headers={"Authorization": "Bearer " +
                 access_token["access_token"]},
            )
            raw = r.json()
            all_data.extend(raw["value"])
            url = raw.get('@odata.nextLink')

        raw["value"] = all_data

        if returnRaw:
            return raw

        data = raw["value"]

        columns = self.get_columns(list_id)

        simple_list = []

        for item in data:
            item["fields"]["id"] = item["id"]
            simple_list.append(item["fields"])

        df = pd.DataFrame(simple_list)

        if '@odata.etag' in df.columns:
            df = df.drop("@odata.etag", axis=1)

        df = df.set_index('id')

        df = df.rename(columns=columns)
        df = df.fillna(0)

        return df

    # Deprecated, use get_list_df(LIST_ID, True)
    def get_list_items(self, list_id, **query_params):
        return self.get_list_df(list_id, True, query_params)

    def update_row(self, list_id, row_id, row_data):
        access_token = self.auth.get_access_token()
        try:
            r = requests.patch(
                (
                    "https://graph.microsoft.com/v1.0/sites/"
                    + self.site_id
                    + "/lists/"
                    + list_id
                    + "/items/"
                    + row_id
                    + "/fields"
                ),
                headers={"Authorization": "Bearer " +
                         access_token["access_token"]},
                json=row_data,
            )
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            print(e)
            print("Error: ", r.json()['error']['message'])

    def inverse_column_map(self, list_id):
        return {v: k for k, v in self.get_columns(list_id).items()}

    def update_rows(self, list_id, new_df):
        existing_df = self.get_list_df(list_id, expand="fields")
        if set(existing_df.columns) != set(new_df.columns):
            raise Exception(
                "New columns have been added to the list, adding columns is not currently supported")
        for index, row in new_df.iterrows():
            new_dict = row.to_dict()
            existing_dict = existing_df.loc[index].to_dict()
            column_map = self.inverse_column_map(list_id)
            values = {column_map[o]: new_dict[o]
                      for o in new_dict.keys() if new_dict[o] != existing_dict[o]}
            if len(values) == 0:
                print("No changes to update on row " + str(index))
                continue
            self.update_row(list_id, str(index), values)
