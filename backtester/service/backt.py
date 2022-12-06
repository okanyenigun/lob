import pandas as pd
from indicators.rsi import Rsi
from indicators.macd import Macd

class Backtest:
    """not very cohesive and has quite couplings
    should be refactored
    """

    def __init__(self, params: dict, percents: list, dflob: pd.DataFrame) -> None:
        self.options = {"rsi": Rsi, "macd": Macd}
        self.params = params
        self.percents = percents
        self.dflob = dflob
        self.money = 100000 #default start money
        self.stock = 0
        self.position = "Buy"
        self.buy_count = 0
        self.sell_count = 0
        self.transaction_history = []

    def test(self) -> tuple([list, int, int, float]):
        """main testing method

        Returns:
            transaction history, #buy and sell orders and total profil in percentage
        """
        #parse methods
        methods = [x for x in list(self.options.keys()) if x in list(self.params.keys())]
        #calculate series
        indicator_series, indicator_objects = self._get_indicator_series(methods)
        for i in range(self.dflob.shape[0]):
            self._tour(i, methods, indicator_series, indicator_objects)
        #and the profit
        profit = self.calculate_profit()
        return self.transaction_history, self.buy_count, self.sell_count, profit

    def _get_indicator_series(self, methods: list) -> tuple([dict, dict]):
        """_summary_

        Args:
            methods(list): indicator types

        Returns:
            series of calculated indicator results and their objects in dictionary
        """
        indicator_series = {}
        indicator_objects = {}
        closes = self.dflob["bid1px"].values.tolist()
        dates = self.dflob["Date"].values.tolist()
        for method in methods:
            I = self.options[method](closes, dates)
            indicator_series[method] = I.calculate_series()
            indicator_objects[method] = I
        return indicator_series, indicator_objects

    def _tour(self, idx: int, methods: list, indicator_series: dict, indicator_objects: dict) -> None:
        """a single tour in backtest

        Args:
            idx (int): index of row in dataframe
            methods (list): indicator method title
            indicator_series (dict): indicator vals
            indicator_objects (dict): indicator objects
        """
        #calculate signals
        signal = self._calculate_signals(idx, methods, indicator_series, indicator_objects)
        #buy and sell
        self._transaction(signal, idx)
        return

    def _calculate_signals(self, idx: int, methods: list, indicator_series: dict, indicator_objects: dict) -> int:
        """get signal for a single tour

        Args:
            idx (int): index of row in dataframe
            methods (list): indicator method title
            indicator_series (dict): indicator vals
            indicator_objects (dict): indicator objects

        Returns:
            int: signal value : 1 for buy and 0 for sell
        """
        signal = 0
        for method in methods:
            I = indicator_objects[method]
            series = indicator_series[method]
            value = I.parse_value_from_series(series, idx)
            signal_i = I.get_signal(value, self.params)
            percent = self.__get_percent(I.title)
            signal += signal_i * percent
        return signal

    def __get_percent(self, title: str) -> float:
        """a helper method that returns percentage of indicator

        Args:
            title (str): indicator title

        Returns:
            float
        """
        for p in self.percents:
            if p["parametername"] == title:
                return p["percent"] / 100
        return 0.0

    def _transaction(self, signal: int, idx: int) -> None:
        """buy or sell stock according to signal

        Args:
            signal (int): signal value: 1for buy -1 for sell
            idx (int): index of tour (or datafraem)
        """
        bid1px = self.dflob.loc[idx,"bid1px"]
        bid1qty = self.dflob.loc[idx,"bid1qty"]
        ask1px = self.dflob.loc[idx,"ask1px"]
        ask1qty = self.dflob.loc[idx,"ask1qty"]
        if signal > 0 and self.position == "Buy":
            self.buy(ask1px, ask1qty, idx)
        elif signal < 0 and self.position == "Sell":
            self.sell(bid1px, bid1qty, idx)
        return

    def buy(self, ask1px: float, ask1qty: int, idx: int) -> None:
        """ buying stock

        Args:
            ask1px (float): current ask price
            ask1qty (int): currecnt ask qty
            idx (int): idx of row
        """
        if ask1px == 0:
            return
        lot = ((self.money / ask1px) / 100)
        if lot <= ask1qty:
            #buy all
            self.stock += lot
            self.money = 0
            exchanged = lot
        else:
            #partial buy
            self.stock += ask1qty
            self.money -= (ask1qty*ask1px*100)
            exchanged = ask1qty
        self.position = "Sell"
        self.buy_count += 1
        self.transaction_history.append({"order": "Buy", "count": self.buy_count, "date": self.dflob.loc[idx, "Date"], "price": ask1px, "lot": exchanged, "money": self.money, "stock": self.stock})
        return

    def sell(self, bid1px: float, bid1qty: int, idx: int) -> None:
        """selling stock

        Args:
            bid1px (float): current buy price
            bid1qty (int): current buy qty
            idx (int): idx of row
        """
        if bid1px == 0:
            return
        if self.stock <= bid1qty:
            #sell all
            self.money += self.stock * bid1px * 100
            self.stock = 0
            exchanged = self.stock
        else:
            #partial sell
            self.money += bid1qty * bid1px * 100
            self.stock -= bid1qty
            exchanged = bid1qty
        self.position = "Buy"
        self.sell_count += 1
        self.transaction_history.append({"order": "Sell", "count": self.sell_count, "date": self.dflob.loc[idx, "Date"], "price": bid1px, "lot": exchanged, "money": self.money, "stock": self.stock})
        return

    def calculate_profit(self) -> float:
        """calculates the profit percentage in the final status

        Returns:
            float: _description_
        """
        last_buy_price = self.dflob["bid1px"].mask(self.dflob["bid1px"]==0).ffill().iloc[[-1]].values[0]
        self.money += last_buy_price * self.stock * 100
        profit = round((((self.money - 100000) / 100000) * 100),1)
        return profit