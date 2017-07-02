import json
import nltk
import re

class Model():
    def __init__(self, trainSet, dictionary, liveSet, pastSet, liveDicSet, pastDicSet):
        self.voc = []
        #self.model = Model("trainSet.json", "dictionary.json", "./liveTrain.json", "./pastTrain.json", "./liveTrainDic.json", "./pastTrainDic.json")
        #Get training set numbers
        self.tweets = self.load(trainSet)
        self.dictionary=self.load(dictionary)
        self.total, self.live, self.past = self.numberTweets()
        
        #convert numbers to prior probabilities
        self.pLive = round(self.live / float(self.total), 2)
        self.pPast = round(self.past / float(self.total), 2)
        
        #To hold bag of words from traning tweets
        self.bagLive = [] 
        self.bagPast = []
        self.totalLive = 0
        self.totalPast = 0
        self.liveSet = liveSet
        self.pastSet = pastSet
        
        self.bagOfWords()
        self.calcProb()

        # # print(self.bagLive)

    
    def load(self, fileName):
        json_data = open(fileName)
        data = json.load(json_data)
        return data

    # get total number of tweets, live and past and total
    def numberTweets(self):
        count = 0
        live = 0
        for line in self.tweets:
            count += 1
            if line['classId'] == 0:
                live += 1
        return (count, live, count-live)


    # add word to live vocabulary
    def insertLive(self, word):
        #to avoid articles, small words etc
        if len(word) < 4:
            return
        # if word aleady exists just increment the count
        for line in self.bagLive:
            if line[0] == word:
                line[1] += 1
                self.totalLive += 1
                return
        # if word does not exist add with count = 1
        self.bagLive.append([word, 1])
        self.totalLive += 1

    # add word to past vocabulary
    def insertPast(self, word):
        #to avoid articles, small words etc
        if len(word) < 4:
            return
        # if word aleady exists just increment the count
        for line in self.bagPast:
            if line[0] == word:
                line[1] += 1
                self.totalPast += 1
                return
        # if word does not exist add with count = 1
        self.bagPast.append([word, 1])
        self.totalPast += 1

    #add word to overall vocabulary 
    def insertVoc(self, word):
        #to avoid articles, small words etc
        if len(word) < 4:
            return
        for line in self.voc:
            if line[0] == word:
                line[1] += 1
                return
        self.voc.append([word, 1])

    # Create the 2 bags (past + live) containing words, their  count and overall probability
    def bagOfWords(self):
        for line in self.tweets:
            # line['text'], hashTags, links, ref, timeStamp = self.extract(line['text'])

            for word in nltk.word_tokenize(line['text']):
                word = word.lower()
                if line['classId'] == 0:
                    self.insertLive(word)
                else:
                    self.insertPast(word)
                #Insert every word in vocabulary
                self.insertVoc(word)

    # Populate probabilities of words
    def calcProb(self):
        for i in xrange(len(self.bagLive)):
            # +1 for the laplace correction
            prob = (self.bagLive[i][1] + 1) / float(len(self.voc) + self.totalLive)
            self.bagLive[i].append(prob)

        for i in xrange(len(self.bagPast)):
            prob = (self.bagPast[i][1] + 1) / float(len(self.voc) + self.totalPast)
            self.bagPast[i].append(prob)

    # Create json files with bag of words, with counts and probabilities for live and past
    def storeProb(self):
        live = []
        for line in self.bagLive:
            live.append({
                "word": line[0],
                "count" : line[1],
                "prob" : line[2]
                })
        with open(self.liveSet, 'w+') as outfile:
            outfile.write(json.dumps(live, indent=4))
        past = []
        for line in self.bagPast:
            past.append({
                "word": line[0],
                "count" : line[1],
                "prob" : line[2]
                })
        with open(self.pastSet, 'w+') as outfile:
            outfile.write(json.dumps(past, indent=4))

    # return prior probability of tweet being live/past
    def getTrainProb(self):
        return self.pLive, self.pPast

    def extract(self, tweet):
        hashTags = []
        while(tweet.find("#") != -1):
            pos = tweet.find("#")
            hashTags.append(tweet[pos:tweet.find(" ", pos)])
            tweet = tweet[:pos] + tweet[tweet.find(" ", pos):]
        links = []
        while(tweet.find("http") != -1):
            url = re.search("(?P<url>https?://[^\s]+)", tweet).group("url")
            pos = tweet.find("http")
            links.append(url)
            tweet = tweet[:pos] + tweet[pos + len(url):]
        ref = []
        while(tweet.find("@") != -1):
            pos = tweet.find("@")
            ref.append(tweet[pos:tweet.find(" ", pos)])
            tweet = tweet[:pos] + tweet[tweet.find(" ", pos):]
        timeStamp = []
        check  = None
        pattern = re.compile(r"[0-9]+ mins")
        check = pattern.search(tweet)
        if check != None:
            pos = re.search(r"[0-9]+ mins", tweet).start()
            timeStamp.append(tweet[pos:tweet.find("s", pos)+1])
        tweet = re.sub("[^a-zA-Z-_]+", " ", tweet)
        return tweet, hashTags, links, ref, timeStamp


#     def printStats(self):
#         print("Total                        %d" % self.total)
#         print("Live                         %d" % self.live)
#         print("Past                         %d" % self.past)
#         print("Prob Live                    %.2f" % self.pLive)
#         print("Prob Past                    %.2f" % self.pPast)
#         print("Len of bag Live              %d" % len(self.bagLive)) 
#         print("Total Live                   %d" % self.totalLive)
#         print("Len of bag Past              %d" % len(self.bagPast))
#         print("Total Past                   %d" % self.totalPast)
#         print("Total Bag of Live Dictionary %d" % self.totalLiveDic )
#         print("Total Bag of Past Dictionary %d" % self.totalPastDic )
#         print("Len of Bag Live Dictionary   %d" % len(self.bagLiveDic ))
#         print("Len of Bag Past Dictionary   %d" % len(self.bagPastDic ))
#         print("Len of Vocabulary            %d" % len(self.voc))
#         print("Prob of 6-char hashtag live  %.2f" % self.hash6live)
#         print("Prob of 6-char hashtag past  %.2f" % self.hash6past)
#         print("Prob of link presence live   %.2f" % self.linksLive)
#         print("Prob of link presence past   %.2f" % self.linksPast)
#         print("Prob of timeStamp live  %.2f" % self.timeStampLive)
#         print("Prob of timeStamp past  %.2f" % self.timeStampPast)


if __name__ == '__main__':
    model = Model("trainSet.json", "dictionary.json", "./liveTrain.json", "./pastTrain.json", "./liveTrainDic.json", "./pastTrainDic.json")
    # model.printStats()
    print(self.bagLive)
    # model.storeProb()
    # model.storeProbDic()

