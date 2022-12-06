import itertools
import pandas as pd

class Lobber:
    """finalizes the limit order book, performs operations a,e,d
    """
    
    def __init__(self, df:pd.DataFrame) -> None:
        self.df = df
        self.buy_orders = {} #stores buy orders key:price value:qty
        self.sell_orders = {} #stores sell orders
        self.rows = [] #each row of lob df

    def create(self) -> tuple([list, dict, dict]):
        """The method that implements the trading decisions (A,E,D) for each mold information in the sent mold dataset.

        Returns:
            tuple: the rows and orders
        """
        for _, row in self.df.iterrows():
            mold_list = row["mold"].split(";")
            self._direct_orders(mold_list)
            row = self._parse_row()
            self.rows.append(row)
        return self.rows, self.buy_orders, self.sell_orders

    def _direct_orders(self, mold_list: list) -> None:
        """apply buy or sell for each order in mold list

        Args:
            mold_list (list): mold
        """
        [self._buysell(x.split("-")[0], x.split("-")[1], float(x.split("-")[2]), int(x.split("-")[3])) for x in mold_list]
        return
    
    def _buysell(self, msg: str, side: str, price: float, qty: int) -> None:
        """drop or add to order books

        Args:
            msg (str): A, E, D
            side (str): Buy or Sell
            price (float): price data
            qty (int): quantity data
        """
        if msg == "E" and side == "B":
            #bidden düş
            self.buy_orders = self.__drop_order(price, self.buy_orders, qty)
        elif msg == "E" and side == "S":
            #sellden düş
            self.sell_orders = self.__drop_order(price, self.sell_orders, qty)
        elif msg == "D" and side == "B":
            #bidden düş
            self.buy_orders = self.__drop_order(price, self.buy_orders, qty)
        elif msg == "D" and side == "S":
            #sellden düş
            self.sell_orders = self.__drop_order(price, self.sell_orders, qty)
        elif msg == "A" and side == "B":
            #add buy
            self.buy_orders = self.__add_order(price, self.buy_orders, qty)
        elif msg == "A" and side == "S":
            #add sell
            self.sell_orders = self.__add_order(price, self.sell_orders, qty)
        return
    
    def __add_order(self, price: float, price_book: dict, qty: int) -> dict:
        """add qty to price level

        Args:
            price (float): price data
            price_book (dict): buy_orders or sell_orders
            qty (int): quantity

        Returns:
            dict: buy_orders or sell_orders
        """
        try:
            price_book[price] += qty
        except:
            price_book[price] = qty
        return price_book
    
    def __drop_order(self, price: float, price_book: dict, qty: int) -> dict:
        """if exists drop; if all the qty sold, drop the key

        Args:
             price (float): price data
            price_book (dict): buy_orders or sell_orders
            qty (int): quantity

        Returns:
            dict: buy_orders or sell_orders
        """
        if price in list(price_book.keys()):
            if price_book[price] > qty:
                price_book[price] += -qty
            else:
                price_book.pop(price)
        return price_book
    
    def _parse_row(self) -> list:
        """return one list (group)

        Returns:
            list: each row of lob df
        """
        bids = self.__find_rows(self.buy_orders, True)[::-1]
        asks = self.__find_rows(self.sell_orders, False)
        return list(itertools.chain(bids, asks))
        
    def __find_rows(self, price_list: dict, reverse: bool) -> list:
        """extract each part of bids and asks 

        Args:
            price_list (dict): sell or buy orders 
            reverse (bool): direction of sorting

        Returns:
            list: ask or bid row part
        """
        prices = sorted(list(price_list.keys()), reverse=reverse)[:3]
        qty_list = [price_list[e] for e in prices]
        merged = list([x for x in itertools.chain.from_iterable(itertools.zip_longest(prices,qty_list)) if x])
        merged.extend(itertools.repeat(0, 6-len(merged)))
        return merged