import os
import pickle
from posixpath import join
from typing import Any

import pandas as pd
import plotly.graph_objects as go

from sources.config.beacon_count import BeaconCount
from sources.domain.port.filesystem_handler import FilesystemHandler

DATA_COUNTS_CSV = "data_counts.csv"
SIMULATIONS_PATH = "simulations"
MODELS_PATH = "models"
VISUALIZATION_PATH = "visualization"


class LocalFilesystemHandler(FilesystemHandler):
    def __init__(self, data_path):
        self.data_path = data_path

    def get_raw_dataframe(self) -> pd.DataFrame:
        return pd.read_csv(
            join(self.data_path, DATA_COUNTS_CSV),
            dtype=BeaconCount.types
        )

    def save_beacon_floor_markov(self, model: Any, model_id: str) -> None:
        os.makedirs(join(self.data_path, MODELS_PATH), exist_ok=True)

        model_file_path = join(self.data_path, MODELS_PATH, f"beacon_floor_markov_{model_id}.pkl")

        with open(model_file_path, mode="wb+") as file:
            pickle.dump(model, file)

    def load_beacon_floor_markov(self, model_id: str) -> Any:
        model_file_path = join(self.data_path, MODELS_PATH, f"beacon_floor_markov_{model_id}.pkl")
        with open(model_file_path, mode="rb") as file:
            model = pickle.load(file)
        return model

    def save_simulation(self, df: pd.DataFrame, simulation_id: str) -> None:
        os.makedirs(join(self.data_path, SIMULATIONS_PATH), exist_ok=True)

        return df.to_parquet(
            join(self.data_path, SIMULATIONS_PATH, f"beacon_floor_markov_simulations_{simulation_id}.parquet"),
        )

    def load_simulation(self, simulation_id: str) -> pd.DataFrame:
        return pd.read_parquet(
            join(self.data_path, SIMULATIONS_PATH, f"beacon_floor_markov_simulations_{simulation_id}.parquet"),
        )

    def save_visualization(self, fig: go.Figure, name: str, visualization_id: str) -> None:
        folder_path = join(self.data_path, VISUALIZATION_PATH)
        os.makedirs(folder_path, exist_ok=True)

        visualization_file_path = join(folder_path, f"{name}_{visualization_id}.html")
        with open(visualization_file_path, mode="w+", encoding='UTF-8') as f:
            f.write(fig.to_html())
