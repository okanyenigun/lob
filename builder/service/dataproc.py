import pandas as pd
import numpy as np
import multiprocessing
from utility.utils import Utility

class DataProcessor:
    """cleans and fills missing data (price&qty)
    """
    
    def __init__(self, path: str) -> None:
        self.data_raw = pd.read_csv(path, names=["network_time", "bist_time", "msg_type", 
                                                  "asset_name", "side", "price", "que_loc", 
                                                  "qty", "order_id"])
        self.df_zero_price = None  #these variables were created for ease of use
        self.df_price = None
        self.df_zero_qty = None
        self.df_qty = None
        self.core_count = multiprocessing.cpu_count() - 1 #multiprocess purposes
    
    def setup(self) -> pd.DataFrame:
        """a procedure method

        Returns:
            pd.DataFrame: final dataframe
        """
        df = self._clean()
        df = self._index_price_by_order(df)
        df = self._index_qty_by_order(df)
        return df
    
    def _clean(self) -> pd.DataFrame:
        """cleans the dataset
        *only B and S sides
        Returns:
            pd.DataFrame: cleaned dataframe
        """
        #only B and S sides
        df = self.data_raw[(self.data_raw["side"] == "B") | (self.data_raw["side"] == "S")]
        df.reset_index(inplace=True, drop=True)
        #to be able to use index as a unique id
        df.reset_index(inplace=True)
        return df

    def _index_price_by_order(self, df: pd.DataFrame) -> pd.DataFrame:
        """fills missing price data by indexing

        Args:
            df (pd.DataFrame): original dataframe

        Returns:
            pd.DataFrame: updated dataframe
        """
        #split data
        self.df_zero_price = df[df["price"] == 0]
        self.df_zero_price.reset_index(inplace=True, drop=True) # to be able to use .loc
        self.df_price = df[df["price"] > 0]
        self.df_price.reset_index(inplace=True, drop=True)
        #obtain new prices
        new_prices = self._run_loops_for_price()
        new_prices = {k:v for list_item in new_prices for (k,v) in list_item.items()}
        df_new_prices = pd.DataFrame(new_prices.items(), columns=["index","price"])
        #add new info into the dataframe
        df = Utility.indexing_1(df_new_prices, df, "index", "price","temp_price")
        df['price'] = np.where(df['price'].eq(0),df['temp_price'],df['price'])
        df.drop(['temp_price'],axis=1,inplace=True)
        return df
    
    def _run_loops_for_price(self) -> list:
        """splits the workload in parallel
        Performs indexing for missing price data
        Returns:
            list: a list of dictionaries
        """
        range_list = self.__create_ranges(self.core_count, self.df_zero_price.shape[0])
        price_list = []
        with multiprocessing.Pool(self.core_count) as p:
            #needs refactoring for reusability
            results = p.starmap(self._loop_for_price, [(range_list[0],range_list[1]), (range_list[1],range_list[2]),(range_list[2],range_list[3]),
            (range_list[3],range_list[4]),(range_list[4],range_list[5]),(range_list[5],range_list[6]),(range_list[6],range_list[7]),
            (range_list[7],range_list[8]),(range_list[8],range_list[9]),(range_list[9],range_list[10]),(range_list[10],range_list[11])])
            for res in results:
                price_list.append(res)
        return price_list

    def _loop_for_price(self, start:int, end:int) -> dict:
        """finds the price value in message type A for the price information that is zero

        Args:
            start (int): range start for loop
            end (int): range end for loop

        Returns:
            dict: a dictionary key: index of row value: non-zero price value
        """
        results = {}
        for i in range(start, end):
            temp = self.df_price[(self.df_price["order_id"] == self.df_zero_price.loc[i,"order_id"]) & 
                                (self.df_price["network_time"] <= self.df_zero_price.loc[i,"network_time"]) & 
                                (self.df_price["index"] < self.df_zero_price.loc[i,"index"])]
            temp.reset_index(inplace=True, drop=True)
            price = temp.loc[len(temp)-1, "price"]
            results[self.df_zero_price.loc[i,"index"]] = price
        return results

    def _index_qty_by_order(self, df: pd.DataFrame) -> pd.DataFrame:
        """fills missing qty data by indexing

        Args:
            df (pd.DataFrame): original dataframe

        Returns:
            pd.DataFrame: updated dataframe
        """
        #split data
        self.df_zero_qty = df[df["qty"] == 0]
        self.df_zero_qty.reset_index(inplace=True, drop=True) # to be able to use .loc
        self.df_qty = df[df["qty"] > 0]
        self.df_qty.reset_index(inplace=True, drop=True)
        #obtain new qty
        new_qty = self._run_loops_for_qty()
        new_qty = {k:v for list_item in new_qty for (k,v) in list_item.items()}
        df_new_qty = pd.DataFrame(new_qty.items(), columns=["index","qty"])
        #add new info into the dataframe
        df = Utility.indexing_1(df_new_qty, df, "index", "qty","temp_qty")
        df['qty'] = np.where(df['qty'].eq(0),df['temp_qty'],df['qty'])
        df.drop(['temp_qty'],axis=1,inplace=True)
        return df

    def _run_loops_for_qty(self) -> list:
        """splits the workload in parallel
        Performs indexing for missing qty data
        Returns:
            list: a list of dictionaries
        """
        range_list = self.__create_ranges(self.core_count, self.df_zero_qty.shape[0])
        qty_list = []
        with multiprocessing.Pool(self.core_count) as p:
            #needs refactoring for reusability
            results = p.starmap(self._loop_for_qty, [(range_list[0],range_list[1]), (range_list[1],range_list[2]),(range_list[2],range_list[3]),
            (range_list[3],range_list[4]),(range_list[4],range_list[5]),(range_list[5],range_list[6]),(range_list[6],range_list[7]),
            (range_list[7],range_list[8]),(range_list[8],range_list[9]),(range_list[9],range_list[10]),(range_list[10],range_list[11])])
            for res in results:
                qty_list.append(res)
        return qty_list

    def _loop_for_qty(self, start: int, end: int) -> dict:
        """finds the qty value

        Args:
            start (int): range start for loop
            end (int): range end for loop

        Returns:
            dict: a dictionary key: index of row value: non-zero qty value
        """
        results = {}
        for i in range(start, end):
            temp = self.df_qty[(self.df_qty["order_id"] == self.df_zero_qty.loc[i,"order_id"]) & 
                                (self.df_qty["network_time"] <= self.df_zero_qty.loc[i,"network_time"]) & 
                                (self.df_qty["index"] < self.df_zero_qty.loc[i,"index"])]
            temp.reset_index(inplace=True, drop=True)
            new_qty = self.__split_qty(temp)
            results[self.df_zero_qty.loc[i,"index"]] = new_qty
        return results

    def __split_qty(self, temp: pd.DataFrame) -> int:
        """qty is the difference between previous A and previous E qty
        NEEDS CONFIRMATION!
        Args:
            temp (pd.DataFrame): filtered dataframe of the given order

        Returns:
            int: new qty
        """
        #for a
        temp_a = temp[temp["msg_type"] == "A"]
        temp_a.reset_index(inplace=True, drop=True)
        qty_a = temp_a.loc[len(temp_a)-1, "qty"]
        a_idx = temp_a.loc[len(temp_a)-1,"index"]
        #for e
        temp_e = temp[temp["msg_type"] == "E"]
        if temp_e.shape[0] == 0:
            qty_e =0
        else:
            temp_e = temp_e[temp_e["index"] > a_idx]
            qty_e = temp_e["qty"].sum()
        qty = qty_a - qty_e
        if qty <0:
            qty = 0
        return int(qty)

    def __create_ranges(self, core: int, length: int) -> list:
        """a helper method 
        divides loop ranges according to the number of cores

        Args:
            core (int): available cpu core
            length (int): the total row count of the dataframe

        Returns:
            list: equally divided ranges
        """
        range_list = list(range(0, length, int(length / core)))
        range_list[-1] = length
        return range_list