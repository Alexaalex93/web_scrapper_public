# -*- coding: utf-8 -*-
"""
Created on Thu May 20 18:48:07 2021

@author: alexf
"""
from lib.customized_requests.request_template import RequestTemplate

class VsGamersRequests(RequestTemplate):

    def nvidia_graphic_card_request(self, **kwargs):

        raw_html = kwargs['parsed_html'].find_all(class_= 'vs-product-card')

        available_items = []
        for child in raw_html:
            if child.find(class_ = 'vs-product-card-title'):
                name = child.find(class_ = 'vs-product-card-title').get_text().strip()
                item = {}
                found = child.find('a')
                item['name'] = name
                item['price'] = child.find(class_ = 'vs-product-card-prices').get_text().strip()
                item['link'] = 'http://www.vsgamers.es' + found['href']
                item['store'] = 'Vs Gamers'

                available_items.append(item)

        return available_items


    def call_right_function(self, brand: str, item: str, **kwargs):
        do = f'{brand}_{item}_request'
        if hasattr(self, do) and callable(func := getattr(self, do)):
            func(**kwargs)