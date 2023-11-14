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
        self.condition = "Dead" # Dead by default
        self._next_condition = None

    def step(self):
        # Function to check who is a top neighbor (depends on pos)
        # The default comparator returns true if the y-position is greater 
        heightComparator = self.model.comparators.get(
            self.pos[1], lambda x: x[1] > self.pos[1]
        )

        # Use list comprehension as a map and filter.
        # Tuple is still required due to the hash function.
        top_neighbors = tuple(
            int(neighbor.condition == "Alive") for neighbor in 
            self.model.grid.iter_neighbors(self.pos, True)
            if heightComparator(neighbor.pos)
        )

        # Update the "next condition" to avoid updating the state too soon.
        self._next_condition = cases.get(top_neighbors)

    def advance(self):
        # Update the actual state of the cell
        if self._next_condition is not None:
            self.condition = self._next_condition