
import numpy as np
from abc import ABC, abstractmethod


class PriceLevels(ABC):

    @abstractmethod
    def is_atlevel(self):
        pass

    @abstractmethod
    def is_near_another(self):
        pass

    @abstractmethod
    def get_levels(self):
        pass

    @abstractmethod
    def find_spots(self):
        pass

    @abstractmethod
    def calculate_distance(self):
        pass

    @abstractmethod
    def collect_params(self):
        pass

class SupportLevel(PriceLevels):
    
    def __init__(self,df):
        self.df = df
    
    def is_atlevel(self,i):
        support = self.df['lowprice'][i] < self.df['lowprice'][i-1]  and self.df['lowprice'][i] < self.df['lowprice'][i+1] and self.df['lowprice'][i+1] < self.df['lowprice'][i+2] and self.df['lowprice'][i-1] < self.df['lowprice'][i-2]
        return support

    def is_near_another(self,l,levels,s):
        return np.sum([abs(l-x) < s  for x in levels]) == 0
    
    def get_levels(self):
        s =  np.mean(self.df['highprice'] - self.df['lowprice'])
        support_levels = []
        for i in range(2,self.df.shape[0]-2):
          if self.is_atlevel(i):
            l = self.df['lowprice'][i]
            if self.is_near_another(l,support_levels,s):
              support_levels.append((i,l))
        return support_levels

    def find_spots(self,levels):
        self.df["SUPPORTSPOT"] = [0] *self.df.shape[0]
        for i in range(len(levels)):
            self.df.loc[levels[i][0],"SUPPORTSPOT"] = 1
        return 
    
    def calculate_distance(self,levels):
        distances = [0] * levels[0][0]
        for i in range(len(levels)-1):
            from_range = levels[i][0]
            to_range = levels[i+1][0]
            diff = to_range - from_range
            for j in range(diff):
                distances.append(j)
        for i in range(self.df.shape[0]-len(distances)):
            distances.append(i)
        return distances
    
    def collect_params(self):
        levels = self.get_levels()
        self.find_spots(levels)
        self.df["SUPPORTDISTANCE"] = self.calculate_distance(levels)
        return self.df

class ResistLevel(PriceLevels):
    
    def __init__(self,df):
        self.df = df
    
    def is_atlevel(self,i):
        resistance = self.df['highprice'][i] > self.df['highprice'][i-1]  and self.df['highprice'][i] > self.df['highprice'][i+1] and self.df['highprice'][i+1] > self.df['highprice'][i+2] and self.df['highprice'][i-1] > self.df['highprice'][i-2]
        return resistance

    def is_near_another(self,l,levels,s):
        return np.sum([abs(l-x) < s  for x in levels]) == 0
    
    def get_levels(self):
        s =  np.mean(self.df['highprice'] - self.df['lowprice'])
        levels = []
        for i in range(2,self.df.shape[0]-2):
          if self.is_atlevel(i):
            l = self.df['highprice'][i]
            if self.is_near_another(l,levels,s):
              levels.append((i,l))
        return levels

    def find_spots(self,levels):
        self.df["RESISTSPOT"] = [0] *self.df.shape[0]
        for i in range(len(levels)):
            self.df.loc[levels[i][0],"RESISTSPOT"] = 1
        return 
    
    def calculate_distance(self,levels):
        distances = [0] * levels[0][0]
        for i in range(len(levels)-1):
            from_range = levels[i][0]
            to_range = levels[i+1][0]
            diff = to_range - from_range
            for j in range(diff):
                distances.append(j)
        for i in range(self.df.shape[0]-len(distances)):
            distances.append(i)
        return distances
    
    def collect_params(self):
        levels = self.get_levels()
        self.find_spots(levels)
        self.df["RESISTDISTANCE"] = self.calculate_distance(levels)
        return self.df