import talib as ta
import numpy as np
import pandas as pd
from utility.charts import RsiChart
from indicators.abs import Indicator

class Rsi(Indicator):

    def __init__(self, closes: list, dates:list) -> None:
        self.title = "RSI"
        self.closes = closes
        self.dates = dates
        self.period = 14

    def set_parameters(self, period:int=14) -> None:
        self.period = period
        return

    def calculate_series(self) -> np.ndarray:
        return ta.RSI(np.array(self.closes), timeperiod=self.period)

    def get_chart(self, customs: dict) -> str:
        df = self.prepare_chart_data()
        R = RsiChart(df,customs)
        chart = R.get_chart()
        return chart

    def prepare_chart_data(self) -> pd.DataFrame:
        df = pd.DataFrame()
        df["opentime"] = self.dates
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