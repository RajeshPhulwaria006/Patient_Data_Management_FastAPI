import json
# function to load and save data from/in .json file
def load_data():
    """Function to load patient's data"""
    with open('backend/patients.json', 'r') as file:
        data = json.load(file)
    return data

def save_data(data):
    """Function to save patient's data"""
    with open('backend/patients.json', 'w') as file:
        json.dump(data, file)
