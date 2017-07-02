import json, nltk, math
from Model import Model
import pylab as P
import matplotlib.pyplot as plt
from numpy.random import normal
import numpy as np
import matplotlib.pyplot as plt

class Visualise():
    def __init__(self):
        self.model = Model("trainSet.json", "dictionary.json", "./liveTrain.json", "./pastTrain.json", "./liveTrainDic.json", "./pastTrainDic.json")
        self.live = self.model.load("liveTrain.json")
        self.past = self.model.load("pastTrain.json")

    def ratios(self):
        words = []
        ratio = []
        bucket = [0]*20
        i = 0
        for line in self.live:
            for line2 in self.past:
                if line2 ['word'].lower() == line ['word'].lower():
                    words.append(line['word'])
                    ratio.append((line['prob']/ line2['prob']))
                    #print words[i], ratio[i]
                    if ratio[i] < 1:
                        bucket [int (ratio[i]*10)] = bucket [int (ratio[i]*10)] + 1
                        print words[i], ratio[i], int (ratio[i]*10)
                    if ratio [i] >= 1 and ratio [i] <= 10:
                        bucket [19 - int (1 / ratio[i] * 10)] = bucket [19 - int (1 / ratio[i] *10 +9)] + 1
                        print words[i], ratio[i], 19 - int (1 / ratio[i] * 10)
                    if ratio [i] > 10:
                        bucket [19] = bucket [19] + 1
                        print words[i], ratio[i], 19
                    i = i + 1
                    break
        print min(ratio), max(ratio)
        for j in xrange (0, 20):
            print j, bucket [j]
        #
        # create a histogram by providing the bin edges (unequally spaced)
        #
        plt.figure()

        bins = [i for i in xrange(0,20)]
        # # the histogram of the data with histtype='step'
        plt.bar(bins, bucket)
        plt.show()

if __name__ == '__main__':
    vis = Visualise()
    vis.ratios()
    
    x = np.arange(0, 5, 0.1);
    y = np.sin(x)
    plt.plot(x, y)
