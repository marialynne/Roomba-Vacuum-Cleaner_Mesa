from room_model import *
import matplotlib.pyplot as plt
import pandas as pd
from mesa.visualization.UserParam import UserSettableParameter

PIXELS_GRID = 500

""" 
params = {
    "agents": 1,
    "rows": 10,
    "columns": 10,
    "x_start": 0,
    "y_start": 0,
    "percentage_dirty_cells": 45,
    "moves": 25
}
results = mesa.batch_run(
    RoomModel,
    parameters=params,
    iterations=5,
    max_steps=100,  # time
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
) """


def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": "Roomba",
        "Color": "blue",
        "r": 0.8,
    }

    if type(agent) == DirtyAgent:
        portrayal["Color"] = "red"
        portrayal["Layer"] = "Dirty"

    if type(agent) == DirtyAgent and agent.cleaned == True:
        portrayal["Color"] = "green"
        portrayal["Layer"] = "Cleaned"

    if type(agent) == RoombaAgent and agent.status == False:
        portrayal["Color"] = "black"
        portrayal["Filled"] = True

    return portrayal


simulation_params = {
    "agents": UserSettableParameter(
        "number",
        "Number of Agents",
        5,
        description="Number of Agents",
    ),
    "rows": 25,
    "columns": 25,
    "moves": UserSettableParameter(
        "number",
        "Moves",
        25,
        description="Number of moves",
    ),
    "percentage_dirty_cells": UserSettableParameter(
        "slider",
        "Percentage of dirty cells",
        value=45,
        min_value=1,
        max_value=100,
        step=1
    ),
    "x_start": 0,
    "y_start": 0
}


def get_clean_percentage(model):
    return f"Percentage of clean cells: {model.clean_percentage:.2f} %"


def get_current_move(model):
    return f"Time to finish: {model.timeToEnd}"


grid = mesa.visualization.CanvasGrid(
    agent_portrayal, simulation_params["rows"], simulation_params["columns"], 600, 600)

server = mesa.visualization.ModularServer(
    RoomModel, [
        grid, get_clean_percentage, get_current_move], "Roomba Vacuum Cleaner", simulation_params
)

server.port = 8521
server.launch()
