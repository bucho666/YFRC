# -*- coding: utf-8 -*-

import urllib2
import webbrowser
from bs4 import BeautifulSoup

class WebPage(object):
    def __init__(self):
        self._soup = None

    def open(self, url):
        html = urllib2.urlopen(url) # TODO DEBUG
        self._soup = BeautifulSoup(html.read())
        return self

    def get_table(self, cols):
        return [line.find_all('td') for line in self._soup.find_all('tr')]

class Stock(object):
    (RANK, URL, MARKET, NAME, TIME,\
            PRICE, PARCENT, VALUE, VOLUME, BBS_URL) = range(10)

    ENCODE = 'utf-8'

    def __init__(self, cols):
        self._cols = cols

    def __str__(self):
        name = self._col(self.NAME)
        number = self.number()
        parcent = self._inside_col(self.PARCENT)
        return '[%s] %s %s%%' % (number, name, parcent)

    def _col(self, num):
        return self._cols[num].contents[0].encode(self.ENCODE)

    def number(self):
        return self._inside_col(self.URL)

    def _inside_col(self, num):
        return self._cols[num].contents[0].contents[0].encode(self.ENCODE)

class StockRanking(object):
    COLS = 10
    def __init__(self, stocks=[]):
        self._stocks = stocks

    def download(self, url):
        page = WebPage().open(url)
        table = page.get_table(self.COLS)
        self._stocks = [Stock(line) for line in table if len(line) == 10]
        return self

    def print_all(self):
        for stock in self._stocks: print stock

    def number_list(self):
        return [stock.number() for stock in self._stocks]

    def duplicate_ranking(self, ranking):
        number_list = ranking.number_list()
        list = [stock for stock in self._stocks if stock.number() in number_list]
        return StockRanking(list)

    def open_chart_pages(self):
        url = 'http://stocks.finance.yahoo.co.jp/stocks/chart/?code=%s.T&ct=z&t=2y&q=c&l=off&z=m&p=m65,m130,s&a=v'
        for stock in self._stocks:
            webbrowser.open(url % stock.number(), new=2)

if __name__ == '__main__':
    value_url = 'http://info.finance.yahoo.co.jp/ranking/?kd=1&tm=d&mk=1'
    volume_url = 'http://info.finance.yahoo.co.jp/ranking/?kd=33&mk=1&tm=d&vl=a'
    value = StockRanking().download(value_url)
    volume = StockRanking().download(volume_url)
    ranking = value.duplicate_ranking(volume)
    ranking.open_chart_pages()
