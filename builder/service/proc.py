import pandas as pd
from builder.service.dataproc import DataProcessor
from builder.service.mold import Molder
from builder.service.lobber import Lobber

class DataBuilder:

    @staticmethod
    def build(path: str) -> pd.DataFrame:
        """a procedural method to create lob dataset from given order data
        path: path of excel file
        Returns:
            pd.DataFrame: final lob dataframe   
        """
        D = DataProcessor(path)
        df = D.setup()
        M = Molder(df)
        df_lob_mold = M.mold()
        L = Lobber(df_lob_mold)
        rows, _, _ = L.create()
        df_lob_price = pd.DataFrame(data=rows)
        df_lob = pd.concat([df_lob_mold, df_lob_price], axis=1)
        df_lob.columns = ["network_time","Date","Mold Package", "bid3qty", "bid3px",
                        "bid2qty", "bid2px", "bid1qty", "bid1px", "ask1px", "ask1qty",
                        "ask2px", "ask2qty","ask3px", "ask3qty"]
        df_lob["Asset"] = ["AKBNK"] * df_lob.shape[0]
        lob = df_lob.loc[:, ["network_time","Date","Asset","bid3qty", "bid3px",
                  "bid2qty", "bid2px", "bid1qty", "bid1px", "ask1px", "ask1qty",
                  "ask2px", "ask2qty","ask3px", "ask3qty","Mold Package"]]
        return lob