import mesa


class DirtyAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cleaned = False

    def step(self):
        self.status = False
