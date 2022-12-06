import math
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

    def calculate_series(self) -> dict:
        return {"rsi": ta.RSI(np.array(self.closes), timeperiod=self.period)}

    def get_chart(self, customs: dict) -> str:
        df = self.prepare_chart_data()
        R = RsiChart(df,customs)
        chart = R.get_chart()
        return chart

    def prepare_chart_data(self) -> pd.DataFrame:
        df = pd.DataFrame()
        df["opentime"] = self.dates
        df["values"] = self.calculate_series()["rsi"]
        df.dropna(inplace=True)
        return df

    def parse_value_from_series(self, vals: dict, idx: int) -> dict:
        return {"rsi": vals["rsi"][idx]}

    def get_signal(self, values: dict, criteria: dict) -> int:
        if math.isnan(values["rsi"]) or values["rsi"] < 10:
            return 0
        if values["rsi"] > int(criteria["rsi_up"]):
            return -1
        elif values["rsi"] < int(criteria["rsi_low"]):
            return 1
        return 0