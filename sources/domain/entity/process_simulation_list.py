from collections import Counter

import pandas as pd

from sources.domain.entity.add_sequence_typology import add_sequence_typology


def simulation_list_to_count_dataframe(path_simulation_list: list[tuple[str]]) -> pd.DataFrame:
    counter = Counter(path_simulation_list)
    return (
        pd.DataFrame
        .from_dict(counter, orient='index')
        .reset_index()
        .rename(columns={'index': 'sequence', 0: 'count'})
    )


def process_simulation_list(path_simulation_list: list[tuple[str]], floor_list: list[str]) -> pd.DataFrame:
    df_count_simulations = simulation_list_to_count_dataframe(path_simulation_list)
    df_count_simulations["floor_sequence"] = df_count_simulations["sequence"].apply(
        lambda x: tuple(s for s in x if s in floor_list)
    )

    df_count_simulations = add_sequence_typology(df_count_simulations)
    return df_count_simulations
