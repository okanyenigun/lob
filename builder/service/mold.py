import pandas as pd
from typing import List

class Molder:
    """creates mold packages
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        
    def mold(self) -> pd.DataFrame:
        """a procedural method

        Returns:
            pd.DataFrame: return a new dataframe for mold packages
        """
        network_list = list(dict.fromkeys(self.df["network_time"].values.tolist()))
        liste = [self._create_mold_string(x) for x in network_list]
        df = self._create_df(network_list, liste)
        return df
        
    def _create_mold_string(self, network: int) -> str:
        """creates a mold package string for each network_time

        Args:
            network (int): network_time

        Returns:
            str: mold package string
        """
        temp = self.df[self.df["network_time"] == network]
        temp.reset_index(inplace=True, drop=True)
        string = ""
        for _, row in temp.iterrows():
            string += "-".join([str(row["msg_type"]), str(row["side"]), 
                                str(row["price"]), str(int(float(row["qty"]))), 
                                str(row["order_id"])]) + ";"
        return string[:-1]
    
    def _create_df(self, network_list: List[int], mold_list: List[str]) -> pd.DataFrame:
        """create the basis for lob dataframe

        Args:
            network_list (List[int]): unique network times
            mold_list (List[str]): obtained mold packages

        Returns:
            pd.DataFrame: new lob dataframe
        """
        df = pd.DataFrame()
        df["network_time"] = network_list
        df['network_date'] = pd.to_datetime(df['network_time'])
        df["mold"] = mold_list
        return df