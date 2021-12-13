# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 01:18:58 2021

@author: alexf
"""
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import re
import platform
from random_user_agent.user_agent import UserAgent

from lib.send_message import SendMessage

class DynURL:
    def __init__(self, **kwargs):
        self.new_urls = {}


        self.send_message = SendMessage(kwargs['token_id_configuration_json_path'])
        self.user_agent_rotator = UserAgent()
        user_agent = self.user_agent_rotator.get_random_user_agent()

        self.options = Options()
        self.options.page_load_strategy = 'eager'
        self.options.headless = True

        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("general.useragent.override", user_agent)
        '''
        self.profile.set_preference('network.proxy.type', 1)
        self.profile.set_preference('network.proxy.http', 'fr.proxymesh.com')
        self.profile.set_preference('network.proxy.http_port', 31280)
        self.profile.set_preference('network.proxy.share_proxy_settings', True)
        '''

        if platform.system() == 'Windows':
            self.browser =  webdriver.Firefox(executable_path='C:/src/web_scrapper/configuration/drivers/geckodriver.exe', options=self.options, firefox_profile=self.profile)
        elif platform.system() == 'Linux':
            self.browser =  webdriver.Firefox(options=self.options, firefox_profile=self.profile)

    def get_new_browser(self):
        try:
            self.browser.close()
            self.send_message.to_log_bot('INFO', 'Class: DynURL, Function: get_new_browser(), driver successfully closed.')
        except Exception:
            self.send_message.to_log_bot('INFO', 'Class: DynURL, Function: get_new_browser(), driver already closed.')

        user_agent = self.user_agent_rotator.get_random_user_agent()
        self.profile.set_preference("general.useragent.override", user_agent)

        if platform.system() == 'Windows':
            self.browser =  webdriver.Firefox(executable_path='C:/src/web_scrapper/configuration/drivers/geckodriver.exe', options=self.options, firefox_profile=self.profile)
        elif platform.system() == 'Linux':
            self.browser =  webdriver.Firefox(options=self.options, firefox_profile=self.profile)

    def get_url(self):
        try:
            nvidia_url = 'https://shop.nvidia.com/es-es/geforce/store/?page=1&limit=9&locale=es-es&manufacturer=NVIDIA&manufacturer_filter=NVIDIA~6,ACER~4,ASUS~44,EVGA~6,GAINWARD~1,GIGABYTE~29,HP~14,LENOVO~2,MSI~45,PNY~8,ZOTAC~13'

            self.browser.get(nvidia_url)

            # Retrieve page source
            soup = BeautifulSoup(self.browser.page_source, 'lxml')
            if "Access Denied" in str(soup):
                self.send_message.to_log_bot('WARNING', 'Class: DynURL, Function: get_url(), Error: ACCESS DENIED')

            raw_html = soup.find_all(class_= 'buy')

            equivalences = {'NVGFT090':'3090', 'NVGFT080':'3080','NVGFT080T':'3080ti','NVGFT070':'3070','NVGFT070T':'3070ti','NVGFT060':'3060','NVGFT060T':'3060ti'}
            for r in raw_html:
                if  re.findall(r"https:\/\/www\.ldlc.+\.html",str(r)) and re.findall(r'NVGFT0.0T?',str(r)):
                    self.new_urls[equivalences[list(set(re.findall(r'NVGFT0.0T?',str(r))))[0]]] = re.findall(r"https:\/\/www\.ldlc.+\.html",str(r))[0]
            self.send_message.to_log_bot('INFO', f'Class: DynURL, Function: get_url(), Recogidas {list(self.new_urls.keys())}')
            self.get_new_browser()

        except Exception as exc:
            self.send_message.to_log_bot('ERROR', f'Class: DynURL, Function: get_url(), Error:{str(exc)}')
            self.get_new_browser()