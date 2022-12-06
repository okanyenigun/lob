import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs._figure import Figure
from abc import ABC, abstractmethod

class ChartMakerAbstract(ABC):
    """an abstract class for charts
    """
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

class IChartMaker(ChartMakerAbstract):
    """concrete class for chart maker
    """
    
    def __init__(self, df: pd.DataFrame, customs: dict) -> None:
        """_summary_

        Args:
            df (pd.DataFrame): lob
            customs (dict): annotations dictionary
        """
        self.df = df
        self.customs = customs

    def get_chart(self) -> str:
        """a procedural method to obtain chart

        Returns:
            str: html string for plotly figure
        """
        fig = self.create_figure()
        fig = self.update_figure(fig)
        graph = self.convert_to_html(fig)
        return graph

    def create_figure(self) -> Figure:
        """create basic figure

        Returns:
            Figure: plotly figure object
        """
        fig = go.Figure(data=go.Scatter(x = self.df["opentime"], y = self.df["values"]))
        return fig

    def update_figure(self, fig: Figure) -> Figure:
        """add annotations

        Args:
            fig (Figure): basic figure

        Returns:
            Figure: updated figure
        """
        fig.update_layout(
                        title=self.customs["title"],
                        yaxis_title=self.customs["ytitle"],
                    )
        return fig

    def convert_to_html(self, fig: Figure) -> str:
        """converts the chart into string format to display in page

        Args:
            fig (Figure): final figure

        Returns:
            str: html string
        """
        graph = fig.to_html(
            full_html=False, default_height=self.customs["h"], default_width=self.customs["w"])
        return graph


    


class MacdChart(IChartMaker):
    def __init__(self, df: pd.DataFrame, customs: dict):
        super().__init__(df,customs)

    def create_figure(self):
        fig = go.Figure(data=go.Scatter())
        fig.add_trace(go.Scatter(x=self.df["opentime"], y=self.df["macd"],line=dict(color="#a74f26"), showlegend=False))
        fig.add_trace(go.Scatter(x=self.df["opentime"], y=self.df["macdsignal"],line=dict(color="#a74f26"), showlegend=False))
        fig.add_trace(go.Scatter(x=self.df["opentime"], y=self.df["macdhist"],line=dict(color="#a74f26"), showlegend=False))
        return fig

class RsiChart(IChartMaker):

    def __init__(self, df: pd.DataFrame, customs: dict):
        super().__init__(df,customs)

    def create_figure(self):
        fig = go.Figure(data=go.Scatter(x = self.df["opentime"], y = self.df["values"]))
        return fig