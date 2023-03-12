# ------------------------------- Import ------------------------------- #
import json
import os
from settings import config

# -------------------------------- Utils ------------------------------- #
def get_data():
    with open(os.path.join(config.BASE_DIR, "data.json"), "r") as data_file:
        return json.load(data_file)

def update_data(data):
    with open(os.path.join(config.BASE_DIR, "data.json"), "w") as data_file:
        json.dump(data, data_file)
