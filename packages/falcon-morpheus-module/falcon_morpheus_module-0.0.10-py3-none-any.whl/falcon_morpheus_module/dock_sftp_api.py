import requests
import base64
import json


class DockDataAPI:
    def __init__(self, auth_url, touchless_url, morpheus_url, client_id, client_secret):
        self.auth_url = auth_url
        self.touchless_url = touchless_url
        self.morpheus_url = morpheus_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self.get_token()

    def get_token(self):
        # Encode the client_id and client_secret in base64
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode("utf-8")
        # Set the headers for authentication
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        # Send the request to obtain the access token
        response = requests.post(self.auth_url, headers=headers)
        # Check if the request was successful
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            return access_token
        else:
            print(f"Authorization failed with status code: {response.status_code}")
            # print(response.json())
            return None

    def create_sftp_user(self, ssh_key, email, access_level, access_folders=None):
        headers = {"Authorization": self.token, "Content-Type": "application/json"}
        data = {"sshKey": ssh_key, "email": email, "accessLevel": access_level}
        if access_folders:
            data["accessFolders"] = access_folders
        response = requests.post(
            self.touchless_url + "/v1/sftp", headers=headers, data=json.dumps(data)
        )
        if response.status_code == 200:
            return response.json()["ticket"]
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")

    def list_sftp_users(self):
        headers = {"Authorization": self.token, "Content-Type": "application/json"}
        response = requests.get(self.touchless_url + "/v1/sftp", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")

    def get_sftp_user(self, ticket):
        headers = {"Authorization": self.token, "Content-Type": "application/json"}
        response = requests.get(
            self.touchless_url + f"/v1/sftp/{ticket}", headers=headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")

    def update_sftp_user(self, ticket, access_level, ssh_key, access_folders):
        headers = {"Authorization": self.token, "Content-Type": "application/json"}
        data = {
            "accessLevel": access_level,
            "sshKey": ssh_key,
            "accessFolders": access_folders,
        }
        response = requests.patch(
            self.touchless_url + f"/v1/sftp/{ticket}",
            headers=headers,
            data=json.dumps(data),
        )
        if response.status_code in [200, 204]:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")

    def delete_sftp_user(self, ticket):
        headers = {"Authorization": self.token}
        response = requests.delete(
            self.base_url + f"/v1/sftp/{ticket}", headers=headers
        )
        if response.status_code == 204:
            print(f"SFTP user with ticket: {ticket} deleted successfully.")
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")

    def request_file(
        self,
        filename,
        limit,
        page,
        file_type,
        column_names,
        start_date=None,
        end_date=None,
    ):
        """
        A method to make a POST request to the API to fetch specific data.

        Parameters:
        filename (str): The name of the file.
        limit (int): Limit for the number of entries returned.
        page (int): Page number for pagination.
        file_type (str): The type of file being requested.
        column_names (list): The list of column names to be included in the response.
        start_date (str): The start date for the creation_date filter.
        end_date (str): The end date for the creation_date filter.

        Returns:
        Response from the API call.
        """
        filter_string = ""
        if start_date and end_date:
            filter_string = f"""
            filter: {{
                creation_date: {{
                    between: {{
                        start: "{start_date}",
                        end: "{end_date}"
                    }}
                }}
            }},"""

        query_string = f"""
        query {{
            {filename}(
                limit: {limit},
                page: {page},
                generate_file: true,
                file_type: {file_type},
                {filter_string}
            )
            {{
                list {{
                    { ' '.join(column_names) }
                }}
            }}
        }}"""

        # print("Query : ", query_string)
        response = requests.request(
            "POST",
            url=self.morpheus_url + "/v1/query",
            headers={
                "Authorization": f"Bearer {self.token}",
            },
            json={
                "query": query_string,
                "variables": {},
            },
        )

        if response.status_code != 200:
            # print("Reponse: ", response.json())
            raise Exception(f"Request failed with status code: {response.status_code}")

        return {
            "response": response.json(),
            "x-ticket": response.headers.get("x-ticket"),
        }

    def get_ticket_status(self, ticket_id):
        """
        A method to make a POST request to the API to get the status of a specific ticket.

        Parameters:
        ticket_id (str): The unique identifier of the ticket.

        Returns:
        Response from the API call.
        """
        query_string = f"""
        query {{
            get_tickets(
                limit: 1,
                page: 1,
                filter: {{
                    id: {{equals: "{ticket_id}"}}
                }}
            )
            {{
                page
                limit
                list {{
                    id
                    status
                    file_name
                    file_extension
                    rows_amount
                    file_size
                    compressing_size
                    created_at
                    started_at
                    finished_at
                }}
            }}
        }}"""

        response = requests.request(
            "POST",
            url=self.morpheus_url + "/v1/query",
            headers={
                "Authorization": f"Bearer {self.token}",
            },
            json={
                "query": query_string,
                "variables": {},
            },
        )

        if response.status_code != 200:
            raise Exception(f"Request failed with status code: {response.status_code}")

        return response.json()
