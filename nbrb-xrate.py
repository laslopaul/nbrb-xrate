#!/usr/bin/env python3

import requests
import json
from sys import argv

class CurrencyConv:
    def __init__(self):
        self.url = 'https://www.nbrb.by/api/exrates/rates?periodicity=0'
        r = requests.get(self.url)
        self.json_data = json.loads(r.text)
        self.xrates = {}
        for entry in self.json_data:
            curname = entry['Cur_Abbreviation']
            numeric = [] # temporary list for currency scale and rate
            numeric.append(entry['Cur_Scale']) 
            numeric.append(entry['Cur_OfficialRate'])
            self.xrates[curname] = numeric
        
    def get_currencies(self):
        """Print the list of available currencies"""
        currencies = list(self.xrates.keys())
        currencies.sort()
        currencies = ', '.join(currencies)
        print(f'Available currencies: {currencies}')
        
    def get_xrate(self, curname: str):
        """Print exchange rates for a specified currency"""
        if curname in self.xrates.keys():
            scale = self.xrates[curname][0]
            rate = self.xrates[curname][1]
            print(f'{scale} {curname} = {rate} BYN')
        else: print(f'ERROR! Invalid currency: {curname}')
    
    def to_byn(self, curname: str, amount: float):
        """Convert given foreign currency amount to BYN"""
        if curname in self.xrates.keys():
            scale = self.xrates[curname][0]
            rate = self.xrates[curname][1]
            result = (rate / scale) * amount
            print('%.2f %s = %.2f BYN' % (amount, curname, result))
        else: print(f'ERROR! Invalid currency: {curname}')

    def from_byn(self, curname: str, amount: float):
        """Convert BYN to foreign currency"""
        if curname in self.xrates.keys():
            scale = self.xrates[curname][0]
            rate = self.xrates[curname][1]
            result = amount / (rate / scale)
            print('%.2f BYN = %.2f %s' % (amount, result, curname))
        else: print(f'ERROR! Invalid currency: {curname}')            


converter = CurrencyConv()

def get_help
