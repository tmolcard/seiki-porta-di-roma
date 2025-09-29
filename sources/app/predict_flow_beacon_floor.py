from sources.config.experiment import DATA_PATH, SIMULATION_ID
from sources.domain.usecase.get_portion_of_path import get_portion_of_path
from sources.infrastructure.local_filesystem_handler import LocalFilesystemHandler


if __name__ == "__main__":
    local_filesystem_handler = LocalFilesystemHandler(DATA_PATH)

    # Si l'on cherche à déterminer quelle proportion des usagers passeraient devant le magasin Guess par exemple
    # On suppose qu'un usager arrivant et ressortant par un même escalier fait le tour de l'étage (hypothèse très forte)

    FLOOR = "0"
    BEACON_PAIRS = [
        ("B1", "B3"),
        ("B2", "B3"),
        ("B1", "B6"),
        ("B2", "B6"),
        ("B4", "B3"),
        ("B5", "B3"),
        ("B1", "B1"),
        ("B2", "B2"),
        ("B3", "B3"),
        ("B4", "B4"),
        ("B5", "B5"),
        ("B6", "B6"),
    ]

    get_portion_of_path(
        filesystem_handler=local_filesystem_handler,
        floor=FLOOR,
        beacon_pairs=BEACON_PAIRS,
        simulation_id=SIMULATION_ID
    )
