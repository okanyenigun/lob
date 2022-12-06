import talib as ta
import numpy as np
import pandas as pd
from utility.charts import RsiChart

class Rsi():

    def __init__(self, closes: list, period:int=14):
        self.closes = closes
        self.period = period

    def calculate_series(self):
        return ta.RSI(np.array(self.closes), timeperiod=self.period)

    def get_rsi_chart(self, opentime_list, customs):
        df = self.__create_chart_data(opentime_list)
        R = RsiChart(df,customs)
        chart = R.get_chart()
        return chart

    def __create_chart_data(self,opentime_list):
        df = pd.DataFrame()
        df["opentime"] = opentime_list
        df["values"] = self.calculate_series()
        df.dropna(inplace=True)
        return df

    @staticmethod
    def get_signal(value, low=30, high=70):
        if value < 0:
            return 0
        if value < low:
            return -1
        elif value > high:
            return 1
        return 0