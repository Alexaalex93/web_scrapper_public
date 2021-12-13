# -*- coding: utf-8 -*-
"""
Created on Thu May 20 16:28:11 2021

@author: alexf
"""
from lib.customized_requests.aussar_requests import AussarRequests
from lib.customized_requests.pccomponentes_requests import PccomponentesRequests
from lib.customized_requests.coolmod_requests import CoolmodRequests
from lib.customized_requests.vsgamers_requests import VsGamersRequests
from lib.customized_requests.ldlc_requests import LdlcRequests

from lib.send_message import SendMessage

import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class BodyRequest:
    def __init__(self, **kwargs):#token_id_configuration_json_path):
        self.stores = {'aussar': AussarRequests(), 'coolmod': CoolmodRequests(),
                       'pccomponentes': PccomponentesRequests(), 'vsgamers': VsGamersRequests(),
                       'ldlc':LdlcRequests()}

        self.user_agent_rotator = UserAgent()

        with open(kwargs['request_configuration_json_path']) as file:
            self.proxy = json.load(file)
        self.proxy = self.proxy['proxy']
        self.send_message = SendMessage(kwargs['token_id_configuration_json_path'])

    def default_request(self, **kwargs):
        try:
            user_agent = self.user_agent_rotator.get_random_user_agent()

            response = requests.get(kwargs['url'], headers={'User-Agent':user_agent, 'Connection': 'close'}, proxies=self.proxy)
            self.send_message.to_log_bot('INFO', f'{kwargs["store"]} {kwargs["model"]} Default Function Status Code: {response.status_code} [{response.reason}]')
            parsed_html = BeautifulSoup(response.text, features='lxml')

            return self.stores[kwargs['store']].call_right_function(brand = kwargs['brand'], item = kwargs['item'], model = kwargs['model'],
                                                                    parsed_html = parsed_html, status = response.reason, url=kwargs['url'])
        except Exception as exc:
            self.send_message.to_log_bot('ERROR', f'Class: BodyRequest, Function: default_request(), Error:{str(exc)} for model {kwargs["model"]}')
            self.send_message.to_log_bot('INFO', f'Retrieving latest status: {kwargs["latest_status"]}')
            return kwargs['latest_status']

    def rendered_request(self, **kwargs):
        try:
            PROXY = self.proxy['http'].replace('http://', '')
            webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                "httpProxy": PROXY,
                "ftpProxy": PROXY,
                "sslProxy": PROXY,
                "proxyType": "MANUAL",
            }

            options = Options()
            options.page_load_strategy = 'eager'

            browser =  webdriver.Firefox(executable_path='C:/src/web_scrapper/configuration/drivers/geckodriver.exe', options=options)
            browser.set_page_load_timeout(5)

            browser.get(kwargs['url'])
            self.send_message.to_log_bot('INFO', f'{kwargs["store"]} {kwargs["model"]} Rendered request')
            parsed_html = BeautifulSoup(browser.page_source, 'lxml')
            browser.close()
            return self.stores[kwargs['store']].call_right_function(brand = kwargs['brand'], item = kwargs['item'], model = kwargs['model'],
                                                                    parsed_html = parsed_html, status = 'OK', url=kwargs['url'])
        except Exception as exc:
            self.send_message.to_log_bot('ERROR', f'Class: BodyRequest, Function: rendered_request(), Error:{str(exc)} for model {kwargs["model"]}')
            self.send_message.to_log_bot('INFO', f'Retrieving latest status: {kwargs["latest_status"]}')
            return kwargs['latest_status']

    def call_right_function(self, request_type: str, **kwargs):
        do = f'{request_type}_request'
        if hasattr(self, do) and callable(func := getattr(self, do)):
            return func(**kwargs)