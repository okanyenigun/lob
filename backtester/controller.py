from django.http import HttpRequest
from utility.utils import Utility
from backtester.service.backt import Backtest
from builder.meta import Meta

class BackController:
    """a kind of controller component
    helpers or services for backtesting app
    """

    @staticmethod
    def parse_input(request: HttpRequest) -> tuple([dict, dict]):
        """parses the data from the request
        
        Args:
            request (HttpRequest): request

        Returns:
            params: indicator parameters
            percents: weights
        """
        params = Utility.convert_req_to_dict(request, "POST")
        percents = BackController.correct_percentages(params)
        params = BackController.__filter_params(params)
        return params, percents

    @staticmethod
    def correct_percentages(params: dict) -> list:
        """if user dont fill percentage(weight) inputs, it is averaged
        for example; two indicator, each has 0 as weights, this will return 50-50
        Args:
            params (dict): indicator input parameters dictionary

        Returns:
            list: list of percentages
        """
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
    def __filter_params(params: dict) -> dict:
        """a helper function to filter request parameters

        Args:
            params (dict): obtained from request

        Returns:
            dict: filtered parameters
        """
        data = {}
        for key, value in params.items():
            if "csrf" in key or "weight" in key or "buy" in key or "sell" in key:
                continue
            data[key] = value
        return data

    @staticmethod
    def run_backtest(params: dict, percents: dict) -> tuple([list, int, int, float]):
        """runs the backtest

        Args:
            params (_type_): params & percents

        Returns:
            transaction history, #buy and sell orders and total profil in percentage
        """
        M = Meta()
        B = Backtest(params, percents, M.df_lob)
        transaction_history, buy_count, sell_count, profit = B.test()
        return transaction_history[::-1], buy_count, sell_count, profit