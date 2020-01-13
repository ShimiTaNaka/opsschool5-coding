from requests import get
import click

BASE_URL = "http://api.weatherstack.com/current"


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
                print("The city {} doesn't exists. Please try another one. For example Dublin".format(city_name))
            else:
                print(response_json["error"]["info"])
    else:
        print(response.content)
    return temperature


@click.command()
@click.option('--token', required=True, help="API Token for weatherstack.com")
@click.option('--city', required=True, help="One or more comma separated cities.For example \"New York\",Dublin")
@click.option('--weather_unit', '--T', default='Celsius', help="Weather unit.'Celsius'(Default) or 'Fahrenheit'")
def main(token, city, weather_unit):
    cities = city.split(",")
    units_names = {"Celsius": "m", "Fahrenheit": "f"}
    for city_name in cities:
        temperature = get_temperature(token, city_name, units_names[weather_unit])
        if temperature:
            print("The weather in {0} today {1} {2}".format(city_name, temperature, weather_unit))
        else:
            print("Can't get the weather for city {}".format(city_name))


if __name__ == '__main__':
    main()
