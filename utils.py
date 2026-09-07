import json
# function to load and save data from/in .json file
def load_data():
    with open('patients.json', 'r') as file:
        data = json.load(file)
    return data

def save_data(data):
    with open('patients.json', 'w') as file:
        json.dump(data, file)
