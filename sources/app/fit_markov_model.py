import logging

from sources.config.experiment import DATA_PATH, MODEL_ID
from sources.domain.usecase.fit_markov_model import fit_markov_model
from sources.infrastructure.local_filesystem_handler import LocalFilesystemHandler

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    local_filesystem_handler = LocalFilesystemHandler(DATA_PATH)
    fit_markov_model(
        filesystem_handler=local_filesystem_handler,
        model_id=MODEL_ID
    )
