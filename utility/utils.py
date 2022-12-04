import pandas as pd

class Utility:
    
    @staticmethod
    def indexing_1(source_data: pd.DataFrame, new_data: pd.DataFrame, indexed_title: str, map_title: str, new_column: str) -> pd.DataFrame:
        """Excel match-index operation

        Args:
            source_data (pd.DataFrame): the source for the new column
            new_data (pd.DataFrame): target dataframe
            indexed_title (str): common column name from the both dataframes
            map_title (str): target column name in the source
            new_column (str): new column name in the new_data

        Returns:
            pd.DataFrame: returns the new_data with the new column
        """
        source = source_data.copy()
        try:
            source.set_index(indexed_title, inplace=True)
        except:
            pass
        map_dict = source[map_title].to_dict()
        new_data[new_column] = new_data[indexed_title].map(map_dict)
        return new_data
    