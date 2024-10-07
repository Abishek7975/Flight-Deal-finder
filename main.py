#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from pprint import pprint
from data_manager import DataManager
import datetime
from notification_manager import NotificationManager
from time import sleep

FROM_CITY = "LON"

flight_search = FlightSearch()
data_manager = DataManager()
data_manager.get_destination_data()
data_manager.update()


depart_date = datetime.datetime.now().date() + datetime.timedelta(days=1)
return_date = datetime.datetime.now().date() + datetime.timedelta(days=30*6)

sheet_data = data_manager.get_destination_data()
print(sheet_data)

for data in sheet_data:
    to_city = data["city"]
    code = data["iataCode"]
    price = data["lowestPrice"]
    print(code)
    print(f"Getting flights for {to_city}...")
    flights = flight_search.find_flights(FROM_CITY,code, depart_date,return_date)
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{to_city}: {cheapest_flight.price}")
    print(cheapest_flight.price)
    print(price)
    if cheapest_flight.price != 'N/A':
        if cheapest_flight.price < price:
            notification_manager = NotificationManager(cheapest_flight.price, FROM_CITY, code, depart_date,return_date)
            notification_manager.send_sms()

    sleep(10)









