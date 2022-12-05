import pandas as pd
import plotly.graph_objects as go
from abc import ABC, abstractmethod

class ChartMakerAbstract(ABC):

    @abstractmethod
    def create_figure(self):
        pass

    @abstractmethod
    def update_figure(self):
        pass

    @abstractmethod
    def get_chart(self):
        pass

    @abstractmethod
    def convert_to_html(self):
        pass

class ChartMaker(ChartMakerAbstract):
    
    def __init__(self, df: pd.DataFrame, customs: dict):
        self.df = df
        self.customs = customs

    def create_figure(self):
        fig = go.Figure(data=go.Scatter(x = self.df["opentime"], y = self.df["values"]))
        return fig

    def update_figure(self,fig):
        fig.update_layout(
                        title=self.customs["title"],
                        yaxis_title=self.customs["ytitle"],
                    )
        return fig

    def convert_to_html(self,fig):
        graph = fig.to_html(
            full_html=False, default_height=self.customs["h"], default_width=self.customs["w"])
        return graph


    def get_chart(self):
        fig = self.create_figure()
        fig = self.update_figure(fig)
        graph = self.convert_to_html(fig)
        return graph


class MacdChart(ChartMaker):
    def __init__(self, df: pd.DataFrame, customs: dict):
        super().__init__(df,customs)

    def create_figure(self):
        fig = go.Figure(data=go.Scatter())
        fig.add_trace(go.Scatter(x=self.df["Date"], y=self.df["macd"],line=dict(color="#a74f26"), showlegend=False))
        fig.add_trace(go.Scatter(x=self.df["Date"], y=self.df["macdsignal"],line=dict(color="#a74f26"), showlegend=False))
        fig.add_trace(go.Scatter(x=self.df["Date"], y=self.df["macdhist"],line=dict(color="#a74f26"), showlegend=False))
        return fig