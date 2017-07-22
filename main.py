#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: print заменить на логер
# TODO: обрабатывать не последнее полученное сообщение, а пачку, например 100

from config import LOGIN, PASSWORD


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


if __name__ == '__main__':
    import vk_api
    vk = vk_api.VkApi(login=LOGIN, password=PASSWORD)
    vk.auth()

    command_prefix = 'Бот,'

    all_commands = {
        'насмеши': 'Случайная цитата башорга',
        'ругнись': 'Ругательство с матогенератора',
        'погода': 'Погода в указанном городе. Например: "Бот, погода магнитогорск"',
        'что посмотреть': 'Рандомная ссылка на кинопоиск',
        'котики': ':3',
        'команды': 'Показать список команд',
    }

    last_message_bot_id = None

    messages_get_values = {
        'out': 0,
        'count': 1,
        'time_offset': 60,
        'version': '5.67'
    }

    while True:
        try:
            rs = vk.method('messages.get', messages_get_values)
            # print(rs)

            # Если ничего не пришло
            if not rs['items']:
                continue

            message_id = rs['items'][0]['id']
            from_user_id = rs['items'][0]['user_id']
            message = rs['items'][0]['body']

            # Бот реагирует только на сообщения, начинающиеся с префикса
            if not message.lower().startswith(command_prefix.lower()):
                continue

            print('    From user #{}, message (#{}): "{}"'.format(from_user_id, message_id, message))
            command = message[len(command_prefix):].strip()

            message = ''

            # Если текущая команда не была найдена среди списка команд хотя бы по совпадению начальной строки
            if not any(command.lower().startswith(x) for x in all_commands):
                message = 'Получена неизвестная команда "{}".\n' \
                          'Чтобы узнать команды введи: "Бот, команды"'.format(command)

            else:
                command = command.lower()

                # TODO: для каждой команды отдельный поток создавать

                if command.startswith('команды'):
                    message = '\n'.join('{}: {}'.format(k, v) for k, v in all_commands.items())

                elif command.startswith('насмеши'):
                    message = get_random_quote()

            if not message:
                message = 'Не получилось выполнить команду "{}" :( Попробуй позже повторить :)'.format(command)

            print(message)

            last_message_bot_id = vk.method('messages.send', {'user_id': from_user_id, 'message': message})
            messages_get_values['last_message_id'] = last_message_bot_id

        except Exception as e:
            import traceback
            print('Error:', traceback.format_exc())

        finally:
            import time
            time.sleep(3)
