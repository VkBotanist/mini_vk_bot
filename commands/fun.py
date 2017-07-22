#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_random_quotes_list():
    quotes = list()

    import requests
    rs = requests.get('http://bash.im/random')

    from lxml import etree
    root = etree.HTML(rs.content)

    for quote_el in root.xpath('//*[@class="quote"]'):
        try:
            text_el = quote_el.xpath('*[@class="text"]')[0]
            quote_text = '\n'.join(text.encode('ISO8859-1').decode('cp1251') for text in text_el.itertext())

            quotes.append(quote_text)

        except IndexError:
            pass

    return quotes


# Хранилище цитат башорга, из которого будут браться цитаты
# Когда этот список будет пустым, оно будет заполнено с сайта.
QUOTES_LIST = list()


def get_random_quote():
    global QUOTES_LIST

    # Если пустой, запрос и заполняем список новыми цитатами
    if not QUOTES_LIST:
        QUOTES_LIST += get_random_quotes_list()

    # Перемешиваем список цитат и берем последний элемент
    import random
    random.shuffle(QUOTES_LIST)

    # Удаление и возврат последнего элемента из списка
    return QUOTES_LIST.pop()
