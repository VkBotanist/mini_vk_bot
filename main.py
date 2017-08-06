#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: обрабатывать не последнее полученное сообщение, а пачку, например 100
# TODO: логировать в файл
# TODO: В messages.get (https://vk.com/dev/messages.get) передавать параметр preview_length
#       чтобы запрашиваемые команды были ограничены

from config import LOGIN, PASSWORD


def get_logger(name):
    import logging
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(message)s')

    import sys
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    return log


log = get_logger('mini_vk_bot')


# Отлов необработанныз исключений и закрытие
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    log.error(text)
    quit()


import sys
sys.excepthook = log_uncaught_exceptions


import time


if __name__ == '__main__':
    import vk_api
    vk = vk_api.VkApi(login=LOGIN, password=PASSWORD)
    vk.auth()
    log.debug("Бот запущен")

    # BOT_USER_ID = vk.method('users.get')[0]['id']
    # time.sleep(0.3)

    # NOTE: для запроса сообщений
    # messages_get_values = {
    #     'out': 0,
    #     'count': 100,
    #     'version': '5.67'
    # }
    # rs = vk.method('messages.get', messages_get_values)
    # print(rs)
    # for i in sorted(rs['items'], key=lambda x: x['date']):
    #     print(i)
    #
    # quit()

    command_prefix = 'Бот,'

    messages_get_values = {
        'out': 0,
        'count': 1,
        'time_offset': 60,
        'version': '5.67'
    }

    messages_get_values__out = {
        'out': 1,
        'count': 1,
        'time_offset': 60,
        'version': '5.67'
    }

    def messages_get(out=0):
        if not out:
            rs = vk.method('messages.get', messages_get_values)
        else:
            rs = vk.method('messages.get', messages_get_values__out)
        # log.debug(rs)

        # Если ничего не пришло
        if not rs['items']:
            return

        item = rs['items'][0]
        message_id = item['id']
        from_user_id = item['user_id']
        message = item['body']

        # Если сообщение пришло из групповой беседы, в chat_id будет число, иначе None
        chat_id = item.get('chat_id')

        # Бот реагирует только на сообщения, начинающиеся с префикса
        if not message.lower().startswith(command_prefix.lower()):
            return

        if chat_id:
            log.debug('From chat #%s from user #%s, message (#%s): "%s"',
                      chat_id, from_user_id, message_id, message)
        else:
            log.debug('From user #%s, message (#%s): "%s"', from_user_id, message_id, message)

        command = message[len(command_prefix):].strip()

        # TODO: для каждой команды отдельный поток создавать
        # Пример: https://www.ibm.com/developerworks/ru/library/l-python_part_9/index.html#N10078
        # только поток нужно без демона использовать, демон указывает что при закрытии главного потока
        # должны и потоки-демоны завершиться, что для текущей задачи не будет правильным

        # Выполнение команды
        try:
            import commands
            message = commands.execute(command)

        except Exception as e:
            log.exception("Error:")

            import traceback
            message = 'При выполнении команды "{}" произошла ошибка: ' \
                      '"{}":\n\n{}'.format(command, e, traceback.format_exc())

        # Если ответа от бота нет
        if not message:
            message = 'Не получилось выполнить команду "{}" :( Попробуй позже повторить :)'.format(command)

        log.debug('Message: "%s"', message)

        messages_send_values = {
            'message': message,
            'version': '5.67'
        }

        # Если сообщение пришло из групповой беседы
        if chat_id:
            messages_send_values['chat_id'] = chat_id
        else:
            messages_send_values['user_id'] = from_user_id

        time.sleep(0.3)
        last_message_bot_id = vk.method('messages.send', messages_send_values)

        if not out:
            messages_get_values['last_message_id'] = last_message_bot_id
        else:
            messages_get_values__out['last_message_id'] = last_message_bot_id

    while True:
        try:
            messages_get()

            # TODO: временно, сделать красиво
            time.sleep(1)

            messages_get(out=1)


        except Exception as e:
            log.exception('Error:')

        finally:
            time.sleep(1)
