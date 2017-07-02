import os, json
from Model import Model
from Classify import Classify
import matplotlib.pyplot as plt
import numpy as np

class CrossValidate():
    def __init__(self, pBag = 0.6, pDict = 0.4):
        self.N = 10
        self.cleanup()
        self.createFileStructure()
        self.model = Model("trainSet.json", "dictionary.json", "./liveTrain.json", "./pastTrain.json", "./liveTrainDic.json", "./pastTrainDic.json")
        self.train = self.model.load("trainSet.json")
        totalP = 0
        totalN = 0
        self.pBag = pBag
        self.pDict = pDict
        for i in xrange(0, self.N):
            self.createTrainStructure(i)
            self.createTrainData(i)
            m, n = self.classify(i)
            m = round(m, 2)
            n = round(n, 2)
            # print(m, n)
            totalP += m
            totalN += n
        print("Average")
        self.totalP = round(totalP/self.N, 2)
        self.totalN = round(totalN/self.N, 2)
        print(self.totalP, self.totalN)

    def cleanup(self):
        os.system("rm -r Validate")

    def createFileStructure(self):
        os.system("mkdir Validate")
        for i in xrange(0, self.N):
            os.system("mkdir Validate/"+str(i))
            os.system("cp dictionary.json ./Validate/"+str(i))

    def createTrainStructure(self, vId):
        train = []
        test = []
        count1 = count2 = 0
        for i in xrange(len(self.train)):
            if i % self.N == vId:
                count1 += 1
                test.append(self.train[i])
            else:
                count2 += 1
                train.append(self.train[i])
        with open('Validate/'+str(vId)+'/Train.json', 'w+') as outfile:
            outfile.write(json.dumps(train, indent=4))

        with open('Validate/'+str(vId)+'/Test.json', 'w+') as outfile:
            outfile.write(json.dumps(test, indent=4))

    def createTrainData(self, vId):
        train = "Validate/"+str(vId)+"/Train.json"
        dictionary = "Validate/"+str(vId)+"/dictionary.json"
        liveTrain = "Validate/"+str(vId)+"/liveTrain.json"
        pastTrain = "Validate/"+str(vId)+"/pastTrain.json"
        liveTrainDic = "Validate/"+str(vId)+"/liveTrainDic.json"
        pastTrainDic = "Validate/"+str(vId)+"/pastTrainDic.json" 
        model = Model(train, dictionary, liveTrain, pastTrain, liveTrainDic, pastTrainDic)
        model.storeProb()
        model.storeProbDic()

    def classify(self, vId):
        train = "Validate/"+str(vId)+"/Train.json"
        dictionary = "Validate/"+str(vId)+"/dictionary.json"
        liveTrain = "Validate/"+str(vId)+"/liveTrain.json"
        pastTrain = "Validate/"+str(vId)+"/pastTrain.json"
        liveTrainDic = "Validate/"+str(vId)+"/liveTrainDic.json"
        pastTrainDic = "Validate/"+str(vId)+"/pastTrainDic.json" 
        classifier = Classify(train, dictionary, liveTrain, pastTrain, liveTrainDic, pastTrainDic)
        data = self.model.load("Validate/"+str(vId)+"/Test.json")
        pos = 0
        falsepos = 0
        neg = 0
        falseneg = 0
        for line in data:
            r = classifier.classify(line['text'], self.pBag, self.pDict)
            if r == 'live':
                if line['classId'] == 0:
                    pos += 1
                else:
                    falsepos += 1
            else:
                if line['classId'] == 1:
                    neg += 1
                else:
                    falseneg += 1
        # print(pos, falsepos, neg, falseneg)
        incorrect = round((100 * (falsepos+falseneg))/float(pos + neg), 2)
        # print(100-incorrect, incorrect)
        return (100-incorrect), incorrect 

if __name__ == '__main__':
    v = CrossValidate()

