#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


ALL_COMMANDS = {
    'насмеши': 'Случайная цитата башорга',
    'ругнись': 'Ругательство с матогенератора',
    'погода': 'Погода в указанном городе. Например: "Бот, погода магнитогорск"',
    'что посмотреть': 'Рандомная ссылка на кинопоиск',
    'котики': ':3',
    'команды': 'Показать список команд',
}


def execute(command):
    # Если текущая команда не была найдена среди списка команд хотя бы по совпадению начальной строки
    if not any(command.lower().startswith(x) for x in ALL_COMMANDS):
        return 'Получена неизвестная команда "{}".\n' \
               'Чтобы узнать команды введи: "Бот, команды"'.format(command)

    else:
        command = command.lower()

        # TODO: для каждой команды отдельный поток создавать
        message = ''

        if command.startswith('команды'):
            message = '\n'.join('{}: {}'.format(k, v) for k, v in ALL_COMMANDS.items())

        elif command.startswith('насмеши'):
            from commands import fun
            message = fun.get_random_quote()

    return message
