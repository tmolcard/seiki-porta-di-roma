import json
import os

DATA_PATH = os.getenv("DATA_PATH", default='/home/theophile/ad-portam-ori/data')

MODEL_ID = os.getenv("MODEL_ID", default="default")
SIMULATION_ID = os.getenv("SIMULATION_ID", default="default")
N_SIMULATIONS = int(os.getenv("N_SIMULATIONS", default="100000"))
POSSIBLE_STARTING_FLOOR_LIST = json.loads(
    os.getenv("POSSIBLE_STARTING_FLOOR_LIST", default='["outdoor", "-1"]')
)
MIN_PATH_LENGTH = int(os.getenv("MIN_PATH_LENGTH", default="3"))
MAX_PATH_LENGTH = int(os.getenv("MAX_PATH_LENGTH", default="16"))
