import os
import pandas as pd
import plotly.graph_objs as go
from django.conf import settings
from builder.meta import Meta
from utility.utils import Utility
from indicators.macd import Macd
from indicators.rsi import Rsi
from indicators.abs import Indicator

class BuilderController:

    @staticmethod
    def create_excel_for_df() -> str:
        """creates an excel file of df_lob in the static folder

        Returns:
            str: path
        """
        path = os.path.join(settings.STATICFILES_DIRS[0], "files", "lob.xlsx")
        M = Meta()
        M.df_lob.to_excel(path, index=False)
        return path

    @staticmethod
    def collect_page_elements(indicator: str) -> dict:
        """collects UI elements to display in home page

        Args:
            indicator (str): indicator type for chart

        Returns:
            dict: context data
        """
        M = Meta()
        data = {}
        #table
        data["arr"], data["columns"] = Utility.convert_df_to_html(M.df_lob.iloc[:200,:])
        #chart
        data["graph"] = BuilderController.draw_line_chart(M.df_lob)
        #indicator chart
        indicator_objects = {"macd": Macd, "rsi": Rsi}
        data["indicatorGraph"] = BuilderController.get_indicator_chart(M.df_lob, indicator_objects[indicator])
        return data

    @staticmethod
    def draw_line_chart(df: pd.DataFrame, height: int = 400, width: int = 800) -> str:
        """bid and ask line chart

        Args:
            df (pd.DataFrame): lob
            height (int, optional): chart heigth. Defaults to 400.
            width (int, optional): chart width. Defaults to 800.

        Returns:
            str: html string of plotly chart
        """
        x = pd.to_datetime(df['network_time'])
        bid = df["bid1px"].values.tolist()
        ask = df["ask1px"].values.tolist()
        yrange = [11, 12]
        fig = go.Figure(data=go.Scatter(),layout_yaxis_range=yrange)
        fig.add_trace(go.Scatter(name="bids", x=x, y=bid,line=dict(color="green"), showlegend=True))
        fig.add_trace(go.Scatter(name="asks", x=x, y=ask,line=dict(color="red"), showlegend=True))
        graph = fig.to_html(full_html=False, default_height=height, default_width=width)
        return graph

    @staticmethod
    def get_indicator_chart(df: pd.DataFrame, I: Indicator) -> str:
        """any indicator chart

        Args:
            df (pd.DataFrame): lob
            I (Indicator): indicator object

        Returns:
            str: html string of plotly chart
        """
        Ind = I(df["bid1px"].values.tolist(), pd.to_datetime(df['network_time']))
        chart = Ind.get_chart({"h":400,"w":800, "title":Ind.title, "ytitle":""})
        return chart