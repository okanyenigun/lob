import talib as ta
import numpy as np
import pandas as pd
from indicators.abs import Indicator
from utility.charts import MacdChart

class Macd(Indicator):

    def __init__(self, closes: list, dates:list) -> None:
        self.title = "MACD"
        self.closes = closes
        self.dates = dates
        self.fastperiod = 12
        self.slowperiod = 26
        self.signalperiod = 29
    
    def set_parameters(self, fast_period:int=12, slowperiod:int=26, signalperiod:int=29) -> None:
        self.fastperiod = fast_period
        self.slowperiod = slowperiod
        self.signalperiod = signalperiod
        return

    def calculate_series(self) -> tuple([np.ndarray, np.ndarray, np.ndarray]):
        macd, macdsignal, macdhist = ta.MACD(np.array(self.closes),fastperiod=self.fastperiod,slowperiod=self.slowperiod,signalperiod=self.signalperiod)
        return macd, macdsignal, macdhist

    def get_chart(self, customs: dict) -> str:
        df = self.prepare_chart_data()
        M = MacdChart(df,customs)
        chart = M.get_chart()
        return chart

    def prepare_chart_data(self) -> pd.DataFrame:
        df = pd.DataFrame()
        df["opentime"] = self.dates
        df["macd"], df["macdsignal"],df["macdhist"] = self.calculate_series()
        df.dropna(inplace=True)
        return df

    @staticmethod
    def get_signal(macd, macd_prev):
        if macd > 0 and macd > macd_prev:
            return -1
        elif macd < 0 and macd >= macd_prev:
            return 1
        elif macd < 0 and macd <= macd_prev:
            return -1
        else:
            return 0
      

# class Macd():

#     def __init__(self,closes,fastperiod=12,slowperiod=26,signalperiod=29):
#         self.closes = closes
#         self.fastperiod = fastperiod
#         self.slowperiod = slowperiod
#         self.signalperiod = signalperiod

#     def calculate_series(self):
#         macd, macdsignal, macdhist = ta.MACD(np.array(self.closes),fastperiod=self.fastperiod,slowperiod=self.slowperiod,signalperiod=self.signalperiod)
#         return macd, macdsignal, macdhist

#     def get_macd_chart(self,opentime_list,customs):
#         df = self.__create_chart_data(opentime_list)
#         M = MacdChart(df,customs)
#         chart = M.get_chart()
#         return chart

#     def __create_chart_data(self,opentime_list):
#         df = pd.DataFrame()
#         df["opentime"] = opentime_list
#         df["macd"], df["macdsignal"],df["macdhist"] = self.calculate_series()
#         df.dropna(inplace=True)
#         return df

#     @staticmethod
#     def get_signal(macd, macd_prev):
#         if macd > 0 and macd > macd_prev:
#             return -1
#         elif macd < 0 and macd >= macd_prev:
#             return 1
#         elif macd < 0 and macd <= macd_prev:
#             return -1
#         else:
#             return 0