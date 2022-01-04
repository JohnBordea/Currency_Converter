from tkinter.constants import TRUE
import requests
import xml.etree.ElementTree as ET
import json
import datetime

class Converter:
    exchange_rate = None
    curency_name = None
    url = 'https://www.bnr.ro/nbrfxrates.xml'
    from_currency = ''
    to_currency = ''
    value_from = 0
    value_to = 0

    def __init__(self):
        self.read_offline_exchange_rate()
        if self.needed_update():
            try:
                response = requests.get(self.url)
                root = ET.ElementTree( ET.fromstring( response.content ) ).getroot()

                currency = [ (root[1][1].text, 1) ]
                for rate in root[1][2]:
                    if 'multiplier' in rate.attrib:
                        currency.append( ( rate.attrib['currency'], (float(rate.text) / float(rate.attrib['multiplier'])) ) )
                    else:
                        currency.append( ( rate.attrib['currency'], float(rate.text) ) )
                currency.append( ('last_update', root[0][1].text) )
                self.exchange_rate = dict(currency)
                self.save_exchange_rate()
            except (requests.ConnectionError, requests.Timeout) as exception:
                self.read_offline_exchange_rate()

        self.from_currency = list(self.exchange_rate.keys())[3]
        self.to_currency = list(self.exchange_rate.keys())[1]

        self.set_name_for_currency()

    def needed_update(self):
        last_updated = datetime.datetime.strptime(self.exchange_rate['last_update'], '%Y-%m-%d')
        current_time = datetime.datetime.now()

        need_update = False
        if current_time.year == last_updated.year and current_time.month == last_updated.month:
            if current_time.day == (last_updated.day + 1):
                if current_time.hour > 13:
                    need_update = True
            elif current_time.day > (last_updated.day + 1):
                need_update = True
        else:
            need_update = True

        return need_update

    def save_exchange_rate(self):
        with open("data/exchange_rate.info", "w") as w:
            w.write(json.dumps(self.exchange_rate))

    def read_offline_exchange_rate(self):
        f = open('data/exchange_rate.info', 'r')
        self.exchange_rate = json.load(f)
        f.close()

    def set_name_for_currency(self):
        f = open('data/dictionary.info', mode='r', encoding="utf-8")
        self.curency_name = json.load(f)
        f.close()

    def change_from(self, index: str):
        if index in list(self.exchange_rate.keys()):
            self.from_currency = index

    def change_to(self, index: str):
        if index in list(self.exchange_rate.keys()):
            self.to_currency = index

    def exchange(self, reverse=False):
        if reverse:
            self.value_to = round( round(self.exchange_rate[self.to_currency] / self.exchange_rate[self.from_currency], 4) * self.value_from , 4)
        else:
            self.value_to = round( round(self.exchange_rate[self.from_currency] / self.exchange_rate[self.to_currency], 4) * self.value_from , 4)
        if (self.value_to * (10 ** 4)) % (10 ** 4) == 0:
            self.value_to = int(self.value_to)

    def get_base_exchange_value(self, reverse=False):
        if reverse:
            base_exchange_value = round(self.exchange_rate[self.to_currency] / self.exchange_rate[self.from_currency], 4)
        else:
            base_exchange_value = round(self.exchange_rate[self.from_currency] / self.exchange_rate[self.to_currency], 4)

        if (base_exchange_value * (10 ** 4)) % (10 ** 4) == 0:
            base_exchange_value = int(base_exchange_value)

        return base_exchange_value

    def __str__(self) -> str:
        st = '{\n'

        for rate in self.exchange_rate:
            st = f'{st}    "{rate}": {self.exchange_rate[rate]}'
            if not rate == list( self.exchange_rate.keys() )[-1]:
                st = f'{st},\n'
            else:
                st = f'{st}\n'

        st = st + '}'
        return st