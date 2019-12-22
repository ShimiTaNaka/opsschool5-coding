from pathlib import Path
import argparse
from requests import get
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(add_help=True, usage="", description='''Getting city weather. ''')
parser.add_argument("city", type=str, nargs="+", help="Cities names separated by ',' ", )
opt_arg_flags = parser.add_mutually_exclusive_group()
opt_arg_flags.add_argument("-f", action="store_true", help="The Weather in Fahrenheit", required=False)
opt_arg_flags.add_argument("-c", action="store_true", help="The Weather in Celsius", required=False)
args = parser.parse_args()
for_supplied_cities = " ".join(map(str, args.city)).strip("'")


def get_api_key():
  api_key_file = "weather_api.key"
  api_key_filepath = Path(api_key_file)
  if not api_key_filepath.exists():
    msg = f"ERROR: file {api_key_file} doesn't exists - Need to create weatherstack.com user and add his api_key \
to {api_key_file} file"
    print(msg)
    exit(404)
  else:
    with open(api_key_file, "r") as key_file:
      try:
        key = key_file.read().strip()
        if key == '':
          msg = "The Api key file his empty"
          raise Exception("empty_api_key_file")
        return key
      except FileNotFoundError as fnfe:
        file_not_found_msg = f"ERROR: Could not find the {api_key_file} file, Create the file and add your api key.\n {fnfe}"
        print(file_not_found_msg)
        exit(404)
      except:
        print(f"ERROR: Something happened when opened the {api_key_file} file, {msg}")
        exit(101)


def print_city_weather(cities_name):
  api_key = get_api_key()
  temp_type = "f" if args.f else "m"
  cities = cities_name

  for city in cities.split(','):
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}&units={temp_type}"
    json_out = get(url).json()
    if 'request' not in json_out:
      if json_out["error"]["type"] == "invalid_access_key":
        msg = f"\nERROR: The api key file is corrupted"
        print(msg)
        exit(101)
      elif json_out["error"]["type"] == "request_failed":
        msg = f"\nERROR: The {city} city doesn't exists, please fix or try another city name instead"
        print(msg)
        print_random_city_weather()
        exit(101)
      else:
        msg = f"\nERROR: Site Api request error answer"
        print(msg)
        exit(615)
    temp = json_out["current"]["temperature"]
    print(f"The weather in {city} today {temp} {'Fahrenheit' if temp_type == 'f' else 'Celsius'}")


def print_random_city_weather():
  city_info = BeautifulSoup(get("https://randomcity.net/").text, features="html.parser").find("h1").string.split(",")
  city = city_info[0].strip(",").strip()
  city_n_country = ",".join(city_info).strip()
  print(f"For example getting the current weather in {city_n_country} with the next command\n"
        f"python3 {__file__} {city} [-c|-f]\n"
        f"will output the next line")
  print_city_weather(city)


if __name__ == '__main__':
  print_city_weather(for_supplied_cities)
