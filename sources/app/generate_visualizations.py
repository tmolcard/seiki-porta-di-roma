import logging

from sources.config.experiment import DATA_PATH, SIMULATION_ID
from sources.domain.usecase.generate_visualizations import generate_visualizations
from sources.infrastructure.local_filesystem_handler import LocalFilesystemHandler

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    local_filesystem_handler = LocalFilesystemHandler(DATA_PATH)

    generate_visualizations(local_filesystem_handler, simulation_id=SIMULATION_ID)

    generate_visualizations(local_filesystem_handler, simulation_id=SIMULATION_ID, floor="0")
    generate_visualizations(local_filesystem_handler, simulation_id=SIMULATION_ID, floor="1")
