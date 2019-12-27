from requests import get
import json


def get_temperature(base_url, access_key, city_name):
    uri = base_url + "?access_key="+access_key+"&query=" + city_name
    response = get(uri)
    temperature = response.json()["current"]["temperature"]
    return temperature


def main():
    base_url = "http://api.weatherstack.com/current"
    access_key = "0c47a9b2d09ac64b1cdf0e14c5d43f6a"
    city_name = "New York"
    temperature = get_temperature(base_url, access_key, city_name)
    print("Current temperature in {0} is: {1}°F".format(city_name, temperature))


if __name__ == '__main__':
    main()
