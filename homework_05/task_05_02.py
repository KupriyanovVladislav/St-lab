import requests
import re


def get_weather():
    town_regex = r'<a.*?place-list__item-name.*?href="/pogoda(/.+?)".*?>([А-яё -]+?)</a>'
    temperature_regex = r'fact__temp.*?<span class=\"temp__value\">([−+])?(\d+)</span>'
    main_url = "https://yandex.by/pogoda/region"
    town_response = requests.get(main_url + '/149')
    result = dict()
    for town in re.findall(town_regex, town_response.text):
        temp_response = requests.get(main_url + town[0])
        match = re.findall(temperature_regex, temp_response.text)[0]
        if match[0]:
            town_temperature = int(match[1]) if match[0] == '+' else -int(match[1])
        else:
            town_temperature = int(match[1])
        result.update({town[1]: town_temperature})
    return result
