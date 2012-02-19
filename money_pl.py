import urllib
import re
import sys

class MoneyClient:
    def get_price(self):
        raise NotImplementedYet
    def get_low_price(self):
        raise NotImplementedYet
    def get_high_price(self):
        raise NotImplementedYet
    def get_change(self):
        raise NotImplementedYet

class CommodityMoneyClient(MoneyClient):
    def __init__(self, url):
        self.url = url
        self.loaded = False
        self.price = .0
        self.low_price = .0
        self.high_price = .0
        self.change = .0
        
    def load_price(self, content):
        pattern = re.compile('<td class="ar"><b>(.*?)</b></td>', re.UNICODE)
        result = pattern.search(content)
        result = result.group(1)
        return float(result.replace(',', '.'))

    def load_min_price(self, content):
        pattern = re.compile('<td class="ar" >(.*?)</td>') 
        result = pattern.search(content)
        return float(result.group(1).replace(',', '.'))

    def load_max_price(self, content):
        pattern = re.compile('<td class="ar">([0-9,]+)</td>')
        result = pattern.search(content)
        return float(result.group(1).replace(',', '.'))

    def load_change(self, content):
        pattern = re.compile('<td class="ar"><span class="r_dn">([\-0-9,%]+)</span></td>')
        result = pattern.search(content)
        if not result:
            pattern = re.compile('<td class="ar"><span class="r_up">([\+0-9,%]+)</span></td>')
            result = pattern.search(content)
        return float(result.group(1).replace('%', '').replace(',', '.'))
        
    def load_content(self):
        if not self.loaded: 
            content = urllib.urlopen(self.url).read()
            prices = self.load_price(content)
            self.price = self.load_price(content)
            self.low_price = self.load_min_price(content)
            self.high_price = self.load_max_price(content)
            self.change = self.load_change(content)
            self.loaded = True
    
    def get_price(self):
        self.load_content()
        return self.price
    
    def get_low_price(self):
        self.load_content()
        return self.low_price
        
    def get_high_price(self):
        self.load_content()
        return self.high_price
        
    def get_change(self):
        self.load_content()
        return self.change

class CurrencyMoneyClient(MoneyClient):
    def __init__(self, url):
        self.url = url
        self.loaded = False
        self.price = .0
        self.low_price = .0
        self.high_price = .0
        self.change = .0
        
    def load_prices(self, content):
        p = re.compile('<td class="ar"><b>(.*?)</b></td>', re.UNICODE)
        return re.findall(p, content)

    def load_change(self, content):
        p = re.compile('<td class="ar (red|green)"><b>(.*?)</b></td>', re.UNICODE)
        change_result = re.findall(p, content)
        return float(change_result[0][1].replace('%', '').replace(',', '.'))
        
    def load_content(self):
        if not self.loaded:
            content = urllib.urlopen(self.url).read()
            prices = self.load_prices(content)
            self.price = float(prices[0].replace(',', '.'))
            self.low_price = float(prices[2].replace(',', '.'))
            self.high_price = float(prices[3].replace(',', '.')) 
            self.change = float(self.load_change(content))
            self.loaded = True
    
    def get_price(self):
        self.load_content()
        return self.price
    
    def get_low_price(self):
        self.load_content()
        return self.low_price
        
    def get_high_price(self):
        self.load_content()
        return self.high_price
        
    def get_change(self):
        self.load_content()
        return self.change


