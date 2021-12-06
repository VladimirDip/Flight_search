from pprint import pprint
import requests
import my_private_date

API_SHEETY_PRICES = my_private_date.API_SHEETY_PRICES
API_SHEETY_NAMES = my_private_date.API_SHEETY_NAMES

class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        req = requests.get(url=API_SHEETY_PRICES)
        sheet_data = req.json()
        self.destination_data = sheet_data["prices"]
        # pprint(sheet_data)
        return self.destination_data

    def update_destination_code(self):
        for city in self.destination_data:
            new_data = {
                "price":{
                    "iataCode":city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{API_SHEETY_PRICES}/{city['id']}",
                json=new_data
            )
            # print(response.text)


    def get_customer_emails(self):
        customers_endpoint = API_SHEETY_NAMES
        response = requests.get(url=customers_endpoint)
        data = response.json()
        self.customer_data = data['names']
        return self.customer_data

