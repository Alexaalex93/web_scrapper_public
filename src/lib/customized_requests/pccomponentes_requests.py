# -*- coding: utf-8 -*-
"""
Created on Thu May 20 18:22:38 2021

@author: alexf
"""
from lib.customized_requests.request_template import RequestTemplate

class PccomponentesRequests(RequestTemplate):

    def nvidia_graphic_card_request(self, **kwargs):

        raw_html = kwargs['parsed_html'].find_all(class_= 'c-product-card__content')

        available_items = []
        for child in raw_html:
            if child.find(class_ = 'disponibilidad-inmediata') or child.find(class_ = 'disponibilidad-moderada'):
                name = child.find(class_ = 'c-product-card__header').get_text().strip()
                if 'rtx' in name.lower():
                    item = {}
                    item['name'] = name
                    item['price']  = child.find(class_ = 'c-product-card__prices').get_text().strip()
                    item['link'] = 'https://www.pccomponentes.com' + child.find('a')['href']
                    item['store'] = 'PCComponentes'

                    available_items.append(item)

        return available_items


    def call_right_function(self, brand: str, item: str, **kwargs):
        do = f'{brand}_{item}_request'
        if hasattr(self, do) and callable(func := getattr(self, do)):
            func(**kwargs)