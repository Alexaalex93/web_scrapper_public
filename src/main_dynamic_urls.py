# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 01:18:26 2021

@author: alexf
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 01:04:47 2021

@author: alexf
"""
from lib.web_scrapper import WebScrapper
from lib.nvidia_founders_dynamic_url import DynURL
import threading
import argparse
import time

def main(args):

    webscrapper = WebScrapper(item=args.item, brand=args.brand, models=args.models, request_configuration_json_path=args.request_configuration, token_id_configuration_json_path=args.token_id_configuration, card_number=args.card_number, expiration_date=args.expiration_date, owner=args.owner, secret_code=args.secret_code)

    dynamic_url = DynURL(token_id_configuration_json_path = args.token_id_configuration)

    t = threading.Thread(target=webscrapper.parallel_run)
    t.start()
    #webscrapper.parallel_run()
    while True:
        dynamic_url.get_url()
        for key in dynamic_url.new_urls.keys():
            webscrapper.items_information[key]['store_urls'][0]['url'] = dynamic_url.new_urls[key]
        time.sleep(5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Scrapper and autobuy script")
    parser.add_argument("-i", "--item", help = "Item you want to scrap from the configuration", required=True)
    parser.add_argument("-b", "--brand", help = "Brand you want to scrap from the configuration", required=True)
    parser.add_argument("-m", "--models", nargs="+", default=[])
    parser.add_argument("-rc", "--request_configuration", help = "Location of your request-configuration json", required=True)
    parser.add_argument("-tc", "--token_id_configuration", help = "Location of your token-id-configuration json", required=True)

    parser.add_argument("-c", "--card_number", help = "Number of your credit card", default='')
    parser.add_argument("-e", "--expiration_date", help = "Expiration date of your credit card", default='')
    parser.add_argument("-o", "--owner", help = "Owner of your credit card", default='')
    parser.add_argument("-s", "--secret_code", help = "Secret code of your credit card", default='')

    args = parser.parse_args()
    main(args)