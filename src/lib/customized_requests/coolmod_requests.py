# -*- coding: utf-8 -*-
"""
Created on Thu May 20 18:51:20 2021

@author: alexf
"""
from lib.customized_requests.request_template import RequestTemplate

class CoolmodRequests(RequestTemplate):

    def nvidia_graphic_card_request(self, **kwargs):

        raw_html = kwargs['parsed_html'].find_all(class_= 'product item-product')

        available_items = []
        for child in raw_html:
            if child.find(class_ = 'product-availability cat-product-availability'):
                if child.find(class_ = 'product-availability cat-product-availability').get_text().strip() != 'Sin Stock':
                    name =  child.find(class_ = 'product-name').get_text().strip()
                    if 'rtx' in name.lower():
                        item = {}
                        item['name'] = name
                        item['price']  = child.find(class_ = 'mod-featured-prices-container').get_text().strip()
                        item['link'] = 'https://www.coolmod.com' + child.find('a')['href']
                        item['store'] = 'Coolmod'

                        available_items.append(item)

        return available_items


    def call_right_function(self, brand: str, item: str, **kwargs):
        do = f'{brand}_{item}_request'
        if hasattr(self, do) and callable(func := getattr(self, do)):
            func(**kwargs)