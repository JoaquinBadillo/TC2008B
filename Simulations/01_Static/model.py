import mesa
from mesa import Model, DataCollector
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation 

from agent import Cell

from functools import reduce

class GameOfLife(Model):
    def __init__(self, height=50, width=50, density=0.65):
        # Count is used to count the number of steps
        self.count = 0
        self.height = height

        self.schedule = SimultaneousActivation(self)
        self.grid = SingleGrid(height, width, torus=False)

        self.datacollector = DataCollector(
            {
                "Dead": lambda m: self.count_type(m, "Dead"),
                "Alive": lambda m: self.count_type(m, "Alive"),
            }
        )

        for _, (x, y) in self.grid.coord_iter():
            new_cell = Cell((x, y), self)

            # First check height (short circuit if not on top), 
            # then use the probability density
            if y == height - 1 and self.random.random() < density:
                new_cell.condition = "Alive"

            self.grid.place_agent(new_cell, (x, y))
            self.schedule.add(new_cell)
                
        # Use running variable to check if simulation should halt
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.count += 1

        # Stop simulation when the last row is reached
        if self.count == self.height - 1:
            self.running = False
        
    @staticmethod
    def count_type(model, cell_condition):
        return reduce(
            lambda x, y: x + 1 if y.condition == cell_condition else x, 
            model.schedule.agents, 
            0
        )
