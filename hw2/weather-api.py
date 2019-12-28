from requests import get
import os
import sys

BASE_URL = "http://api.weatherstack.com/current"
ACCESS_KEY = os.environ.get('WEATHER_KEY')  # set your key in environment vars

def args_parser(args_to_parse):
    args_count = len(args_to_parse)
    last_args = ["-c", "-f"]
    request_units = {"-c": "m", "-f": "f"}
    cities_names = args_to_parse[0].split(",")  # the first argumet is for cities names
    weather_unit = request_units[last_args[0]]  # default last argument is -c
    if args_count == 2 and args_to_parse[1] in last_args:  # if there are 2 args and the second is in the list
        weather_unit = request_units[args_to_parse[1]]
    return [cities_names, weather_unit]


def get_temperature(city_name, units):
    temperature = None
    good_response_code = 200
    request_failed_code = 615
    params = {'access_key': ACCESS_KEY, 'units': units, 'query': city_name}
    response = get(BASE_URL, params)
    if response.status_code == good_response_code:
        response_json = response.json()
        try:
            temperature = response_json["current"]["temperature"]
        except KeyError:  # if requested key doesn't exists
            temperature = None
            error_code = response_json["error"]["code"]
            if error_code == request_failed_code:
                print("The city {} doesn't exists. Please try another one. For example Dublin".format(city_name))
            else:
                print(response_json["error"]["info"])
    else:
        print(response.content)
    return temperature


def main(args):
    parsed_args = args_parser(args)
    cities = parsed_args[0]
    weather_unit = parsed_args[1]
    units_names = {"m": "celsius", "f": "fahrenheit"}
    for city in cities:
        temperature = get_temperature(city, weather_unit)
        if temperature:
            print("The weather in {0} today {1} {2}".format(city, temperature, units_names[weather_unit]))
        else:
            print("Can't get the weather for city {}".format(city))


if __name__ == '__main__':
    args = sys.argv[1:]
    if not len(args) or len(args) > 2:
        print("Please provide at least one or more comma-separated names of cities.")
        print("A city name with spaces has to be inside quotes. For example \"New York\".")
        print("(Optionally) To choose weather unit please use '-c' for celsius or '-f' for fahrenheit.")
    else:
        main(args)

