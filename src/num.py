import math
from util import *
import config as config
class Num():
    """
    Summarizes a stream of numbers. 
    """
    def __init__(self, at: int = 0, txt: str = "") -> None:
        self.at = at
        self.txt = txt

        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.sd = 0
        self.lo = math.inf
        self.hi = -math.inf
        self.w = -1 if self.txt.endswith("-") else 1
        self.has_ = {}

    def add(self, x, n: float = 1) -> None:
        """
        Adds n and updates lo, hi and stuff needed for standard deviation.
        :param n: Number to add
        :return: None
        """
        if x != "?":
            self.n += n

            self.lo, self.hi = min(x, self.lo), max(x, self.hi)

            all = len(self.has_)

            pos = all + 1 if all < config.the["Max"] else rint(1, all) if rand() < config.the["Max"] / self.n else 0

            if pos:
                self.has_[pos] = x
                self.ok = False

            # for stats
            d = x - self.mu
            self.mu = self.mu + d/self.n
            self.m2 = self.m2 + d*(x-self.mu)
            self.sd = 0 if self.n<2 else (self.m2/(self.n - 1))**.5

    def mid(self) -> float:
        """
        Get Central tendancy. 
        Returns: median of nums in Nums class
        """
        return self.mu


    def div(self) -> float:
        return (self.m2 < 0 or self.n < 2) and 0 or (self.m2 / (self.n - 1)) ** 0.5


    def rnd(self, x, n):
        if x == "?":
            return x
        else:
            return rnd(x, n)

    def norm(self, n): 
        """
            provides a normalized version of the numbers
        """
        if n == "?": 
            return n 
        else: 
            return (n - self.lo) / (self.hi - self.lo + (10**-32))
        
    def has(self):
        ret = dict(sorted(self.has_.items(), key=lambda x: x[1]))
        self.ok = True
        return list(ret.values())
    
    def dist(self, n1, n2): 
        if n1 == "?" and n2 == "?": 
            return 1
        else: 
            n1 = self.norm(n1)
            n2 = self.norm(n2)
            if n1 == "?" and n2 < .5: 
                n1 = 1
            else: 
                n1 = 0
            if n2 == "?" and n1 < .5: 
                n2 = 1
            else: 
                n2 = 0 
            
            return abs(n1 - n2)