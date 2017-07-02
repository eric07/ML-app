from CrossValidate import CrossValidate
class PerfectW():
    def __init__(self):
        results = []
        for i in xrange(1, 20):
            for j in xrange(20):
                self.crossValidate = CrossValidate(i/10.0, j/10.0)
                r = (self.crossValidate.totalP, self.crossValidate.totalN, i/10.0, j/10.0)
                print(r)
                results.append(r)
            break
        results = sorted(results, key=self.getKey, reverse=True)
        print("\nResults\n")
        print(results[0])
    def getKey(self, item):
        return item[0]

if __name__ == '__main__':
    perfectW = PerfectW()