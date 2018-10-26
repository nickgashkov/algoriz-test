import mpld3
import pandas as pd
import requests
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property

from algoriz.utils.libcalculator import algo_result

import matplotlib.pyplot as plt


class Algo(models.Model):
    name = models.CharField(verbose_name='Algo name', max_length=500)
    signal = models.CharField(verbose_name='Signal', max_length=500)
    ticker = models.CharField(verbose_name='Ticker', max_length=50)
    trade = models.CharField(verbose_name='Trade', max_length=500)

    positions = models.TextField(verbose_name='Positions', blank=True, null=True)
    pnl = models.TextField(verbose_name='PnLs', blank=True, null=True)

    NUMBER_JOINER = '|||'

    def get_absolute_url(self):
        return reverse('algo-detail', kwargs={'pk': self.pk})

    @cached_property
    def pnl_average(self):
        pnl = self.pnl.split(self.NUMBER_JOINER)

        pnl = map(float, pnl)
        pnl = list(pnl)

        pnl_average = sum(pnl) / len(pnl)

        return pnl_average

    @cached_property
    def pnl_plot(self):
        pnl = self.pnl.split(self.NUMBER_JOINER)

        pnl = map(float, pnl)
        pnl = list(pnl)

        fig, ax = plt.subplots()

        indata = pd.Series(pnl)
        indata.plot(ax=ax)

        return mpld3.fig_to_html(fig)

    @cached_property
    def positions_plot(self):
        positions = self.positions.split(self.NUMBER_JOINER)

        positions = map(float, positions)
        positions = list(positions)

        fig, ax = plt.subplots()

        indata = pd.Series(positions)
        indata.plot(ax=ax)

        return mpld3.fig_to_html(fig)

    def update_algo_result(self):
        prices = self.fetch_prices()
        pnl, positions = algo_result(self.signal, self.trade, prices)

        self.positions = self.NUMBER_JOINER.join(map(str, positions))
        self.pnl = self.NUMBER_JOINER.join(map(str, pnl))

    def fetch_prices(self):
        url = f'https://api.iextrading.com/1.0/stock/{self.ticker.lower()}/chart/1y'

        response = requests.get(url)
        response_data = response.json()

        return [item['close'] for item in response_data]

