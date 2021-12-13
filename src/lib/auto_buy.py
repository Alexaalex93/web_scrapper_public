# -*- coding: utf-8 -*-
"""
Created on Sun May 30 16:14:57 2021

@author: alexf
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import platform

from lib.send_message import SendMessage


class AutoBuy():
    def __init__(self, **kwargs):
        self.send_message = SendMessage(kwargs['token_id_configuration_json_path'])
        self.card_number = kwargs['card_number']
        self.expiration_date = kwargs['expiration_date']
        self.owner = kwargs['owner']
        self.secret_code = kwargs['secret_code']

    def check_buy_button_displayed(self, browser):

        try:
            buy_button = browser.find_elements_by_xpath('//*[@id="product-page-price"]/div[2]/a[2]')
            if len(buy_button) == 0:
                return False
            else:
                buy_button = buy_button[0]
                if buy_button.is_displayed():
                    return True
                else:
                    return False
        except Exception as exc:
            self.send_message.to_log_bot('ERROR', f'Class: AutoBuy, Function: check_buy_button_displayed(), Error:{str(exc)}')

    def check_close_button_displayed(self, browser):

        try:
            close_button = browser.find_elements_by_xpath('/html/body/div[8]/div/div/button/span')
            if len(close_button) == 0:
                return False
            else:
                close_button = close_button[0]
                if close_button.is_displayed():
                    return True
                else:
                    return False
        except Exception as exc:
            self.send_message.to_log_bot('ERROR', f'Class: AutoBuy, Function: check_close_button_displayed(), Error:{str(exc)}')

    def click_buy_now(self, browser, url):

        try:
            current_url = browser.current_url
            while url not in  current_url or current_url not in  url:
                if self.check_buy_button_displayed(browser):
                    buy_button = browser.find_element_by_xpath('//*[@id="product-page-price"]/div[2]/a[2]')
                    buy_button.click()
                    current_url = browser.current_url
                if self.check_close_button_displayed(browser):
                    close_button = browser.find_element_by_xpath('/html/body/div[8]/div/div/button/span')
                    close_button.click()
                browser.implicitly_wait(2)
                browser.refresh()

        except Exception as exc:
            self.send_message.to_log_bot('ERROR', f'Class: AutoBuy, Function: click_buy_now(), Error:{str(exc)}')



    def buy_item_ldlc(self, url, channel):
        try:

            PROXY = 'fr.proxymesh.com:31280'

            webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                "httpProxy": PROXY,
                "ftpProxy": PROXY,
                "sslProxy": PROXY,
                "proxyType": "MANUAL",
            }

            options = Options()
            options.page_load_strategy = 'eager'

            if platform.system() == 'Windows':
                browser =  webdriver.Firefox(executable_path='C:/src/web_scrapper/configuration/drivers/geckodriver.exe', options=options)
            elif platform.system() == 'Linux':
                browser =  webdriver.Firefox(options=options)

            browser.get(url)

            while not self.check_buy_button_displayed(browser):
                browser.implicitly_wait(2)
                browser.refresh()
            self.click_buy_now(browser, url)


            current_url = browser.current_url
            browser.find_element_by_xpath('//*[@id="Email"]').send_keys('alexfdezglez93@gmail.com')
            browser.find_element_by_xpath('//*[@id="Password"]').send_keys('Danale4147')
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, r'/html/body/div[3]/div/form/button')))
            login_button = browser.find_element_by_xpath('/html/body/div[3]/div/form/button')
            login_button.click()
            delivery_button = browser.find_element_by_xpath('//*[@id="deliveryModeClassicSelectionForm"]/div')
            delivery_button.click()


            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, r'//*[@id="form2"]/div[8]/div/button')))
            browser.find_element_by_xpath('//*[@id="ExpirationDate"]').send_keys(self.expiration_date)
            browser.find_element_by_xpath('//*[@id="CardNumber"]').send_keys(self.card_number)
            browser.find_element_by_xpath('//*[@id="OwnerName"]').send_keys(self.owner)
            browser.find_element_by_xpath('//*[@id="Cryptogram"]').send_keys(self.secret_code)
            current_url = browser.current_url
            pay_button = browser.find_element_by_xpath('//*[@id="form2"]/div[8]/div/button')
            pay_button.click()
            WebDriverWait(browser, 15).until(EC.url_changes(current_url))

            browser.close()


            self.send_message.plain_text(channel = channel, text='***COMPRADO***')
        except Exception as exc:
            self.send_message.to_log_bot('ERROR', f'Class: AutoBuy, Function: buy_item_ldlc(), Error:{str(exc)}')
            self.send_message.plain_text(channel = channel, text=f'COMPRAR!!! {url}')