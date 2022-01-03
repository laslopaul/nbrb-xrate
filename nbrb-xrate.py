#!/usr/bin/env python3

import json
from sys import argv

import requests


class CurrencyConv:
    def __init__(self):
        self.url = 'https://www.nbrb.by/api/exrates/rates?periodicity=0'
        r = requests.get(self.url)
        self.json_data = json.loads(r.text)
        self.xrates = {}
        for entry in self.json_data:
            curname = entry['Cur_Abbreviation']
            numeric = [entry['Cur_Scale'], entry['Cur_OfficialRate']]  # temporary list for currency scale and rate
            self.xrates[curname] = numeric

        self.currencies = sorted(list(self.xrates.keys()))

    def get_currencies(self):
        """Print the list of available currencies"""
        cur_list = ', '.join(self.currencies)
        print(f'Supported currencies: {cur_list}')

    def get_xrate(self, curname: str):
        """Print exchange rates for a specified currency"""
        if curname not in self.currencies:
            print(f'ERROR! Invalid currency: {curname}')
        else:
            scale = self.xrates[curname][0]
            rate = self.xrates[curname][1]
            print(f'{scale} {curname} = {rate} BYN')

    def to_byn(self, curname: str, amount: float):
        """Convert given foreign currency amount to BYN"""
        if curname not in self.currencies:
            print(f'ERROR! Invalid currency: {curname}')
        else:
            scale = self.xrates[curname][0]
            rate = self.xrates[curname][1]
            result = (rate / scale) * amount
            print('%.2f %s = %.2f BYN' % (amount, curname, result))

    def from_byn(self, curname: str, amount: float):
        """Convert BYN to foreign currency"""
        if curname in self.currencies:
            scale = self.xrates[curname][0]
            rate = self.xrates[curname][1]
            result = amount / (rate / scale)
            print('%.2f BYN = %.2f %s' % (amount, result, curname))
        elif curname == 'BYN':
            print('%.2f BYN = %.2f BYN' % (amount, amount))
        else:
            print(f'ERROR! Invalid currency: {curname}')


converter = CurrencyConv()


def get_help():
    print(f'Usage: {argv[0]} -r | -c <options>')
    print(
        f'\t-r [currency_codes]: Print exchange rates for specified currencies'
    )
    print('\t-c [amount] [input_currency] [resulting_currency]:', end=' ')
    print('Convert from BYN to foreign currency or vice versa.\n')
    converter.get_currencies()
    quit()


def main():
    # Processing command line arguments: no parameters specified
    if len(argv) == 1:
        get_help()

    # Processing command line arguments: get exchange rates
    elif argv[1] == '-r':
        if len(argv) > 2:
            for cur in argv[2:]:
                converter.get_xrate(cur)
        else:  # Getting all available rates
            for cur in converter.currencies:
                converter.get_xrate(cur)

    # Processing command line arguments: currency conversion
    elif argv[1] == '-c':
        try:
            float(argv[2])
        except ValueError:
            quit('Please, enter a correct amount')
        except IndexError:
            get_help()

        if argv[3] == 'BYN':
            try:
                converter.from_byn(argv[4], float(argv[2]))
            except IndexError:
                quit('Please, specify the resulting currency')
        elif argv[3] in converter.currencies and len(argv) == 4:
            converter.to_byn(argv[3], float(argv[2]))
        elif argv[3] in converter.currencies and argv[4] == 'BYN':
            converter.to_byn(argv[3], float(argv[2]))

        else:
            try:
                cpath = f'{argv[3]} -> {argv[4]}'
                print('Unsupported conversion path: ' + cpath)
            except IndexError:
                converter.to_byn(argv[3], float(argv[2]))

    # Processing command line arguments: other cases
    else:
        get_help()


if __name__ == "__main__":
    main()
