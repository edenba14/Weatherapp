import requests
import re
from translate import Translator as Trans


def get_weather(location, api_key):
    """
    this function receives a location uses api of visualcrossing to get the weather of  this location
    it returns a dictionary filtered with date, morning temp, night temp and humidity of seven days.
    :param location:
    :param api_key:
    :return: dictionary
    """
    location = translate_to_english(location)
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/next6days'
    params = {
        'key': api_key,
        'include': 'hours,days,datetime',
        'elements': 'rdatetime,datetime,humidity,tempmin,tempmax,temp',
        'unitGroup': 'metric',
        'lang': 'en'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        locations = {'location': location}
        forecast = [locations]
        for day in data['days']:
            morning_temp = -float('inf')
            night_temp = float('inf')

            # this will go over each day and find the min and max temp by the hours.
            for hour in day['hours']:
                hour_temp = hour['temp']
                if is_morning(hour['datetime']):
                    morning_temp = max(morning_temp, hour_temp)
                else:
                    night_temp = min(night_temp, hour_temp)

            weather_info = {
                'date': day['datetime'],
                'morning_temperature': morning_temp,
                'night_temperature': night_temp,
                'humidity': day['humidity']
            }
            forecast.append(weather_info)
        return forecast
    else:
        return None


def translate_to_english(addr):
    """
    this function receives a word and returns a translated word to english.
    :param addr:
    :return:
    """
    if re.search("^[a-zA-Z ,]*$", addr) is None:
        transl = Trans(to_lang="en", from_lang="autodetect")
        translate_name = transl.translate(addr)
        return translate_name
    return addr


def is_morning(datetime_str):
    """
    this function checks if it is morning by an hour range from 6:30 to 18:30
    :param datetime_str:
    :return:
    """
    hour = int(datetime_str.split(':')[0])
    minute = int(datetime_str.split(':')[1])
    if (hour == 6 and minute >= 30) or (6 < hour < 18) or (hour == 18 and minute <= 30):
        return True
    return False


