#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


ALL_COMMANDS = {
    'насмеши': 'Случайная цитата башорга',
    'ругнись': 'Напиши кого бот отругает. Например: "Бот, ругнись петр иваныч"',
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
        # TODO: для каждой команды отдельный поток создавать
        message = ''

        # Приведение в нижний регистр чтобы проверка команды была регистронезависимой
        execute_command = command.lower()

        if execute_command.startswith('команды'):
            return '\n'.join('{}: {}'.format(k, v) for k, v in ALL_COMMANDS.items())

        elif execute_command.startswith('насмеши'):
            from commands import fun
            return fun.get_random_quote()

        elif execute_command.startswith('ругнись'):
            # Вытаскивание имени того, кого нужно обругать
            name = command[len('ругнись'):].strip()

            if not name:
                return 'Не удалось выполнить команду "ругнись": нужно указать имя.'

            from commands import damn
            return damn.damn(name)

    return message
