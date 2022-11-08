import mesa
from dirty_agent import *


class RoombaAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.status = True
        self.moves = 0
        self.cleanedCells = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.moves += 1

    def clean(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            for i in cellmates:
                if type(i) == DirtyAgent and i.cleaned == False:
                    i.dirty = True
                    self.cleanedCells += 1

    def step(self):
        self.clean()
        self.move()
