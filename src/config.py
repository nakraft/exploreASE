import math


the,help = {},"""
xpln: multi-goal semi-supervised explanation
(c) 2023 Tim Menzies <timm@ieee.org> BSD-2
  
USAGE: lua xpln.lua [OPTIONS] [-g ACTIONS]
  
OPTIONS:
  -b  --bins    initial number of bins       = 16
  -c  --cliffs  cliff's delta threshold      = .147
  -d  --d       different is over sd*d       = .35
  -F  --Far     distance to distant          = .95
  -g  --go      start-up action              = nothing
  -f  --file    file to generate table of    = etc/data/auto2.csv
  -h  --help    show help                    = false
  -H  --Halves  search space for clustering  = 1024
  -m  --min     size of smallest cluster     = .5
  -M  --Max     numbers                      = 512
  -p  --p       dist coefficient             = 2
  -r  --rest    how many of rest to sample   = 10
  -x  --bootstrap   number of samples to bootstrap   = 512
  -R  --Reuse   child splits reuse a parent pole = true
  -n  --nTimes   number of iterations to run  = 3
  -o  --conf        confidence interval      = 0.05
  -s  --seed    random number seed           = 937162211
  -h  --help    show help                    = false
  -w  --wColor      output with color        = true
  -w1 --width    the width for the tile      = 40
  -f1 --Fmt     the format of the tile       = {:.2f}
  -c1 --cohen   effect-size mthod            = .35
"""

Seed = 937162211

n = 0

def rint(nlo, nhi): 
  return math.floor(.5 + rand(nlo, nhi))

def rand(nlo, nhi): 
  nlo = nlo if nlo is not None else 0 
  nhi = nhi if nhi is not None else 1 
  seed = (16807 * Seed) % 2147483647
  return nlo + (nhi - nlo) * seed / 2147483647

def rnd(n, nPlaces=3):
    mult=10**(nPlaces or 3)
    return math.floor(n*mult + 0.5)/mult