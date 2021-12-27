import requests
import xml.etree.ElementTree as ET

class Converter:
    exchange_rate = {}
    url = 'https://www.bnr.ro/nbrfxrates.xml'

    def __init__(self):
        response = requests.get(self.url)
        root = ET.ElementTree( ET.fromstring( response.content ) ).getroot()

        currency = []
        for rate in root[1][2]:
            if 'multiplier' in rate.attrib:
                currency.append( ( rate.attrib['currency'], (float(rate.text) / float(rate.attrib['multiplier'])) ) )
            else:
                currency.append( ( rate.attrib['currency'], float(rate.text) ) )

        self.exchange_rate = dict(currency)