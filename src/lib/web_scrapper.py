# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 15:26:05 2020

@author: Alex
"""
import random
import json
import time
import threading
from lib.body_request import BodyRequest
from lib.send_message import SendMessage
from lib.auto_buy import AutoBuy


class WebScrapper():
    def __init__(self, **kwargs):#, item, brand, models, request_configuration_json_path, token_id_configuration_json_path, card_number, expiration_date, owner, secret_code):

        self.latest_status = {}
        self.current_status = {}

        self.b_request = BodyRequest(request_configuration_json_path=kwargs['request_configuration_json_path'], token_id_configuration_json_path=kwargs['token_id_configuration_json_path'])
        self.send_message = SendMessage(kwargs['token_id_configuration_json_path'])
        self.autobuy = AutoBuy(token_id_configuration_json_path=kwargs['token_id_configuration_json_path'], card_number=kwargs['card_number'], expiration_date=kwargs['expiration_date'], owner=kwargs['owner'], secret_code=kwargs['secret_code'])

        with open(kwargs['request_configuration_json_path']) as file:
            self.items_information = json.load(file)

        with open('../configuration/request_type_store.json') as file:
            self.request_type_store = json.load(file)

        self.item = kwargs['item']
        self.brand = kwargs['brand']

        if kwargs['models']:
            all_keys = list(self.items_information[self.item][self.brand].keys())
            keys_to_delete = list(set(all_keys) - set(kwargs['models']))
            self.items_information = self.items_information[self.item][self.brand]
            for to_delete in keys_to_delete:
                self.items_information.pop(to_delete)
        else:
            self.items_information = self.items_information[self.item][self.brand]
        if not  kwargs['card_number'] or not kwargs['expiration_date'] or not kwargs['owner'] or not kwargs['secret_code']:
            for key in self.items_information.keys():
                self.items_information[key]['autobuy'] = False
        self.models = list(self.items_information.keys())
        self.len_models = len(self.items_information.keys())
    def check_latest_status(self, model):
        try:
            if model in self.latest_status.keys() and model in self.current_status.keys(): #Solo si existe esa key en los ultimos estados
                current_status_stores = set(list(self.current_status[model].keys()))
                latest_status_stores = set(list(self.latest_status[model].keys()))

                if (current_status_stores - latest_status_stores) or (latest_status_stores - current_status_stores): #Si cambian las tiendas, envio mensaje
                    self.latest_status[model] = self.current_status[model]
                    self.current_status.pop(model)
                    return True
                else:
                    for store in self.current_status[model]:
                        current_status_names = set(item['name'] for item in self.current_status[model][store])
                        latest_status_names = set(item['name'] for item in self.latest_status[model][store])
                        if (current_status_names - latest_status_names) or (latest_status_names - current_status_names): #Si cambia cualquier elemento dentro de una tienda. Envio mensaje
                            self.latest_status[model] = self.current_status[model] #NO COMPRUEBO UNO POR UNO, CON QUE UNO CAMBIE, ME VALE. ENVIO MENSAJE. MIRAR SI ES MEJOR COMPROBAR UNO POR UNO
                            self.current_status.pop(model)
                            return True

            if not model in self.latest_status.keys() and model in self.current_status.keys():#Si no existe esa key pero en los actuales hay algo de informacion
                self.latest_status[model] = self.current_status[model] #NO COMPRUEBO UNO POR UNO, CON QUE UNO CAMBIE, ME VALE. ENVIO MENSAJE. MIRAR SI ES MEJOR COMPROBAR UNO POR UNO
                self.current_status.pop(model)
                return True
            if model in self.latest_status.keys():
                if not model in self.current_status.keys():
                    self.latest_status.pop(model)
                return False
            return False
        except Exception as exc:
            self.to_log_bot('ERROR', f'Class: WebScrapper, Function: check_latest_status(), Error:{str(exc)} for model {model}')

    #CAMBIAR FUNCION DE COMPRAR
    def get_updates(self, **kwargs):

        current_status = {}
        for store_url in kwargs['items_information']['store_urls']:
            if not kwargs['model'] in self.latest_status.keys():
                latest_status = {}
            elif not store_url['store'] in self.latest_status[kwargs['model']].keys():
                latest_status = {}
            else:
                latest_status = self.latest_status[kwargs['model']][store_url['store']]

            available_items = self.b_request.call_right_function(request_type = self.request_type_store[store_url['store']], brand = self.brand, item=self.item,
                                                     store=store_url['store'], model=kwargs['model'], url=store_url['url'], latest_status = latest_status)
            if available_items:
                current_status[store_url['store']] = available_items
                if kwargs['items_information']['autobuy']:
                    self.autobuy.buy_item_ldlc(store_url['url'], kwargs['items_information']['target_channel'])
                    self.send_message.to_telegram_channel(model = kwargs['model'], send_to_channel = kwargs['items_information']['send_to_channel'], channel = kwargs['items_information']['target_channel'], items={store_url['store']:available_items}) #Repensar la logica para comprar
                    if kwargs['items_information']['buy_once']:
                        kwargs['items_information']['autobuy'] = False
        if current_status:
            self.current_status[kwargs['model']] = current_status

        if self.check_latest_status(kwargs['model']):
            self.send_message.to_telegram_channel(model = kwargs['model'], send_to_channel = kwargs['items_information']['send_to_channel'],  channel = kwargs['items_information']['target_channel'], items=self.latest_status[kwargs['model']])


    def run(self, model):
        while True:
            chosen_time = random.randint(15, 30)
            self.send_message.to_log_bot('INFO', f'Random time {chosen_time} chosen for model {model}')
            time.sleep(chosen_time)
            self.get_updates(model = model, items_information = self.items_information[model])

    def parallel_run(self):
        threads = []
        for i in range(self.len_models):
            t = threading.Thread(target=self.run, args=(self.models[i],))
            threads.append(t)
            t.start()