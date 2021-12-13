# -*- coding: utf-8 -*-
"""
Created on Fri May 28 18:27:57 2021

@author: alexf
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
options = webdriver.ChromeOptions()
options.headless = True

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get(')

html = driver.page_source



from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
# Requests library cannot return rendered javascript content, only the unmodified DOM (static web page). Use selenium and a web driver to automate a web browser and return rendered javascript content (dynamic web page). Initiate headless Firefox driver
options = Options()
options.headless = True

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
gpu3080ti = 'https://shop.nvidia.com/es-es/geforce/store/?page=1&limit=9&locale=es-es&manufacturer=NVIDIA&manufacturer_filter=NVIDIA~6,ACER~4,ASUS~44,EVGA~6,GAINWARD~1,GIGABYTE~29,HP~14,LENOVO~2,MSI~45,PNY~8,ZOTAC~13'

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get(gpu3080ti)

from bs4 import BeautifulSoup
import lxml
# Retrieve page source
soup = BeautifulSoup(driver.page_source, 'lxml')


import re
r1 = re.findall(r"https:\/\/www\.ldlc.+\.html",str(parsed_html))
a3090gpu = 'https://www.ldlc.com/es-es/ficha/PB32951877.html'
a3080gpu = 'https://www.ldlc.com/es-es/ficha/PB74583210.html'
a3070gpu = 'https://www.ldlc.com/es-es/ficha/PB84219657.html'
a3060tigpu = 'https://www.ldlc.com/es-es/ficha/PB45784578.html'
import requests
response = requests.get(gpu3080ti)

parsed_html = BeautifulSoup(response.text, features='lxml')
print(parsed_html)
a = parsed_html.find_all(class_= 'main p410')
print('Este producto ya no está disponible. Te redirigimos a la página de inicio' in parsed_html)
print(a)


import requests
from selenium.webdriver.support import expected_conditions as EC

response = requests.get(a3080gpu)
"para ver si esta disponible"
parsed_html = BeautifulSoup(response.text, features='lxml')
a = parsed_html.find_all(class_= 'main p410')
print(a.get_text().strip())
print('Este producto ya no está disponible. Te redirigimos a la página de inicio' in str(a))


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from src.send_message import SendMessage
send_message = SendMessage()
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.ldlc.com/es-es/ficha/PB00230960.html')
current_url = driver.current_url
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, r'//*[@id="cookieConsentAcceptButton"]')))
cookie_button = driver.find_element_by_xpath(r'//*[@id="cookieConsentAcceptButton"]')
cookie_button.click()

buy_button = driver.find_element_by_xpath('//*[@id="product-page-price"]/div[2]/a[2]')
buy_button.click()
WebDriverWait(driver, 15).until(EC.url_changes(current_url))
current_url = driver.current_url
driver.find_element_by_xpath('//*[@id="Email"]').send_keys('alexfdezglez93@gmail.com')
driver.find_element_by_xpath('//*[@id="Password"]').send_keys('Danale4147')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, r'/html/body/div[3]/div/form/button')))
login_button = driver.find_element_by_xpath('/html/body/div[3]/div/form/button')
login_button.click()
delivery_button = driver.find_element_by_xpath('//*[@id="deliveryModeClassicSelectionForm"]/div')
delivery_button.click()
card_number = ''
caducidad = ''
titular = ''
codigo = ''

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, r'//*[@id="form3"]/div/div')))
paypal_round_button = driver.find_element_by_xpath(r'//*[@id="form3"]/div/div')
paypal_round_button.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, r'//*[@id="form3"]/div[3]/div/button')))
pay_button = driver.find_element_by_xpath(r'//*[@id="form3"]/div[3]/div/button')
pay_button.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, r'//*[@id="btnNext"]')))
send_message


#driver.find_element_by_xpath('//*[@id="ExpirationDate"]').send_keys(caducidad)
#driver.find_element_by_xpath('//*[@id="CardNumber"]').send_keys(card_number)


#driver.find_element_by_xpath('//*[@id="OwnerName"]').send_keys(titular)

#driver.find_element_by_xpath('//*[@id="Cryptogram"]').send_keys(codigo)

pay_button = driver.find_element_by_xpath('//*[@id="form2"]/div[8]/div/button')
pay_button.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, r'//*[@id="form3"]/div[3]/div/button')))




response = requests.get('https://www.ldlc.com/es-es/ficha/PB00120013.html')

parsed_html = BeautifulSoup(response.text, features='lxml')
a = parsed_html.find_all(class_= 'saleBlock invisible')[0]
print(a.find(class_= 'price').get_text().strip())
print(a.get('data-product-price-vat-on'))
print(a.get_text().strip())
print('Este producto ya no está disponible. Te redirigimos a la página de inicio' in str(a))

a.find_all(class_= 'price')

parsed_html.select('h1.title-1')[0].text.strip()




from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()


nvidia = 'https://shop.nvidia.com/es-es/geforce/store/?page=1&limit=9&locale=es-es&manufacturer=NVIDIA&manufacturer_filter=NVIDIA~6,ACER~4,ASUS~44,EVGA~6,GAINWARD~1,GIGABYTE~29,HP~14,LENOVO~2,MSI~45,PNY~8,ZOTAC~13'

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get(gpu3080ti)

from bs4 import BeautifulSoup
import lxml
# Retrieve page source
soup = BeautifulSoup(driver.page_source, 'lxml')
r1 = re.findall(r"https:\/\/www\.ldlc.+\.html",str(soup))
driver.close()