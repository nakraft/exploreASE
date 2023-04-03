from test import test_xpln, checkCsv, checkHalf, checkClone, checkBins, checkSway, checkTree, checkDist, checkCliffs, show_settings, checkRand, checkSome, checkNums, checkSyms, checkData, checkCsv
from string_util import settings
from string_util import cli
from test import *
import config
from util import *

def main(options, help, funs, saved = {}, fails = 0):
    """
    `main` fills in the settings, updates them from the command line, runs
    the start up actions (and before each run, it resets the random number seed and settongs);
    and, finally, returns the number of test crashed to the operating system.
    :param funs: list of actions to run
    :param saved: dictionary to store options
    :param fails: number of failed functions
    """
    for k, v in cli(settings(help)).items():
        options[k] = v
        saved[k] = v

    if options["help"]:
        print(help)
    else:
        for what in funs:
            if options["go"] == "all" or what == options["go"]:
                for k,v in saved.items():
                    options[k] = v
                if funs[what]() == False:
                    fails = fails + 1
                    print("❌ fail:", what)
                else:
                    print("✅ pass:", what)
    
egs = {}
def eg(key,string,fun):
  global egs
  egs[key]=fun
  config.help = config.help + ("  -g  %s\t%s\n" % (key,string))
  
eg("the", "show options", show_settings)
eg("rand", "demo random number generation", checkRand)
eg("some", "demo of reservoir sampling", checkSome)
eg("nums","demo of NUM", checkNums)
eg("syms","demo SYMS", checkSyms)
eg("csv", "reading csv files", checkCsv)
eg("data", "showing data sets", checkData)
eg("clone","replicate structure of a DATA", checkClone)
eg("cliffs", "stats tests", checkCliffs)
eg("dist","distance test", checkDist)
eg("half","divide data in half", checkHalf)
eg("tree","make snd show tree of clusters", checkTree)
eg("sway","optimizing", checkSway)
eg("bins","find deltas between best and rest", checkBins)
eg("xpln", "explore explanation sets", test_xpln)

list_of_file_paths = ["etc/data/auto2.csv", "etc/data/auto93.csv", "etc/data/china.csv", "etc/data/coc1000.csv",
                          "etc/data/coc10000.csv", "etc/data/healthCloseIsses12mths0001-hard.csv", "etc/data/healthCloseIsses12mths0011-easy.csv",
                          "etc/data/nasa93dem.csv", "etc/data/pom.csv", "etc/data/SSM.csv", "etc/data/SSN.csv"]
table1_dict = {}
for file in list_of_file_paths:
    file_string = str(file.split('/')[-1]).split('.')[0]
    print(f"File: {file_string}")
    config.FILE = file
    print(config.FILE)
    main(config.the, config.help, egs)