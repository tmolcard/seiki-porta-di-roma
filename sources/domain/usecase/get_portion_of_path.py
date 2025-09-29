import logging

from sources.domain.port.filesystem_handler import FilesystemHandler


def get_portion_of_path(
    filesystem_handler: FilesystemHandler, floor: str, beacon_pairs: list[tuple[str, str]], simulation_id: str
) -> tuple[int, int, float]:
    df_simulation = filesystem_handler.load_simulation(simulation_id=simulation_id)

    sub_sequence_set = set.union(
        {(start, floor, end) for start, end in beacon_pairs},
        {(end, floor, start) for start, end in beacon_pairs}
    )

    def is_in_sequence(sequence):
        for i in range(int((len(sequence) - 1) / 2 - 1)):
            if (sequence[2 * i + 1], sequence[2*i + 2], sequence[2*i + 3]) in sub_sequence_set:
                return True
        return False

    df_simulation["is_in_sequence"] = df_simulation["sequence"].apply(is_in_sequence)

    result = df_simulation.groupby("is_in_sequence")["count"].sum()

    n_true = result[True]
    n_false = result[False]

    total = n_true + n_false
    proportion = n_true / total

    logging.info(f"Proportion of paths going through the beacon pairs on floor {floor}.")
    logging.info(f"For {total} people entering the building {n_true} would pass by those path.")
    logging.info(f"This represents {proportion:.2%}")

    return int(n_true), int(total), proportion
