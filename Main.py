from Classify import Classify
from Fetch import Fetch
import json, requests

# Main class to fetch one tweet and classify
class Main():
    url = None
    tweets = None
    fetch = None
    parse = None
    classifier = Classify("trainSet.json", "dictionary.json", "./liveTrain.json", "./pastTrain.json", "./liveTrainDic.json", "./pastTrainDic.json")
    fetch = Fetch ()
    print(classifier.classifyOne(fetch.tweets[0],1,1))


    # Load parsed tweets
    def loadTweets(self):
        json_data = open("parsedTweets.json")
        data = json.load(json_data)
        return data

    # Function to check tweet exists
    def getTweet(self, tweet_id):
        for line in self.tweets:
            if int(line['id']) == tweet_id:
                return line 

    # Save a tweet in json file
    def save(self):
        with open('./parsedTweets.json', 'w+') as outfile:
            outfile.write(json.dumps(self.tweets, indent=4))

