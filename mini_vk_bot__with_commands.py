#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: обрабатывать не последнее полученное сообщение, а пачку, например 100

from config import LOGIN, PASSWORD


if __name__ == '__main__':
    import vk_api
    vk = vk_api.VkApi(login=LOGIN, password=PASSWORD)
    vk.auth()

    command_prefix = 'Бот, '

    all_commands = {
        'насмеши': 'Случайная цитата башорга',
        'ругнись': 'Ругательство с матогенератора',
        'погода': 'Погода в указанном городе. Например: "Бот, погода магнитогорск"',
        'что посмотреть': 'Рандомная ссылка на кинопоиск',
        'котики': ':3',
        'команды': 'Показать список команд',
    }

    # Ограничение бота, чтобы он не отвечал на свои же сообщения
    # Для снятие ограничения: bot_user_id = None
    rs = vk.method('users.get')
    bot_user_id = rs[0]['id']

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

            # Не будем отвечать на собственное сообщение
            if from_user_id == bot_user_id:
                continue

            # Бот реагирует только на сообщения, начинающиеся с префикса
            if not message.lower().startswith(command_prefix.lower()):
                continue

            print('    From user #{}, message (#{}): "{}"'.format(from_user_id, message_id, message))
            command = message[len(command_prefix):]

            message = ''

            if command.lower() not in all_commands:
                message = 'Получена неизвестная команда "{}".\n' \
                          'Чтобы узнать команды введи: "Бот, команды"'.format(command)

            else:
                command = command.lower()

                # TODO: для каждой команды отдельный поток создавать

                if command == 'команды':
                    message = '\n'.join('{}: {}'.format(k, v) for k, v in all_commands.items())

                all_commands = {
                    'насмеши': 'Случайная цитата башорга',
                    'ругнись': 'Ругательство с матогенератора',
                    'погода': 'Погода в указанном городе. Например: "Бот, погода магнитогорск"',
                    'что посмотреть': 'Рандомная ссылка на кинопоиск',
                    'котики': ':3',
                    'команды': 'Показать список команд',
                }

            if not message:
                message = 'Не получилось выполнить команду "{}" :( Попробуй позже повторить :)'.format(command)

            last_message_bot_id = vk.method('messages.send', {'user_id': from_user_id, 'message': message})
            messages_get_values['last_message_id'] = last_message_bot_id

        except Exception as e:
            import traceback
            print('Error:', traceback.format_exc())

        finally:
            import time
            time.sleep(3)
