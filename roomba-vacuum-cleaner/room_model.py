import mesa
import numpy as np
from roomba_agent import RoombaAgent
from dirty_agent import DirtyAgent


def time_to_end(model):
    currentMoves = 0
    for agent in model.schedule.agents:
        if type(agent) == RoombaAgent:
            currentMoves = agent.moves
    return model.moves - currentMoves


class RoomModel(mesa.Model):

    def __init__(self, agents, rows, columns, x_start, y_start, percentage_dirty_cells, moves):
        self.num_agents = agents
        self.grid = mesa.space.MultiGrid(rows, columns, False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.moves = moves
        self.timeToEnd = 0
        self.clean_percentage = 0

        # Create dirty cells
        coordinates = np.random.choice([False, True],
                                       size=(rows, columns),
                                       p=[1-(percentage_dirty_cells/100), percentage_dirty_cells/100])
        index = 0
        for row in range(rows):
            for col in range(columns):
                if (coordinates[row][col]):
                    index += 1
                    d = DirtyAgent(agents + index, self)
                    self.schedule.add(d)
                    self.grid.place_agent(d, (row, col))

        self.dirtyCells = index

        # Create roomba agents
        for i in range(self.num_agents):
            a = RoombaAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (x_start, y_start))

        self.datacollector = mesa.DataCollector(
            {
                "Celdas sucias": "1"
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.timeToEnd = time_to_end(self)

        if RoomModel.movementsUsed(self):
            self.running = False
        if RoomModel.cleanRoom(self):
            self.running = False
        RoomModel.getCleanPercentage(self)

    @staticmethod
    def movementsUsed(model):
        return [1 for agent in model.schedule.agents if type(agent) == RoombaAgent and agent.moves == model.moves-1]

    @staticmethod
    def cleanRoom(model):
        cleanedCells = 0
        for agent in model.schedule.agents:
            if type(agent) == DirtyAgent and agent.cleaned:
                cleanedCells += 1
        return cleanedCells == model.dirtyCells

    @staticmethod
    def getCleanPercentage(model):
        cleanedCells = 0
        for agent in model.schedule.agents:
            if type(agent) == DirtyAgent and agent.cleaned:
                cleanedCells += 1
        model.clean_percentage = (cleanedCells / model.dirtyCells) * 100

