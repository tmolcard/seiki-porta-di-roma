import logging

from sources.config.experiment import (
    DATA_PATH, MAX_PATH_LENGTH, MIN_PATH_LENGTH, MODEL_ID, N_SIMULATIONS, POSSIBLE_STARTING_FLOOR_LIST, SIMULATION_ID
)
from sources.domain.usecase.run_simulations import run_simulations
from sources.infrastructure.local_filesystem_handler import LocalFilesystemHandler

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    local_filesystem_handler = LocalFilesystemHandler(DATA_PATH)
    run_simulations(
        filesystem_handler=local_filesystem_handler,
        model_id=MODEL_ID,
        simulation_id=SIMULATION_ID,
        n_simulations=N_SIMULATIONS,
        possible_starting_floor_list=POSSIBLE_STARTING_FLOOR_LIST,
        min_path_length=MIN_PATH_LENGTH,
        max_path_length=MAX_PATH_LENGTH
    )
