import logging

from sources.config.beacon_count import BeaconCount
from sources.domain.entity.beacon_floor_markov import BeaconFloorMarkov
from sources.domain.port.filesystem_handler import FilesystemHandler


def fit_markov_model(filesystem_handler: FilesystemHandler, model_id: str):
    df = filesystem_handler.get_raw_dataframe()

    floor_list = df[BeaconCount.direction_in].unique().tolist()
    logging.info(f"Floors: {floor_list}")

    beacon_list = df[BeaconCount.beacon].unique().tolist()
    logging.info(f"Beacons: {beacon_list}")

    beacon_floor_markov = BeaconFloorMarkov(floor_list=floor_list, beacon_list=beacon_list)
    beacon_floor_markov = beacon_floor_markov.fit_transition_matrix(df)

    filesystem_handler.save_beacon_floor_markov(beacon_floor_markov, model_id=model_id)
