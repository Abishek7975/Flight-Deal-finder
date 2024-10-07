import os
import requests
from pprint import pprint


AMADEUS_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.environ["AMADEUS_KEY"]
        self._api_secret = os.environ["AMADEUS_SECRET"]
        self._token = self._get_new_token()

    def _get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            "grant_type": "client_credentials",
            "client_id" : self._api_key,
            "client_secret": self._api_secret
        }

        response = requests.post(url=AMADEUS_URL,headers=header, data=body)
        return response.json()['access_token']


    def get_iata_code(self, city):
        URL = f"https://test.api.amadeus.com/v1/reference-data/locations/cities?keyword={city}&max=1"
        header = {"Authorization": f"Bearer {self._token}"}

        body = {
            "keyword": city,
            "max": "1",
            "include": "AIRPORTS",
        }
        response = requests.get(url=URL, headers=header, data=body).json()
        try:
            code = response['data'][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city}.")
            return "N/A"
        except KeyError:
            print(f"IndexError: No airport code found for {city}.")
            return "N/A"
        return code


    def find_flights(self,from_city,to_city, from_time, to_time):

        print(from_city,to_city,from_time,to_time)
        Flight = "https://test.api.amadeus.com/v2/shopping/flight-offers"

        header = {"Authorization": f"Bearer {self._token}"}

        query = {
            "originLocationCode": str(from_city),
            "destinationLocationCode": str(to_city),
            "departureDate": from_time,
            "returnDate": to_time,
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "max": "10",
        }

        response = requests.get(url=Flight, headers=header, params=query)
        pprint(response)
        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()





