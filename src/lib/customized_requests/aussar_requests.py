# -*- coding: utf-8 -*-
"""
Created on Thu May 20 18:43:49 2021

@author: alexf
"""
from lib.customized_requests.request_template import RequestTemplate

class AussarRequests(RequestTemplate):

    def nvidia_graphic_card_request(self, **kwargs):

        raw_html = kwargs['parsed_html'].find_all(class_= 'product-meta')

        available_items = []
        for child in raw_html:
            name =  child.find(class_ = 'h3 product-title').get_text().strip()
            if 'rtx' in name.lower():
                item = {}
                item['name'] = name
                item['price']  = child.find(class_ = 'price').get_text().strip()
                item['link'] = child.find('a')['href']
                item['store'] = 'Aussar'

                available_items.append(item)

        return available_items



    def call_right_function(self, brand: str, item: str, **kwargs):
        do = f'{brand}_{item}_request'
        if hasattr(self, do) and callable(func := getattr(self, do)):
            func(**kwargs)