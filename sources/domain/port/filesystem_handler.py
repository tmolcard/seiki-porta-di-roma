from abc import ABC, abstractmethod
from typing import Any

import pandas as pd
import plotly.graph_objects as go


class FilesystemHandler(ABC):

    @abstractmethod
    def get_raw_dataframe(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def save_beacon_floor_markov(self, model: Any, model_id: str) -> None:
        pass

    @abstractmethod
    def load_beacon_floor_markov(self, model_id: str) -> Any:
        pass

    @abstractmethod
    def save_simulation(self, df: pd.DataFrame, simulation_id: str) -> None:
        pass

    @abstractmethod
    def load_simulation(self, simulation_id: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def save_visualization(self, fig: go.Figure, name: str, visualization_id: str) -> None:
        pass
