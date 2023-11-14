from model import CleaningModel
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer
from portrayals import portrayals, default_portrayal

def agent_portrayal(agent):
    if agent is None: return None
    p = portrayals.get(type(agent), default_portrayal).copy()
    return p 


model_params = {
    "num_agents":5,
    "num_dirt": 10,
    "num_obstacles": 8,
    "width":25, 
    "height":25
}

grid = CanvasGrid(agent_portrayal, 25, 25, 500, 500)

bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps"
)

server = ModularServer(
    CleaningModel, 
    [grid, bar_chart],
    "Super Roomba 3: Electric Boogaloo",
    model_params
)
                       
server.port = 8521
server.launch()