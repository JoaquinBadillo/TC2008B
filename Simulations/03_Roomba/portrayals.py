from agent import Roomba, ObstacleAgent, DirtAgent, ChargingStation

# Dictionary that maps types to portrayals (which are dictionaries themselves)
portrayals = {
    ObstacleAgent: {
        "Shape": "rect",
        "Filled": "true",
        "Color": "black",
        "Layer": 1,
        "w": 1,
        "h": 1
    },
    DirtAgent: {
        "Shape": "circle",
        "Filled": "true",
        "Color": "grey",
        "Layer": 0,
        "r": 0.5
    },
    Roomba: {
        "Shape": "circle",
        "Filled": "true",
        "Color": "black",
        "Layer": 1,
        "r": 0.3
    
    },
    ChargingStation: {
        "Shape": "circle",
        "Filled": "true",
        "Color": "green",
        "Layer": 0,
        "r": 0.75
    },
}

default_portrayal = {
    "Color": "black",
    "Shape": "rect",
    "Filled": "true",
    "Layer": 0,
    "w": 1,
    "h": 1
}