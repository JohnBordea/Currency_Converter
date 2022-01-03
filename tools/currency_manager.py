import requests
import xml.etree.ElementTree as ET

class Converter:
    exchange_rate = None
    curency_name = None
    url = 'https://www.bnr.ro/nbrfxrates.xml'
    from_currency = ''
    to_currency = ''
    value_from = 0
    value_to = 0

    def __init__(self):
        try:
            response = requests.get(self.url)
            root = ET.ElementTree( ET.fromstring( response.content ) ).getroot()

            currency = [ (root[1][1].text, 1) ]
            for rate in root[1][2]:
                if 'multiplier' in rate.attrib:
                    currency.append( ( rate.attrib['currency'], (float(rate.text) / float(rate.attrib['multiplier'])) ) )
                else:
                    currency.append( ( rate.attrib['currency'], float(rate.text) ) )

            self.exchange_rate = dict(currency)
            self.save_exchange_rate()
        except (requests.ConnectionError, requests.Timeout) as exception:
            self.read_offline_exchange_rate()

        self.from_currency = list(self.exchange_rate.keys())[0]
        self.to_currency = list(self.exchange_rate.keys())[1]

        self.set_name_for_currency()

    def save_exchange_rate(self):
        w = open("data/exchange_rate.info", "w")

        for rate in self.exchange_rate:
            w.write(f"{rate}={self.exchange_rate[rate]}")
            if not rate == list( self.exchange_rate.keys() )[-1]:
                w.write('\n')

        w.close()

    def read_offline_exchange_rate(self):
        f = open('data/exchange_rate.info', 'r')
        currency = []
        for text in f:
            if not text == '':
                element = text.split('=')
                currency.append( (element[0], float(element[1]) ) )

        f.close()
        self.exchange_rate = dict(currency)

    def set_name_for_currency(self):
        f = open('data/dictionary.info', mode='r', encoding="utf-8")
        currency = []
        for text in f:
            if not text == '':
                element = text.split('=')
                currency.append( (element[1].strip('\n'), element[0] ) )

        f.close()
        self.curency_name = dict(currency)

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