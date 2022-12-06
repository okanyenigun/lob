from abc import ABC, abstractmethod


class Indicator(ABC):
    """an abstract (and not cohesive) class for indicators
    """

    @abstractmethod
    def calculate_series(self):
        """calculate indicator data
        """

    @abstractmethod
    def get_chart(self, customs: dict):
        """draw chart of series"""

    @staticmethod
    @abstractmethod
    def get_signal():
        """calculate buy or sell signal"""

    @abstractmethod
    def set_parameters(self, *args, **kwargs):
        """rearrange parameters"""

    @abstractmethod
    def prepare_chart_data(self):
        """prepares the data required for chart
        """
    @abstractmethod
    def parse_value_from_series(self, *args):
        """it selects the necessary information for signal calculation
        needs customization for each indicator"""