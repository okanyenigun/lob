import pandas as pd
import numpy as np
from utility.utils import Utility

class DataProcessor:
    """prepare given data to obtain a LOB dataset
    """
    
    def __init__(self, path: str) -> None:
        self.data_raw = pd.read_csv(path, names=["network_time", "bist_time", "msg_type", 
                                                  "asset_name", "side", "price", "que_loc", 
                                                  "qty", "order_id"])
    
    def setup(self) -> pd.DataFrame:
        """a procedure method

        Returns:
            pd.DataFrame: final dataframe
        """
        df = self._clean()
        #correct e&d
        df = self._fill_ed_empty_price(df)
        return df
    
    def _clean(self) -> pd.DataFrame:
        """general
        *only B and S sides
        Returns:
            pd.DataFrame: cleaned dataframe
        """
        #only B and S sides
        df = self.data_raw[(self.data_raw["side"] == "B") | (self.data_raw["side"] == "S")]
        df.reset_index(inplace=True, drop=True)
        return df
    
    def _fill_ed_empty_price(self, df: pd.DataFrame) -> pd.DataFrame:
        """(E) ve (D) tipli mesajlarda fiyat bilgisi bulunmuyor. Bu işlemlerin hangi fiyat seviyesinden gerçekleştiğini “order_id”leri kullanarak ve (A) mesajları ile eşleştirme yaparak bulabilirsiniz.

        Args:
            df (pd.DataFrame): cleaned dataframe

        Returns:
            pd.DataFrame: filled dataframe
        """
        temp = df[df["msg_type"] == "A"]
        df = Utility.indexing_1(temp, df, "order_id", "price", "temp_price")
        df['price'] = np.where(df['price'].eq(0),df['temp_price'],df['price'])
        df.drop(['temp_price'],axis=1,inplace=True)
        return df