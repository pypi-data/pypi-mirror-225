import base64
import json

import requests
import xmltodict
from lexisnexisapi import credentials as cred

__version__ = "3.0.3.3"
__author__ = (
    "Robert Cuffney & Ozgur Aycan, "
    "CS Integration Consultants @ LexisNexis"
)


class APIEndpoints:
    """
    Class of API endpoints
    """
    COMPANYANDFINANCIAL = "https://services-api.lexisnexis.com/v1/CompanyAndFinancial?"
    COMPANYDOSSIERS = "https://services-api.lexisnexis.com/v1/CompanyDossiers?"
    NEWS = "https://services-api.lexisnexis.com/v1/News?"
    SOURCES = "https://services-api.lexisnexis.com/v1/Sources?"
    DOCKETS = "https://services-api.lexisnexis.com/v1/Dockets?"
    JURYVERDICTSANDSETTLEMENTS = "https://services-api.lexisnexis.com/v1/JuryVerdictsSettlements?"


def error_handler(func):
    """
    generic error handling
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred in function: '{func.__name__}'")
            print(f"error: {e}")
            print(f"args:{args}")
            print(f"kwargs:{kwargs}")
            raise  # Re-raise the exception to propagate it further

    return wrapper


def token():
    """Gets Authorization token to use in other requests."""
    client_id = cred.get_Key("WSAPI_CLIENT_ID")
    secret = cred.get_Key("WSAPI_SECRET")
    auth_url = "https://auth-api.lexisnexis.com/oauth/v2/token"
    payload = {
        "grant_type": "client_credentials",
        "scope": "http://oauth.lexisnexis.com/all",
    }
    auth = requests.auth.HTTPBasicAuth(client_id, secret)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(auth_url,
                             auth=auth,
                             headers=headers,
                             data=payload
                             )
    response.raise_for_status()  # Raise exception for bad status codes
    json_data = response.json()
    return json_data["access_token"]


@error_handler
def call_api(access_token, endpoint, **kwargs):
    """Call the API with the provided token and endpoint"""
    headers = {
               "Authorization": f"Bearer {access_token}",
               "Accept": "application/json"
               }
    url = getattr(APIEndpoints(), endpoint)
    with requests.Session() as session:
        response = session.get(headers=headers, url=url, **kwargs)
        response.raise_for_status()  # Raise exception for bad status codes
        api_data = response.json()
        return api_data


def get_base64(message):
    base64_message = base64.b64encode(message.encode("ascii")).decode("ascii")
    return base64_message


def convert_xml_content(data):
    """
    conversts the content section of the document to a
    python dictionary
    """
    for c in data["value"]:
        myDoc = c["Document"]["Content"]
        ordDict = xmltodict.parse(
            myDoc
        )  # parse out the xml, and convert to ordered dictionary
        newDict = json.loads(
            json.dumps(ordDict)
        )  # convert to regular dictionary ('unnecessary')
        c["Document"]["Content"] = newDict
    return data
