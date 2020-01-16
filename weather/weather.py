import click
from requests import get


@click.command()
@click.option(
  '--temperature', '-T',
  type=click.Choice(['Celsius', 'Fahrenheit'], case_sensitive=False),
  default='Celsius',
  help=("Weather temperature units type. "
        "Temperature unit options are Celsius or Fahrenheit"),
  show_default=True,
  required=False
  )
@click.option("--city", '-c', help="Cities names separated by ',' or ';'. "
              "A city name that contains more than an one word must be enclosed in brackets(\")", required=True)
@click.option("--token", '-t', help="The weatherstack.com user API Token ", required=True)
def cli(temperature, city, token):
    cities = city.replace(';', ',').split(',')
    for_supplied_cities = [city_exists for city_exists in cities if city_exists]
    in_temperature_unit = temperature
    using_api_token = token
    print_city_weather(for_supplied_cities, in_temperature_unit, using_api_token)


def print_city_weather(cities, temperature, token):
    temperature_unit = "m" if temperature == 'Celsius' else "f"
    for city in cities:
        url = f"http://api.weatherstack.com/current?access_key={token}&query={city}&units={temperature_unit}"
        json_out = get(url).json()
        if 'request' not in json_out:
            if json_out["error"]["type"] == "invalid_access_key":
                msg = f"\nERROR: The api key is invalid"
                print(msg)
                exit(101)
            if json_out["error"]["type"] == "request_failed":
                msg = f"ERROR: The {city} city does'nt exists, please fix or try another city name instead\n"
                print(msg)
                exit(101)
            else:
                msg = f"\nERROR: Site Api request failed"
                print(msg)
                exit(615)
        print(f"The weather in {json_out['request']['query']} today {json_out["current"]["temperature"]} \
{temperature}")


if __name__ == '__main__':
    cli()
