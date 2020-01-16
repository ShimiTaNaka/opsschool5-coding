import click
from requests import get


@click.command()
@click.option(
  '--temperature_unit', '-T',
  type=click.Choice(['Celsius', 'Fahrenheit'], case_sensitive=False),
  default='Celsius',
  help=("Weather temperature units type. "
        "Temperature unit options are Celsius or Fahrenheit"),
  show_default=True,
  required=False
  )
@click.option("--city", '-c', help="Cities names separated by ',' or ';'. "
              "A city name that contains more than an one word must be enclosed in brackets(\")", required=True)
@click.option("--api_token", '-t', help="The weatherstack.com user API Token ", required=True)
def cli(temperature_unit, city, api_token):
    for_supplied_cities = [not_empty_city_name for not_empty_city_name in city.replace(';', ',').split(',') if not_empty_city_name]
    print_city_weather(for_supplied_cities, temperature_unit, api_token)

def print_city_weather(cities, temperature_unit, token):
    temperature_unit_Acronyms = "m" if temperature_unit == 'Celsius' else "f"
    for city in cities:
        url = f"http://api.weatherstack.com/current?access_key={token}&query={city}&units={temperature_unit_Acronyms}"
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
        print(f"The weather in {json_out['request']['query']} today {json_out['current']['temperature']} {temperature_unit}")

if __name__ == '__main__':
    cli()