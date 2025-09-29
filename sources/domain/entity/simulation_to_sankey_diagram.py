

import pandas as pd
import plotly.graph_objects as go


def prepare_sankey_data(
    df_simulation: pd.DataFrame, filter_floor: str = None
) -> tuple[list, pd.Series, pd.Series, pd.Series]:
    df_simulation["pairs"] = df_simulation["sequence"].apply(
        lambda sequence: [(sequence[i], sequence[i+1]) for i in range(len(sequence)-1)]
    )

    df_pairs_count = (
        df_simulation[["pairs", "count"]]
        .explode("pairs")
        .groupby("pairs")["count"].sum()
        .reset_index()
    )

    if filter_floor is not None:
        df_pairs_count = df_pairs_count[
            df_pairs_count["pairs"].apply(lambda x: filter_floor in x)
        ]

    nodes = sorted(set.union(*df_pairs_count["pairs"].apply(set).to_list()))
    node_index = {n: i for i, n in enumerate(nodes)}

    # Build Sankey data
    source = df_pairs_count["pairs"].apply(lambda x: node_index[x[0]])
    target = df_pairs_count["pairs"].apply(lambda x: node_index[x[1]])
    value = df_pairs_count["count"]
    return nodes, source, target, value


def simulation_to_sankey_diagram(df_simulation: pd.DataFrame, filter_floor: str = None) -> go.Figure:
    nodes, source, target, value = prepare_sankey_data(df_simulation=df_simulation, filter_floor=filter_floor)

    # Create Sankey diagram
    return go.Figure(
        data=[
            go.Sankey(
                node={
                    'pad': 15,
                    'thickness': 20,
                    'line': {'color': "black", 'width': 0.5},
                    'label': nodes,
                },
                link={
                    'source': source.to_list(),
                    'target': target.to_list(),
                    'value': value.to_list()
                }
            )
        ],
        layout={
            "title_text": "Sankey Diagram of Simulated Paths"
        }
    )
