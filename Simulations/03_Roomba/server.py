from model import CleaningModel
from mesa.visualization import CanvasGrid, ChartModule, BarChartModule
from mesa.visualization import ModularServer, Slider
from portrayals import portrayals, default_portrayal

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Server to visualize mesa simulation'
    )

    # Width and height are command line arguments, because the canvas grid
    # dimensions cannot be changed after the server is launched in the 
    # mesa visualization module.
    parser.add_argument(
        '--width',
        type=int,
        nargs='?',
        default=25,
        help='Width of the grid'
    )

    parser.add_argument(
        '--height',
        type=int,
        nargs='?',
        default=25,
        help='Height of the grid'
    )

    args = parser.parse_args()

    if args.width < 15 or args.height < 15:
        raise ValueError("Width and height must be at least 15")

    def agent_portrayal(agent):
        if agent is None: return None
        p = portrayals.get(type(agent), default_portrayal).copy()
        return p 

    model_params = {
        "num_agents": Slider(
            "Number of Agents",
            5, 
            1, 
            10, 
            1
        ),
        "dirt_density": Slider(
            "Dirt Density",
            0.1, 
            0.05, 
            0.4, 
            0.05
        ),
        "obstacle_density": Slider(
            "Obstacle Density",
            0.1, 
            0.05, 
            0.4, 
            0.05
        ),
        "width": args.width, 
        "height": args.height,
        "limit": Slider(
            "Step Limit", 
            500, 
            100, 
            1000, 
            100
        )
    }

    grid = CanvasGrid(
        agent_portrayal, 
        model_params["width"],
        model_params["height"],
        500,
        500
    )

    bar_chart = BarChartModule(
        [{"Label":"Steps", "Color":"#00AA00"}], 
        scope="agent", sorting="ascending", sort_by="Steps"
    )

    scatter_plot = ChartModule(
        [{"Label": "Dirt", "Color": "grey"}],
        data_collector_name="datacollector"
    )

    server = ModularServer(
        CleaningModel, 
        [grid, bar_chart, scatter_plot],
        "Super Roomba 3: Electric Boogaloo",
        model_params
    )
                 
    server.port = 8521
    try: 
        server.launch()
    except:
        raise("Unable to launch server. Make sure port 8521 is free.")