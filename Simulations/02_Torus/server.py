from mesa.visualization import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization import ModularServer
from mesa.visualization import Slider

from model import GameOfLife

COLORS = {"Alive": "#000000", "Dead": "#FFFFFF"}

def game_of_life_portrayal(cell):
    if cell is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = cell.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[cell.condition]

    return portrayal

canvas_element = CanvasGrid(game_of_life_portrayal, 50, 50, 500, 500)

# The chart will plot the number of each type of cell over time.
cell_chart = ChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)

# The pie chart will plot the number of each type of cell at the current step.
pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)

# The model parameters will be set by sliders controlling the initial density
model_params = {
    "height": 50,
    "width": 50,
    "density": Slider("cell density", 0.1, 0.01, 0.5, 0.01),
}

# The modular server is a special visualization server that allows multiple
# elements to be displayed simultaneously, and for each of them to be updated
# when the user interacts with them.
server = ModularServer(
    GameOfLife, [canvas_element, cell_chart, pie_chart], "Game of Life 2.0", model_params
)

server.launch()