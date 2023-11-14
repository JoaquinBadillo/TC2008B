from typing import Tuple, Callable
from mesa import Agent


class Roomba(Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.explored_cells = set()
        self.station_path = []
        self.free_path = False
        self.other_agent = None
        self.steps_taken = 0
        self.battery = 100
        self.low_battery = False

    def decide(self) -> Callable[[], bool]:
        has_obstacle = lambda cell: any(
            isinstance(agent, ObstacleAgent) for agent in 
            self.model.grid.get_cell_list_contents([cell])
        )

        has_roomba = lambda cell: any(
            isinstance(agent, Roomba) for agent in 
            self.model.grid.get_cell_list_contents([cell])
        )

        
        cells = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )

        available_cells = tuple(filter(
            lambda cell: not has_obstacle(cell) and 
                         not has_roomba(cell),
            cells
        ))

        if self.battery <= len(self.station_path) * 1.2:
            self.low_battery = True

        if self.free_path:
            self.free_path = False
            if not available_cells:
                agent = self.other_agent
                self.other_agent = None
                return lambda: self.ask_to_move(agent)

            return lambda: self.move(self.random.choice(tuple(available_cells)))

        elif self.low_battery:
            if not self.station_path:
                return lambda: self.recharge()
                
            return lambda: self.go_charge()
        
        dirt = next(
            filter(
                lambda agent: isinstance(agent, DirtAgent),
                self.model.grid.get_cell_list_contents([self.pos])
            ),
            None
        )

        if dirt is not None:
            return lambda: self.clean(dirt)
        
        return lambda: self.explore(available_cells)

    def explore(self, free_cells) -> bool:
        if not free_cells:
            return False
        
        dirt_cell = None

        for cell in free_cells:
            if any(isinstance(agent, DirtAgent) for agent in
                self.model.grid.get_cell_list_contents([cell])):
                
                dirt_cell = cell
                break
        
        if dirt_cell:
            return self.move(dirt_cell)

        new_cells = tuple(filter(
            lambda cell: cell not in self.explored_cells,
            free_cells
        ))

        if new_cells:
            return self.move(self.random.choice(new_cells))
        
        return self.move(self.random.choice(free_cells))

    def clean(self, dirt: "DirtAgent") -> bool:
        self.model.grid.remove_agent(dirt)
        self.model.dirt_count -= 1

        return True

    def ask_to_move(self, agent: "Agent") -> bool:
        print(f"{self.unique_id}: Beep Beep {agent.unique_id}")
        agent.free_path = [True, self]
        return True

    def recharge(self) -> bool:
        print(f"{self.unique_id} @ {self.battery}% is charging")
        self.battery = self.battery + 5
        print(f"{self.unique_id} @ {self.battery}% is charging")
        
        if self.battery >= 100:
            self.low_battery = False

        return False
    
    def go_charge(self) -> bool:
        prev = self.station_path.pop()
        otherAgent = next(
            filter(
                lambda x: isinstance(x, Roomba),
                self.model.grid.get_cell_list_contents([prev])
            ),
            None
        )
        
        if otherAgent is not None:
            return self.ask_to_move(otherAgent)

        return self.move(prev, track_path=False)
    
    def move(self, pos: Tuple[int], track_path = True) -> bool:
        if track_path: self.station_path.append(self.pos)
        self.model.grid.move_agent(self, pos) 
        self.explored_cells.add(self.pos)       
        return True

    def step(self):
        if self.battery <= 0:
            return
        
        decision = self.decide()
        self.battery -= (1 if decision() else 0)

        
class ObstacleAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class DirtAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class ChargingStation(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass