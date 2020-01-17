from requests import get
import click
import sys
BASE_URL = "http://api.weatherstack.com/current"


def print_error(code, message):
    print("Error code: {0}. Message: {1} ".format(code, message))


def get_temperature(token, city_name, units):
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
                print_error(error_code, "The city '{}; doesn't exist. "
                                        "Please try another one. For example Dublin.".format(city_name))
            else:
                print_error(error_code, response_json["error"]["info"])
                sys.exit(1)
    else:
        print_error(response.status_code, response.content)
        sys.exit(1)
    return temperature


@click.command()
@click.option('--token', required=True, help="API Token for weatherstack.com")
@click.option('--city', required=True, help="One or more comma separated cities.For example \"New York\",Dublin")
@click.option('--temperature_name', '--T', default='Celsius',
              type=click.Choice(['Celsius', 'Fahrenheit'], case_sensitive=False))
def main(token, city, temperature_name):
    names_units = {"celsius": "m", "fahrenheit": "f"}
    cities = city.split(",")
    temperature_unit = names_units[temperature_name.lower()]
    for city_name in cities:
        temperature = get_temperature(token, city_name, temperature_unit)
        if temperature is not None:
            print("The weather in {0} today {1} {2}".format(city_name, temperature, temperature_name.capitalize()))


if __name__ == '__main__':
    main()
