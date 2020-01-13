from requests import get
import click

BASE_URL = "http://api.weatherstack.com/current"


def get_temperature_unit(temperature_name):
    names_units = {"Celsius": "m", "Fahrenheit": "f"}
    temperature_unit = None
    try:
        temperature_unit = names_units[temperature_name]
    except KeyError:
        print("The temperature name '{}' doesn't exist.".format(temperature_name))
        keys_list = list(names_units.keys())
        print("Please choose {0} or {1}.".format(keys_list[0], keys_list[1]))
    return temperature_unit


def get_temperature(token, city_name, units):
    temperature = None
    good_response_code = 200
    request_failed_code = 615
    params = {'access_key': token, 'units': units, 'query': city_name}
    response = get(BASE_URL, params)
    if response.status_code == good_response_code:
        response_json = response.json()
        try:
            temperature = response_json["current"]["temperature"]
        except KeyError:  # if requested key doesn't exists
            temperature = None
            error_code = response_json["error"]["code"]
            if error_code == request_failed_code:
                print("The city '{}; doesn't exist. Please try another one. For example Dublin".format(city_name))
            else:
                print(response_json["error"]["info"])
    else:
        print(response.content)
    return temperature


@click.command()
@click.option('--token', required=True, help="API Token for weatherstack.com")
@click.option('--city', required=True, help="One or more comma separated cities.For example \"New York\",Dublin")
@click.option('--temperature_name', '--T', default='Celsius', help="Weather unit.'Celsius'(Default) or 'Fahrenheit'")
def main(token, city, temperature_name):
    cities = city.split(",")
    temperature_unit = get_temperature_unit(temperature_name)
    if temperature_unit:
        for city_name in cities:
            temperature = get_temperature(token, city_name, temperature_unit)
            if temperature:
                print("The weather in {0} today {1} {2}".format(city_name, temperature, temperature_name))


if __name__ == '__main__':
    main()
