import os
import pandas as pd
import plotly.graph_objs as go
from django.conf import settings
from builder.meta import Meta
from utility.utils import Utility
from indicators.macd import Macd
from indicators.rsi import Rsi
from backtester.service.backt import Testing

class BackController:
    """a kind of controller component
    helpers or services for backtesting app
    """

    @staticmethod
    def parse_input(request):
        params = Utility.convert_req_to_dict(request, "POST")
        percents = BackController.correct_percentages(params)
        params = BackController.foo(params)
        return params, percents

    @staticmethod
    def correct_percentages(params):
        "if user dont fill percentages inputs, it is averaged"
        percents = []
        for key, value in params.items():
            if "weight" in key:
                percents.append(float(value))
        total = 0
        for p in percents:
            total += float(p)
        if total == 100:
            return percents
        if total > 100:
            diff = 1 / ((total - 100) / len(percents))
            percents = [float(x) - (float(x) * diff) for x in percents]
        elif total > 0 and total < 100:
            percents = [float(x) * 100 / total for x in percents]
        else:
            ratio = 100 / len(percents)
            percents = [ratio] * len(percents)
        data = []
        
        i = 0
        for key, value in params.items():
            out = {}
            if "weight" in key:
                if "_RSI" in key:
                    out["parametername"] = "RSI"
                elif "_Bollinger" in key:
                    out["parametername"] = "Bollinger"
                elif "_MACD" in key:
                    out["parametername"] = "MACD"
                elif "_S&R" in key:
                    out["parametername"] = "Support&Resistance"
                elif "_AI" in key:
                    out["parametername"] = "AI"
                out["percent"] = percents[i]
                i += 1
                data.append(out)
        return data

    @staticmethod
    def foo(params):
        data = {}
        for key, value in params.items():
            if "csrf" in key or "weight" in key or "buy" in key or "sell" in key:
                continue
            data[key] = value
        return data

    @staticmethod
    def run_backtest(params, percents):
        T = Testing(params, percents)
        T.run()

        return