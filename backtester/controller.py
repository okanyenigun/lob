import os
import pandas as pd
import plotly.graph_objs as go
from django.conf import settings
from builder.meta import Meta
from utility.utils import Utility

class BackController:
    """a kind of controller component
    helpers or services for backtesting app
    """

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
    def collect_page_elements(df):
        data = {}
        #table
        data["arr"], data["columns"] = Utility.convert_df_to_html(df.iloc[:200,:])
        #chart
        data["graph"] = BackController.draw_line_chart(df)
        return data

    @staticmethod
    def draw_line_chart(df: pd.DataFrame, yrange:list = [11.6, 12], height: int = 400, width: int = 800) -> str:
        x = df["network_time"].values.tolist()
        bid = df["bid1px"].values.tolist()
        ask = df["ask1px"].values.tolist()
        fig = go.Figure(data=go.Scatter(),layout_yaxis_range=yrange)
        fig.add_trace(go.Scatter(name="bids", x=x, y=bid,line=dict(color="green"), showlegend=True))
        fig.add_trace(go.Scatter(name="asks", x=x, y=ask,line=dict(color="red"), showlegend=True))
        graph = fig.to_html(full_html=False, default_height=height, default_width=width)
        print(type(graph))
        return graph