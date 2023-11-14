import mesa
from mesa import Model, DataCollector
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation 

from agent import Cell

from functools import reduce

class GameOfLife(Model):
    def __init__(self, height=50, width=50, density=0.65):
        # Grid Parameters
        self.height = height
        self.width = width

        # Special comparators to check the top neighbors
        # The keys represent the vertical position of a cell
        self.comparators = {
            0: lambda x: x[1] == 1,
            height - 1: lambda x: x[1] == 0,
        }

        self.schedule = SimultaneousActivation(self)
        self.grid = SingleGrid(height, width, torus=True)

        self.datacollector = DataCollector(
            {
                "Dead": lambda m: self.count_type(m, "Dead"),
                "Alive": lambda m: self.count_type(m, "Alive"),
            }
        )
        
        # Create cells with the given alive density
        for _, (x, y) in self.grid.coord_iter():
            new_cell = Cell((x, y), self)

            if self.random.random() < density:
                new_cell.condition = "Alive"

            self.grid.place_agent(new_cell, (x, y))
            self.schedule.add(new_cell)
        
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        
    @staticmethod
    def count_type(model, cell_condition):
        # Ah yes, functional patterns
        return reduce(
            lambda x, y: x + 1 if y.condition == cell_condition else x, 
            model.schedule.agents, 
            0
        )
