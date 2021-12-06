import requests
from pprint import pprint
from flight_data import FlightData
import my_private_date

TEQUILA_ENDPOINT = my_private_date.TEQUILA_ENDPOINT
TEQUILA_API_KEY = my_private_date.TEQUILA_API_KEY


class FlightSearch:

    def get_distination(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_API_KEY}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        # print(code)
        return code

    def search(self, origin_city_code, destination_city_code, from_time, to_time):
        search_end_point = f"{TEQUILA_ENDPOINT}/v2/search"
        header = {"apikey": TEQUILA_API_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "curr": "RUB",
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "max_stopovers": 1
        }
        response = requests.get(url=search_end_point, params=query, headers=header)
        try:
            results = response.json()["data"][0]
            # print(results)
        except IndexError:
            query["max_stopovers"] = 2
            response = requests.get(url=search_end_point, params=query, headers=header)
            try:
                results = response.json()["data"][0]
                # pprint(results)
            except IndexError:
                return None

            flight_data = FlightData(
                price=results["price"],
                origins_city=results["cityFrom"],
                origin_airport=results["flyFrom"],
                destination_city=results["cityTo"],
                destination_airport=results["flyTo"],
                out_date=results["route"][0]["local_departure"].split("T")[0],
                return_date=results["route"][2]["local_departure"].split("T")[0],
                stop_overs=2,
                via_city=results["route"][0]['cityTo']

            )
            print(f"City: {flight_data.destination_city}: Cost: Rub{flight_data.price}\n"
                  f"Out date: {flight_data.out_date} - Return date: {flight_data.return_date}\n"
                  f"Stop overs = {flight_data.stop_overs - 1} in the {flight_data.via_city}\n"
                  f"")
            return flight_data

        else:
            flight_data = FlightData(
                price=results["price"],
                origins_city=results["cityFrom"],
                origin_airport=results["flyFrom"],
                destination_city=results["cityTo"],
                destination_airport=results["flyTo"],
                out_date=results["route"][0]["local_departure"].split("T")[0],
                return_date=results["route"][1]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=results["route"][0]['cityTo']

            )
            print(
                f"City: {flight_data.destination_city}: Cost: Rub{flight_data.price}\n"
                f"Out date: {flight_data.out_date} - Return date: {flight_data.return_date}\n"
            )
            return flight_data
