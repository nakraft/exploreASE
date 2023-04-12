
 

from typing import List, Dict, Tuple
from util import rnd
import heapq
import time

from data import Data
from discretization import value, bins, RANGE
from string_util import *
class Explain:
    def __init__(self, best: Data, rest: Data):
        self.best = best
        self.rest = rest

        self.tmp: List[Tuple[RANGE, int, float]] = []
        self.max_sizes: Dict[str, int] = {}

    def score(self, ranges: List[RANGE]):
        rule = self.rule(ranges, self.max_sizes)

        if rule:
            bestr = selects(rule, self.best.rows)
            restr = selects(rule, self.rest.rows)

            if len(bestr) + len(restr) > 0:
                return value({"best": len(bestr), "rest": len(restr)}, len(self.best.rows), len(self.rest.rows), "best"), rule
        return None,None

    def xpln(self, data: Data, best: Data, rest: Data):
        start_time = time.time()
        def v(has):
            return value(has, len(best.rows), len(rest.rows), "best")
        
        tmp,self.max_sizes = [],{}
        for _,ranges in enumerate(bins(data.cols.x,{"best":best.rows, "rest":rest.rows})):
            self.max_sizes[ranges[0]['txt']] = len(ranges)
            for _,range in enumerate(ranges):
                tmp.append({"range":range, "max":len(ranges),"val": v(range['y'].has)})
        rule,most=self.firstN(sorted(tmp,key = lambda x: x["val"],reverse=True),self.score)
        print("time xpln1= " + str(time.time()-start_time))
        return rule,most

    def xpln2(self, data: Data, best: Data, rest: Data):
        start_time = time.time()
        def v(has):
            return value(has, len(best.rows), len(rest.rows), "best")
        
        tmp,self.max_sizes = [],{}
        for _,ranges in enumerate(bins(data.cols.x,{"best":best.rows, "rest":rest.rows})):
            self.max_sizes[ranges[0]['txt']] = len(ranges)
            for _,range in enumerate(ranges):
                tmp.append({"range":range, "max":len(ranges),"val": v(range['y'].has)})
        rule, most = self.firstN(heapq.nlargest(len(ranges), tmp, key=lambda x: x["val"]), self.score)
        print("time xpln2= " + str(time.time()-start_time))
        return rule,most
    
    def firstN(self, sorted_ranges, scoreFun):
        first = sorted_ranges[0]['val']

        def useful(range):
            if range['val'] > 0.05 and range['val'] > first / 10:
                return range
        sorted_ranges = [s for s in sorted_ranges if useful(s)]
        most: int = -1
        out: int = -1

        for n in range(len(sorted_ranges)):
            tmp, rule = scoreFun([r['range'] for r in sorted_ranges[:n+1]])

            if tmp is not None and tmp > most:
                out, most = rule, tmp

        return out, most
    
    def rule(self, ranges,maxSize):
        t={}
        for _,range in enumerate(ranges):
            t[range['txt']] = t.get(range['txt'], [])
            t[range['txt']].append({"lo":range['lo'],"hi":range['hi'],"at":range['at']})
        return self.prune(t, maxSize)

    def prune(self, rule, maxSize):
        n=0
        new_rule = {}
        for txt,ranges in rule.items():
            n = n+1
            if len(ranges) == maxSize[txt]:
                n=n-1
                rule[txt] = None
            else:
                new_rule[txt] = ranges
        if n > 0: 
            return new_rule
        return None

def showRule(self,rule):
    def pretty(range):
        return range['lo'] if range['lo']==range['hi'] else [range['lo'], range['hi']]
    def merge(t0):
        t,j =[],1
        while j<=len(t0):
            left = t0[j-1]
            if j < len(t0):
                right = t0[j]
            else:
                right = None
            if right and left['hi'] == right['lo']:
                left['hi'] = right['hi']
                j=j+1
            t.append({'lo':left['lo'], 'hi':left['hi']})
            j=j+1
        return t if len(t0)==len(t) else merge(t) 

def selects(rule, rows):
    def disjunction(ranges, row):
        for rang in ranges:
            at = rang['at']
            x = row.cells[at]
            lo = rang['lo']
            hi = rang['hi']  
            if x == '?' or (lo == hi and lo == x) or (lo <= x and x< hi):
                return True
        return False
    def conjunction(row):
        for _,ranges in rule.items():
            if not disjunction(ranges, row):
                return False
        return True
    def function(r):
        return r if conjunction(r) else None
    
    r = []
    for item in list(map(function, rows)):
        if item:
            r.append(item)
    return r