#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: добавить команду курс валют
# TODO: добавить команду курс криптовалют
# TODO: поддержать опциональную команду график к командам курса валют, которая вернет картинку с графиком курса
#       диапазон курса выбрать опытным путем
ALL_COMMANDS = {
    'насмеши': 'Случайная цитата башорга',
    'ругнись': 'Напиши кого бот отругает. Например: "Бот, ругнись петр иваныч"',
    'погода': 'Погода в указанном городе. Например: "Бот, погода магнитогорск"',
    'что посмотреть': 'Рандомная ссылка на кинопоиск',
    'котики': ':3',
    'команды': 'Показать список команд',
}


def execute(command):
    # TODO: кроме результата команды лучше писать что за команда
    # Пример: Бот: результат выполнения команды: "погода магнитогорск"
    #         23 C, облачно
    #
    # Любой ответ от бота нужно начинать с "Бот: "
    
    # Если текущая команда не была найдена среди списка команд хотя бы по совпадению начальной строки
    if not any(command.lower().startswith(x) for x in ALL_COMMANDS):
        return 'Получена неизвестная команда "{}".\n' \
               'Чтобы узнать команды введи: "Бот, команды"'.format(command)

    else:
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
                name = 'Бот'

            from commands import damn
            return damn.damn(name)

    return message
