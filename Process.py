from Main import Main
from Classify import Classify
import json
class Process():
    """docstring for Process"""
    def __init__(self):
        self.main = Main("http://ml-research.herokuapp.com/upload", False)
        self.classifier = Classify("trainSet.json", "dictionary.json", "./liveTrain.json", "./pastTrain.json", "./liveTrainDic.json", "./pastTrainDic.json")
        json_data = open("testSet.json")
        self.tweets = json.load(json_data)
        for tweet in self.tweets:
            r = self.classifier.classify(tweet['text'])
            if r == 'live':
                color = "#ECF0F1"
                if "KICK-OFF" in tweet['text']:
                    color = "#3498DB"
                if "GOAL" in tweet['text']:
                    color = "#E74C3C"
                if "HALF-TIME" in tweet['text']:
                    color = "#E67E22"
                if "PENALTY" in tweet['text']:
                    color = "#2ECC71"
                if "SUB" in tweet['text']:
                    color = "#34495E"
                if "FULL-TIME" in tweet['text']:
                    color = "#9B59B6"
                js = {
                    "py_time": tweet['py_time'],
                    "text": tweet['text'],
                    "tw_id": tweet['id'],
                    "classId" : 0,
                    "color" : color,
                    "avatar" : tweet['avatar']
                }
                self.main.sendTweet(js)

if __name__ == '__main__':
    process = Process()
