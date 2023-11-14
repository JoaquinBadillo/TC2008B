from mesa import Agent

# Da rules (each tuple represets the top neighbours from left to right)
cases = {
    (0, 0, 0): "Dead",
    (0, 0, 1): "Alive",
    (0, 1, 0): "Dead",
    (0, 1, 1): "Alive",
    (1, 0, 0): "Alive",
    (1, 0, 1): "Dead",
    (1, 1, 0): "Alive",
    (1, 1, 1): "Dead",
}

class Cell(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Dead"
        self._next_condition = None

    def step(self):
        if self.condition == "Alive":
            return
        
        # Neighbors are ordered left to right and bottom to top (according to some logs).
        # if mesa changes the behaviour of their interface I will be sad...
        # Also, use tuple because these can be hashed (unlike lists)
        top_neighbors = tuple(
            int(neighbor.condition == "Alive") for neighbor in 
            self.model.grid.iter_neighbors(self.pos, True)
            if neighbor.pos[1] > self.pos[1]
        )

        # Update the "next condition" to avoid updating the state too soon.
        self._next_condition = cases.get(top_neighbors, "Dead")

    def advance(self):
        # Advance updates the real condition
        if self._next_condition is not None:
            self.condition = self._next_condition
