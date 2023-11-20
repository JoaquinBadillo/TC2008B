from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent import Roomba, ObstacleAgent, DirtAgent, ChargingStation

class CleaningModel(Model):
    def __init__(self, 
                 num_agents=5,
                 dirt_density=0.2,
                 obstacle_density=0.2,
                 width=50,
                 height=50,
                 limit=500):

        self.grid = MultiGrid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        
        self.running = True
        self.dirt_count = int(dirt_density * width * height)
        self.obstacle_count = int(obstacle_density * width * height)
        self.limit = limit

        self.steps = 0

        self.datacollector = DataCollector( 
            agent_reporters = {
            "Steps": lambda a: a.steps_taken
                if isinstance(a, Roomba) else 0
            },
            model_reporters = {
                "Dirt": lambda m: m.dirt_count
            }
        )

        positions = None

        # Manage both the single and multiple agent case.
        # Used sample to get unique positions for each agent. 
        if num_agents == 1:
            positions = self.random.sample(
                tuple((x, y) for x in range(width) if x != 1 
                             for y in range(height) if y != 1),
                k = self.dirt_count + self.obstacle_count
            )

            positions.append((1, 1))
        else:
            positions = self.random.sample(
                tuple((x, y) for x in range(width) for y in range(height)),
                k = self.dirt_count + self.obstacle_count + num_agents
            )

        # Initilize the roombas (using the position list as a stack)
        # Roombas start at the same position as their charging station
        for _ in range(num_agents):
            pos = positions.pop()
            roomba = Roomba(f"r-{pos}", self)
            station = ChargingStation(f"s-{pos}", self)
            self.grid.place_agent(roomba, pos)
            self.grid.place_agent(station, pos)
            self.schedule.add(roomba)

        # Initialize the dirt cells
        for _ in range(self.dirt_count):
            pos = positions.pop()
            dirt = DirtAgent(f"d-{pos}", self)
            self.grid.place_agent(dirt, pos)
        
        # Initialize the obstacle cells
        for _ in range(self.obstacle_count):
            pos = positions.pop()
            obstacle = ObstacleAgent(f"o-{pos}", self)
            self.grid.place_agent(obstacle, pos)

        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.steps += 1

        # Finish the simulation either by limit or completion of the objective.
        if self.dirt_count == 0 or self.steps >= self.limit:
            self.running = False