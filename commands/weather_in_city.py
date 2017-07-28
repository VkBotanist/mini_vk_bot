#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Maia'


def get_weather(city):
    """
    Функция возвращает описание погоды указанного населенный пункт.

    """

    url = "https://query.yahooapis.com/v1/public/yql?q=select item from weather.forecast where woeid in " \
          "(select woeid from geo.places(1) where text='{city}') and u='c'" \
          "&format=json&diagnostics=true".format(city=city)

    import requests
    rs = requests.get(url)

    query = rs.json().get('query')

    # Если query = None или query['results'] = None
    if not query or not query['results']:
        return "Не найден населенный пункт"

    item = query['results']['channel']['item']
    condition = item['condition']

    text = condition['text']
    temp = condition['temp']

    return 'Текущая погода в "{}": {} °C, {}'.format(city, temp, text)


if __name__ == '__main__':
    city = "Магнитогорск"
    print(get_weather(city))

    city = "[etcjcbyf"
    print(get_weather(city))

    city = ""
    print(get_weather(city))


# import requests
#
# def weather()
# CODE_WEATHER_BY_DESCRIPTION = {
#     '0': 'Торнадо',
#     '31': 'Ясно (ночь)'
#
# }
#
#
# if __name__ == '__main__':
#     city = "Магнитогорск"
#     url = "https://query.yahooapis.com/v1/public/yql?q=select item from weather.forecast where woeid in " \
#           "(select woeid from geo.places(1) where text='{city}') and u='c'" \
#           "&format=json&diagnostics=true".format(city=city)
#     print(url)
#
#     rs = requests.get(url)
#     item = rs.json()['query']['results']['channel']['item']
#     condition = item['condition']
#     code = condition['code']
#     print(code)
#
#     weather_description = ''
#     if code in CODE_WEATHER_BY_DESCRIPTION:
#         weather_description = CODE_WEATHER_BY_DESCRIPTION[code]
#     else:
#         print("Не удалось получить состояние погоды")
#
#     print('Current: {temp} °C, {text}'.format(**condition))
#     print()
#
