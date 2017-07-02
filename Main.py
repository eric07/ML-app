from Classify import Classify
from Fetch import Fetch
import json, requests

class Main():
    url = None
    tweets = None
    fetch = None
    parse = None
    classifier = Classify("trainSet.json", "dictionary.json", "./liveTrain.json", "./pastTrain.json", "./liveTrainDic.json", "./pastTrainDic.json")
    fetch = Fetch ()
    print (fetch.tweets[0])
    print("Tweet is " + classifier.classifyOne(fetch.tweets[0],1,1))

    def joinJsons(self, tweets):
        for line in tweets:
            self.tweets.append(line)
        self.tweets = self.parse.sortTweets(self.tweets)

    def loadTweets(self):
        json_data = open("parsedTweets.json")
        data = json.load(json_data)
        return data

    def getTweet(self, tweet_id):
        for line in self.tweets:
            if int(line['id']) == tweet_id:
                return line 

    def save(self):
        with open('./parsedTweets.json', 'w+') as outfile:
            outfile.write(json.dumps(self.tweets, indent=4))

    def send(self, tweet_id):
        tweet = self.getTweet(int(tweet_id))
        headers = {'content-type': 'application/json'}
        r = requests.post(self.url, data = json.dumps(tweet), headers=headers)
        print(r.text)

    def sendTweet(self, tweet):
        headers = {'content-type': 'application/json'}
        r = requests.post(self.url, data = json.dumps(tweet), headers=headers)
        print(r.text)

    def getMinId(self):
        return self.tweets[0]['id']

    def sendAll(self):
        for line in self.tweets:
            self.send(line['id'])
            print("Sent %d" % line['count'])      