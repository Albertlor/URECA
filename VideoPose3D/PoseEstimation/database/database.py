import numpy as np
import json


class Database:
    """
    This module has the functionalities as follows:
    1. Read the npy dataset from local file
    2. Read the csv dataset from local file
    3. Write the result from Calculation.py into JSON file
    4. Write the result from Calculation.py into csv file
    """
    def __init__(self, npyPath=None, jsonPathDict=None, individual=1):
        self.npyPath = npyPath
        self.jsonPathDict = jsonPathDict
        self.individual = individual

    def read_npy_data(self):
        npy_file = np.load(self.npyPath)
        return npy_file

    def read_json_data(self):
        json_file_dict = {}
        count = 0
        for jsonPath in self.jsonPathDict.values():
            try:
                with open(f'{jsonPath}') as f:
                    json_file = json.load(f)
                    key = list(self.jsonPathDict.keys())[count]
                    json_file_dict[key] = json_file
                count += 1
            except FileNotFoundError:
                print('This file does not exist!')
                break
        return json_file_dict

    def write_json_data(self, json_file, json_filename):
        with open(f'./database/json_data/Individual_{self.individual}/{json_filename}.json', 'w') as outfile:
            outfile.write(json_file)
        

    
