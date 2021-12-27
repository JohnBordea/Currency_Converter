import requests
import xml.etree.ElementTree as ET

class Converter:
    exchange_rate = {}
    url = 'https://www.bnr.ro/nbrfxrates.xml'
    from_currency = ''
    to_currency = ''

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
            self.save_for_offline_use()
        except (requests.ConnectionError, requests.Timeout) as exception:
            self.read_in_case_of_offline()

        self.from_currency = list(self.exchange_rate.keys())[0]
        self.to_currency = list(self.exchange_rate.keys())[1]

    def save_for_offline_use(self):
        w = open("data/exchange_rate.info", "w")

        for rate in self.exchange_rate:
            w.write(f"{rate}={self.exchange_rate[rate]}")
            if not rate == list( self.exchange_rate.keys() )[-1]:
                w.write('\n')

        w.close()

    def read_in_case_of_offline(self):
        f = open('data/exchange_rate.info', 'r')
        currency = []
        for text in f:
            if not text == '':
                element = text.split('=')
                currency.append( (element[0], float(element[1]) ) )

        f.close()
        self.exchange_rate = dict(currency)

    def change_from(self, index: str):
        if not self.from_currency == str and not self.to_currency == index:
            self.from_currency = index

    def change_to(self, index: str):
        if not self.from_currency == str and not self.to_currency == index:
            self.to_currency = index

    def __str__(self):
        st = '{\n'

        for rate in self.exchange_rate:
            st = f'{st}    "{rate}": {self.exchange_rate[rate]}'
            if not rate == list( self.exchange_rate.keys() )[-1]:
                st = f'{st},\n'
            else:
                st = f'{st}\n'

        st = st + '}'
        return st