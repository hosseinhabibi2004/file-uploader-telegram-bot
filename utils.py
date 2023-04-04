# ------------------------------- Import ------------------------------- #
import json
import os
from settings import config

# -------------------------------- Utils ------------------------------- #
def get_data():
    with open(os.path.join(config.BASE_DIR, "data.json"), "r") as data_file:
        data = json.load(data_file)

    data['USERS'] = set(data['USERS'])
    data['ADMINS'] = set(data['ADMINS'])
    for channel in data['CHANNELS']:
        data['CHANNELS'][channel] = set(data['CHANNELS'][channel])
    for file in data['FILES']:
        data['FILES'][file]['users'] = set(data['FILES'][file]['users'])
    
    return data

def update_data(data):
    data['USERS'] = list(data['USERS'])
    data['ADMINS'] = list(data['ADMINS'])
    for channel in data['CHANNELS']:
        data['CHANNELS'][channel] = list(data['CHANNELS'][channel])
    for file in data['FILES']:
        data['FILES'][file]['users'] = list(data['FILES'][file]['users'])
    
    with open(os.path.join(config.BASE_DIR, "data.json"), "w") as data_file:
        json.dump(data, data_file)
