from Maps.credentials import MAPS_API_KEY
from prettyprinter import pprint as pp
import requests


ONE_MAPS_BASE_URL = "https://developers.onemap.sg/commonapi/search"
GOOGLE_MAPS_BASE_URL = "https://maps.googleapis.com/maps/api/"
DISTANCE_MATRIX_URI = "distancematrix"


def postcode_to_coordinates(postcode_list):
    address_coordinate_list = []

    for postcode in postcode_list:
        one_maps_arguments = {
            "parameters": {
                "searchVal": f"{postcode}",
                "returnGeom": "Y",
                "getAddrDetails": "Y",
                "pageNum": "1"
            }
        }
        one_maps_request = form_request_url(url=ONE_MAPS_BASE_URL, request_dict=one_maps_arguments)
        response = requests.get(url=one_maps_request)
        if response.json()["found"] == 0:
            pp(f"POSTAL CODE: {postcode} IS INVALID ")
            exit()
        else:
            latitude = response.json()["results"][0]["LATITUDE"]
            longitude = response.json()["results"][0]["LONGITUDE"]
            address = response.json()["results"][0]["ADDRESS"]
            address_coordinate_list.append(
                {
                    "latitude": latitude,
                    "longitude": longitude,
                    "address": address
                }
            )

    return address_coordinate_list


def form_request_url(url, request_dict):
    for key in request_dict:
        if key == "parameters":
            parameters_dict = request_dict[key]
            first_param = True
            for nested_key, nested_value in parameters_dict.items():
                if first_param:
                    url += "?" + f"{nested_key}" + "=" + f"{nested_value}"
                    first_param = False
                else:
                    url += "&" + f"{nested_key}" + "=" + f"{nested_value}"
        else:
            url += "/" + f"{request_dict[key]}"

    return url


def compute_duration_matrix(postcode_list):
    address_coordinate_list = postcode_to_coordinates(postcode_list=postcode_list)

    locations_list = []
    for coordinate_object in address_coordinate_list:
        locations_list.append(coordinate_object["latitude"] + "," + coordinate_object["longitude"])
    locations_string = "|".join(locations_list)

    google_maps_arguments = {
        "output_format": "json",
        "parameters": {
            "origins": f"{locations_string}",
            "destinations": f"{locations_string}",
            "language": "en-GB",
            "mode": "driving",
            "region": "sg",
            "key": f"{MAPS_API_KEY}"
        }
    }

    google_maps_request = form_request_url(url=f"{GOOGLE_MAPS_BASE_URL}" + f"{DISTANCE_MATRIX_URI}",
                                           request_dict=google_maps_arguments)
    payload = {}
    headers = {}

    response = requests.get(url=google_maps_request, headers=headers, data=payload)

    duration_matrix = []
    duration_rows_list = response.json()["rows"]
    for row_dict in duration_rows_list:
        row_elements_list = row_dict["elements"]
        duration_list = []
        for row_element_dict in row_elements_list:
            duration = row_element_dict["duration"]["value"] if row_element_dict["duration"]["value"] > 0 else -1
            duration_list.append(duration)
        duration_matrix.append(duration_list)

    return duration_matrix


if __name__ == '__main__':
    profitable_companies = ["120359", "120462", "120379", "120343", "120332", "120429"]
    unprofitable_companies = ["667970", "679910", "618495", "641682"]
    postcode_list = unprofitable_companies + profitable_companies
    compute_duration_matrix(postcode_list=postcode_list)
