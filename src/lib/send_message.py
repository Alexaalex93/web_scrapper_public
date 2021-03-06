# -*- coding: utf-8 -*-
"""
Created on Fri May 28 15:39:00 2021

@author: alexf
"""
import json
import telegram
import time
from datetime import date

class SendMessage():

    def __init__(self, token_id_configuration_json_path):
        with open(token_id_configuration_json_path) as file:
            token_id_configuration = json.load(file)

        self.chat_id_logs = token_id_configuration['chat_id_logs']

        bot_token_channel = token_id_configuration['bot_token_channel']
        bot_token_logs = token_id_configuration['bot_token_logs']

        self.bot_channel = telegram.Bot(token=bot_token_channel)
        self.bot_logs = telegram.Bot(token=bot_token_logs)

    def to_log_bot(self, level, message):

        try:
           time.sleep(1)
           current_time = time.strftime("%H:%M:%S", time.localtime())
           today = date.today().strftime("%d-%m-%Y")
           if 'Status'in message and not '200'in message:
               level = 'WARNING'
           formatted_message = f'{today} {current_time} - {level} - {message}'
           self.bot_logs.send_message(chat_id=self.chat_id_logs, text=formatted_message, timeout=5)
           time.sleep(1)
        except Exception as exc:
           self.to_log_bot('ERROR', f'Class: SendMessage, Function: to_log_bot(), Error:{str(exc)}')
           print(str(exc))

    def plain_text(self, **kwargs):
        self.bot_channel.send_message(chat_id=kwargs['channel'], text=kwargs['text'], parse_mode=telegram.ParseMode.MARKDOWN, timeout=5)

    def to_telegram_channel(self, **kwargs):
        if kwargs['send_to_channel']:
            try:
                self.bot_channel.send_message(chat_id=kwargs['channel'], text="**CAMBIOS DETECTADOS**", parse_mode=telegram.ParseMode.MARKDOWN, timeout=5)
                time.sleep(0.5)

                for store in kwargs['items'].keys():
                    self.bot_channel.send_message(chat_id=kwargs['channel'], text=f'STORE: {store.upper()}', parse_mode=telegram.ParseMode.MARKDOWN, timeout=5)
                    time.sleep(0.5)
                    for item in kwargs['items'][store]:
                        markup = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(text='URL', url=item['link'])]])
                        text_message = f"*{item['name']}*\n{item['price']}\n{item['store']}"
                        self.bot_channel.send_message(chat_id=kwargs['channel'], text=text_message, parse_mode=telegram.ParseMode.MARKDOWN, timeout=5, reply_markup=markup)
                        time.sleep(0.5)
            except Exception as exc:
                self.to_log_bot('ERROR', f'Class: SendMessage, Function: to_telegram_channel(), Error:{str(exc)} for model {kwargs["model"]}')