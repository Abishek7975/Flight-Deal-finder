import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import requests

load_dotenv()
SHEETY_URL = "https://api.sheety.co/abd320602acb7eecac7b880521e22c1c/copyOfFlightDeals/prices"

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._user,self._password)

    def get_destination_data(self):
        response = requests.get(SHEETY_URL, auth=self._authorization).json()
        sheet_data = response["prices"]
        self.destination_data = sheet_data
        return self.destination_data


    def update(self):
        print(self.destination_data)
        for city in self.destination_data:

            body = {
                "price": {
                    "iataCode" : city["iataCode"]
                }
            }

            SHEETY_PUT = f"{SHEETY_URL}/{city['id']}"

            response = requests.put(url=SHEETY_PUT, json=body,auth=self._authorization)
            print(response.text)