import itertools
import pandas as pd
class Lobber:
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.buy_orders = {}
        self.sell_orders = {}
        self.rows = []
        
    def create(self) -> tuple([list, dict, dict]):
        """procedural method

        Returns:
            a tuple: lob rows list, buy and sell orders dictionaries
        """
        for i in range(self.df.shape[0]):
            row = self.df.loc[i, "mold"].split(";")
            for j in range(len(row)):
                liste = row[j].split("-")
                side = liste[1]
                price = float(liste[2])
                qty = int(liste[3])
                #buy&sell
                qty = self._buysell(side, price, qty)
                #book
                self._add_to_book(side, price, qty)
                #row
            row = self._parse_row()
            self.rows.append(row)
        return self.rows, self.buy_orders, self.sell_orders
    
    def _buysell(self, side, price, qty):
        if side == "B":
            qty, self.sell_orders = self.__transact(price, self.sell_orders, qty, 1, False)
        elif side == "S":
            qty, self.buy_orders = self.__transact(price, self.buy_orders, qty, -1, True)
        return qty
        
    def __transact(self, price, price_book, qty, direction, reverse):
        """direction=1 : buy"""
        prices = sorted(list(price_book.keys()), reverse=reverse)
        for p in prices:
            if price_book[p] == 0:
                continue
            #print(price * direction >= p * direction)
            if price * direction >= p * direction:
                if price_book[p] >= qty:
                    #print(f"if transact: {price} direction: {direction} p: {p} p_qty: {price_book[p]} - qty: {qty}")
                    price_book[p] += -qty
                    #print(price_book[p])
                    if price_book[p] == 0:
                        price_book.pop(p)
                    qty = 0
                else:
                    #print(f"else transact: {price} direction: {direction} p: {p} p_qty: {price_book[p]} - qty: {qty}")
                    val = price_book[p]
                    price_book.pop(p)
                    qty += -val
        return qty, price_book

    def _add_to_book(self, side, price, qty):
        if side == "B":
            self.buy_orders = self.__adding(self.buy_orders, price, qty)
        elif side == "S":
            self.sell_orders = self.__adding(self.sell_orders, price, qty)
        return
    
    def __adding(self, price_book, price, qty):
        if qty == 0:
            return price_book
        keys = list(price_book.keys())
        if price in keys:
            price_book[price] += qty
        else:
            price_book[price] = qty
        return price_book
    
    def _parse_row(self):
        bids = self.__find_rows(self.buy_orders, True)[::-1]
        #print("bids: ",bids)
        asks = self.__find_rows(self.sell_orders, False)
        #print("asks: ",asks)
        #print()
        #print(list(itertools.chain(bids, asks)))
        return list(itertools.chain(bids, asks))
        
    def __find_rows(self, price_list,reverse):
        prices = sorted(list(price_list.keys()), reverse=reverse)[:3]
        #print("prices: ",prices)
        #print("price_list: ",price_list)
        qty_list = [price_list[e] for e in prices]
        #print("qty_list: ",qty_list)
        merged = list([x for x in itertools.chain.from_iterable(itertools.zip_longest(prices,qty_list)) if x])
        merged.extend(itertools.repeat(0, 6-len(merged)))
        return merged
        