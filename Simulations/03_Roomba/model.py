from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent import Roomba, ObstacleAgent, DirtAgent, ChargingStation

class CleaningModel(Model):
    def __init__(self, 
                 num_agents=5,
                 num_dirt=5,
                 num_obstacles=10,
                 width=50,
                 height=50):
        self.num_agents = num_agents
        self.num_dirt = num_dirt
        self.num_obstacles = num_obstacles

        self.grid = MultiGrid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        
        self.running = True
        self.dirt_count = num_dirt

        self.datacollector = DataCollector( 
            agent_reporters = {
            "Steps": lambda a: a.steps_taken
            if isinstance(a, Roomba) else 0
            }
        )

        positions = self.random.sample(
            tuple((x, y) for x in range(width) for y in range(height)),
            k = self.num_dirt + self.num_obstacles + self.num_agents
        )

        for _ in range(num_agents):
            pos = positions.pop()
            roomba = Roomba(f"r-{pos}", self)
            station = ChargingStation(f"s-{pos}", self)
            self.grid.place_agent(roomba, pos)
            self.grid.place_agent(station, pos)
            self.schedule.add(roomba)

        for _ in range(num_dirt):
            pos = positions.pop()
            dirt = DirtAgent(f"d-{pos}", self)
            self.grid.place_agent(dirt, pos)
        
        for _ in range(num_obstacles):
            pos = positions.pop()
            obstacle = ObstacleAgent(f"o-{pos}", self)
            self.grid.place_agent(obstacle, pos)

        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        if self.dirt_count == 0:
            self.running = False