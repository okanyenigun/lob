from builder.meta import Meta
from indicators.rsi import Rsi

class Testing:

    def __init__(self, params, weights, money=100000):
        self.params = params
        self.weights = weights
        self.money = money
        M = Meta()
        self.df = M.df_lob

    def run(self):
        signals = {}
        #hangi testler
        test_list = self.parse_tests()
        for test in test_list:
            liste = []
            if test == "rsi":
                closes = self.df["bid1px"].values.tolist()
                I = Rsi(closes)
                self.df["rsi"] = I.calculate_series()
                self.df["rsi"].fillna(-1,inplace=True)
                for i in range(self.df.shape[0]):
                    signal = I.get_signal(self.df.loc[i,"rsi"])
                    liste.append(signal)
                print(len(liste))
                #get signal
                for weight in self.weights:
                    if weight["parametername"] == "RSI":
                        print((weight["percent"]/100))
                        liste = [x * (weight["percent"]/100) for x in liste]
                signals["rsi"] = liste
        print(signals)
        return
            
    def parse_tests(self):
        test_list = [x.split("_")[0] for x in self.params]
        return list(dict.fromkeys(test_list))

    def buy(self):
        pass