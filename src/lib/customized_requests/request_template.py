# -*- coding: utf-8 -*-
"""
Created on Thu May 20 18:20:21 2021

@author: alexf
"""
from abc import ABC, abstractmethod

class RequestTemplate(ABC):
    @abstractmethod
    def nvidia_graphic_card_request(self):
        pass

    @abstractmethod
    def call_right_function(self, brand: str, item: str, **kwargs):
        pass