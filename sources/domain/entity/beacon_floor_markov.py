from typing import Self

import numpy as np
import pandas as pd

from sources.config.beacon_count import BeaconCount


class BeaconFloorMarkov():
    def __init__(self, floor_list: list[str], beacon_list: list[str]):
        self.floor_list = floor_list
        self.beacon_list = beacon_list

        self.transition_matrix = None
        self.possible_starting_floor_list = None
        self.starting_probs = None

    def fit_transition_matrix(self, df: pd.DataFrame) -> Self:

        beacon_floor_list = self.floor_list + self.beacon_list

        od_matrix = pd.DataFrame(0, index=beacon_floor_list, columns=beacon_floor_list)

        floor_beacon_aggregation = df.groupby(
            [BeaconCount.direction_in, BeaconCount.beacon, BeaconCount.direction_out]
        )[BeaconCount.count].sum()

        for (direction_in, beacon, direction_out), count in floor_beacon_aggregation.items():
            od_matrix.loc[direction_in, beacon] = count
            od_matrix.loc[beacon, direction_out] = count

        # We assume no one takes the stairs to get back to the floor they are coming from.
        # We want to avoid paths like Fi -> Bx -> Fi.
        second_order_od_matrix = od_matrix.loc[self.floor_list, :]

        beacon_floor_matrix = od_matrix.loc[self.beacon_list, :]

        for floor in self.floor_list:
            floor_beacon_floor_matrix = beacon_floor_matrix.copy()
            floor_beacon_floor_matrix.loc[:, floor] = 0
            floor_beacon_floor_matrix.index = [f"{floor}_{b}" for b in floor_beacon_floor_matrix.index]
            second_order_od_matrix = pd.concat([
                second_order_od_matrix, floor_beacon_floor_matrix
            ])

        self.transition_matrix = second_order_od_matrix.div(second_order_od_matrix.sum(axis=1), axis=0)
        return self

    def _set_possible_starting_floor_list(self, possible_starting_floor_list: list[str]):
        self.possible_starting_floor_list = possible_starting_floor_list
        starting_weights = self.transition_matrix.loc[self.possible_starting_floor_list].sum(axis=1).values
        self.starting_probs = starting_weights / starting_weights.sum()

    def _choose_starting_floor(self):
        return str(np.random.choice(self.possible_starting_floor_list, p=self.starting_probs))

    def simulate_one_path(
        self,
        absorbing_floor_set: set[str],
        min_path_length: int,
        max_path_length: int
    ):
        path = []

        while len(path) <= min_path_length:
            starting_floor = self._choose_starting_floor()
            path = [starting_floor]
            current = starting_floor

            for _ in range(max_path_length):
                probs = self.transition_matrix.loc[current, :].values

                next_step = np.random.choice(self.transition_matrix.columns, p=probs)

                path.append(next_step)

                if next_step in self.beacon_list:
                    next_step = f"{current}_{next_step}"

                current = next_step

                if current in absorbing_floor_set:
                    break

        return tuple(path)

    def simulate_n_path(
        self,
        n_simulations: int,
        possible_starting_floor_list: list[str],
        absorbing_floor_set: set[str],
        min_path_length: int,
        max_path_length: int
    ) -> list[tuple[str]]:
        self._set_possible_starting_floor_list(possible_starting_floor_list=possible_starting_floor_list)
        return [
            self.simulate_one_path(
                absorbing_floor_set=absorbing_floor_set,
                min_path_length=min_path_length,
                max_path_length=max_path_length
            ) for _ in range(n_simulations)
        ]
