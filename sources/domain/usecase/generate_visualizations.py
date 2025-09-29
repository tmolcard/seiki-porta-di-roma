from sources.domain.entity.simulation_to_sankey_diagram import simulation_to_sankey_diagram
from sources.domain.port.filesystem_handler import FilesystemHandler


def generate_visualizations(filesystem_handler: FilesystemHandler, simulation_id: str, floor: str = None) -> str:
    df_simulation = filesystem_handler.load_simulation(simulation_id=simulation_id)

    viz_name = f"sankey_diagram_floor_{floor}" if floor else "sankey_diagram"

    fig = simulation_to_sankey_diagram(df_simulation, filter_floor=floor)
    filesystem_handler.save_visualization(fig, name=viz_name, visualization_id=simulation_id)

    return fig.to_html()
