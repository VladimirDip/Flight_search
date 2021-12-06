from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import my_private_date

MY_EMAIL = my_private_date.MY_EMAIL
MY_PASSWORD = my_private_date.MY_PASSWORD
ORIGINS_CITY_IATA = "VVO"

data_manager = DataManager()
flight_search = FlightSearch()
notification = NotificationManager()

sheet_data = data_manager.get_destination_data()

for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_distination(row["city"])
        # print(sheet_data)

data_manager.destination_data = sheet_data
data_manager.update_destination_code()

destinations = {
    data['iataCode']: {
        'id': data['id'],
        "city": data['city'],
        "price": data['lowestPrice']
    } for data in sheet_data}
# print(destination)

tomorrow = datetime.now() + timedelta(days=1)
date_six_months_advance = (datetime.now() + timedelta(days=6 * 30))

for destitation_code in destinations:
    flight = flight_search.search(
        ORIGINS_CITY_IATA,
        destitation_code,
        from_time=tomorrow,
        to_time=date_six_months_advance
    )
    if flight is None:
        continue

    if flight.price < destinations[destitation_code]["price"]:
        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        message = f"Low price alert: Only Rub{flight.price} to fly from {flight.origins_city} - {flight.origins_airport}" \
                  f" to {flight.destination_city} - {flight.destination_airport}, from {flight.out_date} to " \
                  f"{flight.return_date}"

        if flight.stop_overs > 1:
            message += f"\nFlight has {flight.stop_overs - 1} stop over, via {flight.via_city}"

        link = f"https://www.google.com/flights?hl=en#flt={flight.origins_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origins_airport}.{flight.return_date}"

        notification.send_emails(emails, message, link)
