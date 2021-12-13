# -*- coding: utf-8 -*-
"""
Created on Thu May 20 11:35:43 2021

@author: alexf
"""

from lib.web_scrapper import WebScrapper
import threading
import socket
from flask import Flask


#webscrapper = WebScrapper(item=args.item, brand=args.brand, models=args.models, request_configuration_json_path=args.request_configuration, token_id_configuration_json_path=args.token_id_configuration, card_number=args.card_number, expiration_date=args.expiration_date, owner=args.owner, secret_code=args.secret_code)
webscrapper = WebScrapper(item='graphic_card', brand='nvidia', models=[], request_configuration_json_path="C:/src/web_scrapper/configuration/request_configuration.json", token_id_configuration_json_path="C:/src/web_scrapper/configuration/token_id_configuration.json", card_number='', expiration_date='', owner='', secret_code='')
webscrapper.parallel_run()

local_ip = socket.gethostbyname(socket.gethostname())
local_port = ''
if local_ip == '192.168.1.37':
    local_port = '10'
if local_ip == '192.168.1.95':
    local_port = '1234'


t = threading.Thread(target=webscrapper.parallel_run)
t.start()


app = Flask(__name__)
@app.route("/")
def get_current_values():
    return str(webscrapper.latest_status)

@app.route("/fake_call")
def get_fake_values():
    return {'portatil':{'pccomponentes':[{'name':'Razer Blade 15 Base Model FHD Intel Core I7 10750H 16GB 512GB SSD RTX 3060 156', 'price':'1739€', 'link':'https://www.pccomponentes.com/razer-blade-15-base-model-fhd-intel-core-i7-10750h-16gb-512gb-ssd-rtx-3060-156', 'store':'PCCOMPONENTES'},{'name':'HP 15s Fq2004ns Intel Core I5 1135G7 8GB 512GB SSD 156', 'price':'619€', 'link':'https://www.pccomponentes.com/hp-15s-fq2004ns-intel-core-i5-1135g7-8gb-512gb-ssd-156', 'store':'PCCOMPONENTES'}], 'aussar':[{'name':'MACBOOK AIR APPLE 13 M1 8CORE GOLD 256GB MGND3Y/A', 'price':'1082,64 €', 'link':'https://www.aussar.es/equipos/macbook-air-apple-13-m1-8core-gold-256gb-mgnd3ya.html', 'store':'AUSSAR'}]},
'movil':{'coolmod':[{'name':'Apple iPhone 12 Pro Max 6.7" / 5G / 256GB / Libre / Azul Pacífico', 'price':'1403,95€', 'link':'https://www.coolmod.com/apple-iphone-12-pro-max-67-5g-256gb-libre-azul-pacafico-smartphone-mavil-precio', 'store':'COOLMOD'}], 'lifeinformatica':[{'name':'Xiaomi Redmi 9T 4/128GB Verde Oceánico Libre – Smartphone', 'price':'184,16 €', 'link':'https://lifeinformatica.com/tienda/xiaomi-redmi-9t-4-128gb-verde-oceanico-libre-smartphone/', 'store':'LIFEINFORMATICA'}]}}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=local_port)