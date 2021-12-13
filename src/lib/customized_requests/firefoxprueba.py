# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 09:55:33 2021

@author: alexf
"""


from selenium import webdriver


from selenium import webdriver

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless=True
driver = webdriver.Firefox()


nvidia = 'https://shop.nvidia.com/es-es/geforce/store/?page=1&limit=9&locale=es-es&manufacturer=NVIDIA&manufacturer_filter=NVIDIA~6,ACER~4,ASUS~44,EVGA~6,GAINWARD~1,GIGABYTE~29,HP~14,LENOVO~2,MSI~45,PNY~8,ZOTAC~13'
binary = FirefoxBinary('/home/ubuntu/web_scrapper/configuration/drivers/arm/')
driver = webdriver.Firefox(executable_path='/home/ubuntu/web_scrapper/configuration/drivers/arm/geckodriver')

driver = webdriver.Firefox(firefox_binary=binary, options=options)
driver.get(str(nvidia))
from bs4 import BeautifulSoup
import lxml
import re
# Retrieve page source
soup = BeautifulSoup(driver.page_source, 'lxml')
r1 = re.findall(r"https:\/\/www\.ldlc.+\.html",str(soup))
driver.close()
print(r1)
'''
self.options = webdriver.ChromeOptions()
  self.options.page_load_strategy = 'eager'
  self.options.add_argument('--no-sandbox')  # required if root
  self.options.add_argument('--headless')
  self.options.add_argument('--disable-blink-features=AutomationControlled')
  self.options.add_argument('--disable-dev-shm-usage')
  self.options.add_argument(f'--user-agent="{user_agent}"')
  self.options.add_argument(f'--user-data-dir={self.selenium_path}')
  self.options.add_argument('--window-position=0,0')
  self.options.add_argument('--window-size=1920,1080')
'''