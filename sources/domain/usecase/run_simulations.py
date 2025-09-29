from sources.domain.entity.beacon_floor_markov import BeaconFloorMarkov
from sources.domain.entity.process_simulation_list import process_simulation_list
from sources.domain.port.filesystem_handler import FilesystemHandler


def run_simulations(
    filesystem_handler: FilesystemHandler, model_id: str, simulation_id: str, n_simulations: int,
    possible_starting_floor_list: list[str], min_path_length: int, max_path_length: int
):
    beacon_floor_markov: BeaconFloorMarkov = filesystem_handler.load_beacon_floor_markov(model_id=model_id)

    path_simulation_list = beacon_floor_markov.simulate_n_path(
        n_simulations=n_simulations,
        possible_starting_floor_list=possible_starting_floor_list,
        absorbing_floor_set=set(possible_starting_floor_list),
        min_path_length=min_path_length,
        max_path_length=max_path_length
    )

    df_count_sim = process_simulation_list(
        path_simulation_list=path_simulation_list, floor_list=beacon_floor_markov.floor_list
    )

    filesystem_handler.save_simulation(df_count_sim, simulation_id=simulation_id)
