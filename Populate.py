from twitter import *
import json
from Parse import Parse
from datetime import datetime
import time
import requests
from Model import Model
import sys

class Populate():
    def __init__(self, URL):
        self.parse = Parse()
        self.url = URL
        # Create instance of model class to import teams json
        self.model = Model("trainSet.json", "dictionary.json", "./liveTrain.json", "./pastTrain.json", "./liveTrainDic.json", "./pastTrainDic.json")
        self.livetrain = self.model.load("liveTrain.json")
        self.pasttrain = self.model.load("pastTrain.json")
        # Push teams to server
        self.upload_live(self.livetrain)
        self.upload_past(self.pasttrain)
        # Get tweets from twitter API and push them to server
        

    # Functions to communicate with server
    # Move all live training data to server
    def upload_live (self, document):
        headers = {'content-type': 'application/json'}
        r = requests.post(self.url + "api/training/create/live", data= json.dumps(document), headers= headers)
        print("document upload", r, r.text)

    def upload_past (self, document):
        headers = {'content-type': 'application/json'}
        r = requests.post(self.url + "api/training/create/past", data= json.dumps(document), headers= headers)
        print("document upload", r, r.text)
    

production = "http://atrato.herokuapp.com/"
local = "http://localhost:3000/"

if __name__ == '__main__':
    pop = Populate(local)
