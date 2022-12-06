import math
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

    def calculate_series(self) -> dict:
        macd, macdsignal, macdhist = ta.MACD(np.array(self.closes),fastperiod=self.fastperiod,slowperiod=self.slowperiod,signalperiod=self.signalperiod)
        return {"macd":macd, "macdsignal":macdsignal, "macdhist":macdhist}

    def get_chart(self, customs: dict) -> str:
        df = self.prepare_chart_data()
        M = MacdChart(df,customs)
        chart = M.get_chart()
        return chart

    def prepare_chart_data(self) -> pd.DataFrame:
        df = pd.DataFrame()
        df["opentime"] = self.dates
        data = self.calculate_series()
        df["macd"] = data["macd"]
        df["macdsignal"] = data["macdsignal"]
        df["macdhist"] = data["macdhist"]
        df.dropna(inplace=True)
        return df

    def parse_value_from_series(self, vals: dict, idx: int) -> dict:
        return {"macd": vals["macd"][idx], "macdsignal": vals["macdsignal"][idx]}

    def get_signal(self, values: dict, criteria: dict) -> int:
        if math.isnan(values["macd"]) or math.isnan(values["macdsignal"]) or values["macd"] == 0:
            return 0
        diff = (values["macd"] - values["macdsignal"]) / values["macd"]
        if diff > float(criteria["macd"]):
            #buy signal
            return 1
        elif diff < - float(criteria["macd"]):
            #sell
            return -1
        return 0