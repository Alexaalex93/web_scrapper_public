# -*- coding: utf-8 -*-
"""
Created on Sun May 30 12:27:43 2021

@author: alexf
"""
from lib.customized_requests.request_template import RequestTemplate

class LdlcRequests(RequestTemplate):

    def nvidia_founders_graphic_card_request(self, **kwargs):

        try:
            #raw_html = kwargs['parsed_html'].find_all(class_= 'main p410')
            if 'ok' in kwargs['status'].lower():
                #if 'Agotado' not in kwargs['parsed_html'].find(class_ = "website dispo-w100").get_text().strip():
                item = {}
                item['name'] = kwargs['parsed_html'].select('h1.title-1')[0].text.strip()
                item['price'] = kwargs['parsed_html'].find_all(class_= 'saleBlock invisible')[0].find(class_= 'price').get_text().strip()
                item['link'] = kwargs['url']
                item['store'] = 'LDLC'

                return [item]
                #else:
                    #return []
        except Exception:

            item = {}
            item['name'] = f'Founders Edition {kwargs["model"]}'
            item['price'] = "XXX"
            item['link'] = kwargs['url']
            item['store'] = 'LDLC'

            return [item]


    def nvidia_graphic_card_request(self, **kwargs):
        pass

    def call_right_function(self, brand: str, item: str, **kwargs):
        do = f'{brand}_{item}_request'
        if hasattr(self, do) and callable(func := getattr(self, do)):
            return func(**kwargs)