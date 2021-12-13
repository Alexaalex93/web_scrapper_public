# -*- coding: utf-8 -*-
"""
Created on Thu May 27 12:35:24 2021

@author: alexf
"""

import pytest
from src.body_request import BodyRequest

from src.customized_requests.aussar_requests import AussarRequests
from src.customized_requests.coolmod_requests import CoolmodRequests
from src.customized_requests.pccomponentes_requests import PccomponentesRequests
from src.customized_requests.vsgamers_requests import VsGamersRequests

import pandas as pd

@pytest.mark.parametrize("expected",[
    {'item':'graphic_card',
                'brand':'nvidia',
                'model':'3080',
                'store':'aussar',
                'items':[]}
    ])


def test_aussar_graphic_response(input_format, expected):
    AussarRequests.graphic_card_request(parsed_html='', model='3080')

def test_get_mars_format_from_months(input_format, expected):
    configuration = { "week-first-day": "sun",
                      "periodicity": "MTH",
                      "iso":"en"}
    formatter = PeriodFormatter(pd.DataFrame(), configuration, 'PER_TAG')

    actual = formatter.get_mars_format_from_months(str.lower(input_format))
    assert expected == actual

@pytest.mark.parametrize("input_format, expected",[
    ("Y2019", "20191231"),
    ("Y2020", "20201231"),
    ("Y2040", "20401231"),
    ("Y2010", "20101231"),
    ("Y1990", "19901231")])

def test_get_mars_format_from_years(input_format, expected):
    configuration = { "week-first-day": "sun",
                      "periodicity": "YRLY",
                      "iso":"en"}

    formatter = PeriodFormatter(pd.DataFrame(), configuration, 'PER_TAG')

    actual = formatter.get_mars_format_from_years(str.lower(input_format))
    assert expected == actual

@pytest.mark.parametrize("input_format, week_first_day, expected",[
    ("W2018037", "sun", "20180915"),
    ("W2018039", "sun", "20180929"),
    ("W2020011", "sun", "20200314"),
    ("W2018052", "sun", "20181229"),
    ("W2019036", "tue", "20190909"),
    ("W2019036", "fri", "20190905"),
    ("W2020001", "mon", "20200105"),
    ("W2018001", "sun", "20180106"),
    ("W2018021", "sun", "20180526")])

def test_get_mars_format_from_weeks(input_format, week_first_day, expected):
    configuration = {"periodicity": "WKY"}
    configuration['week-first-day'] = week_first_day
    configuration['iso'] = 'en'

    formatter = PeriodFormatter(pd.DataFrame(), configuration, 'PER_TAG')

    actual = formatter.get_mars_format_from_weeks(str.lower(input_format))
    assert expected == actual