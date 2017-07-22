import json, nltk, math
from Model import Model
from Fetch import Fetch

# Class implementing Naive Bayes classification
class Classify():
    def __init__(self, trainSet, dictionary, liveTrain, pastTrain, liveTrainDic, pastTrainDic):
        self.model = Model(trainSet, dictionary, liveTrain, pastTrain, liveTrainDic, pastTrainDic)
        self.live = self.model.load(liveTrain)
        self.past = self.model.load(pastTrain)

    # Find prior probability of word in past and live training set
    def getProb(self, word):
        live = None
        past = None
        word = word.lower()
        for line in self.live:
            if word == line['word']:
                live = line['prob']
                break
        for line in self.past:
            if word == line['word']:
                past = line['prob']
                break
        return live, past

    # Classify a tweet 
    def classifyOne(self, tweet, pBag, pDict):
        #Get initial probabilities
        live, past = self.model.getTrainProb()
        live = math.log(live)
        past = math.log(past)

        #Set importance of each feature
        weightMain = pBag
        weightDic = pDict


        print ("\n")
        print("Classifying tweet:")
        print (tweet)
        
        
        # Calculate Probability of tweet
        switch = 0
        for word in tweet.split():
            # Disregard articles etc
            if(len(word) < 4):
                continue
            i, j = self.getProb(word)
            # if tweet is present add to total probability
            if i != None:
                live += math.log(i)
            # else apply Lapplace correction
            else:
                live += math.log( 1 / float(len(self.model.voc) + self.model.totalLive ))
            if j != None:
                past += math.log(j)
            else:
                past += math.log( 1 / float(len(self.model.voc) + self.model.totalPast ))

            #Use dictionary in classification
            if switch == 1:
                i, j = self.getProbDic(word)
                if i != None:
                    liveDic += math.log(i)
                else:
                    liveDic += math.log( 1 / float(len(self.model.vocDic) + self.model.totalLiveDic ))
                if j != None:
                    pastDic += math.log(j)
                else:
                    pastDic += math.log( 1 / float(len(self.model.vocDic) + self.model.totalPastDic ))

        #Assign weights to each feature
        if switch == 1:
            live = live * weightMain + liveDic * weightDic
            past = past * weightMain + pastDic * weightDic

        if live >= past:
            return ("Tweet is happening now!")
        else:
            return ("Tweet talks about the past!")


if __name__ == '__main__':
    classifier = Classify("trainSet.json", "dictionary.json", "./liveTrain.json", "./pastTrain.json", "./liveTrainDic.json", "./pastTrainDic.json")
    print(classifier.classifyOne("SUB Nacho Monreal is forced off with an injury and replaced by Kieran Gibbs. It's West Brom 0-0 Arsenal (23 mins) #WBAARS", 1,1))
    print(classifier.classifyOne("Starting today, 20 #BPL matches in 5 days\u2026 Ready? http://t.co/qbszRAau2U",1,1))
    print(classifier.classifyOne("PHOTO Arsenal have had the better chances in the early running but it remains 0-0 after 21 mins #WBAARS http://t.co/A3bmkwQ2aT",1,1))
    print(classifier.classifyOne("KICK-OFF The second half is under way at The Hawthorns with both teams unchanged after the break #WBAARS",1,1))
    print(classifier.classifyOne("WOODWORK #WBAARS",1,1))
    print(classifier.classifyOne("Second meets third at St Mary's on Sunday. Who wins? #SOUMCI http://t.co/sJtQESy0fK",1,1))
