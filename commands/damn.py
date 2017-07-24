#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def damn(name):
    url = 'https://damn.ru/?sex=&name=' + name

    import requests
    rs = requests.get(url)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    damn_item = root.select_one('div.damn')
    if not damn_item:
        return

    return damn_item.text


if __name__ == '__main__':
    print(damn('   '))
    print(damn(' Иван'))
