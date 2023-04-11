from explain import selects
from data import Data
from string_util import settings
from string_util import cli
from test import *
import config
from util import *
from stats import cliffsDelta, bootstrap
from tabulate import tabulate
from explain import Explain

def main(options, help):
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

    print(options)
    if options["help"]:
        print(help)
    else:
        results = {"all": [], "sway1": [], "xpln1": [], "sway2" : [], "xpln2": [], "top": []}
        comparisons = [[["all", "all"],None], 
                       [["all", "sway1"],None],
                       [["all", "sway2"],None],
                       [["sway1", "sway2"],None],    
                       [["sway1", "xpln1"],None],  
                       [["sway2", "xpln2"],None],  
                       [["sway1", "top"],None]]
        n_evals = {"all": 0, "sway1": 0, "sway2": 0,  "xpln1": 0, "xpln2": 0, "top": 0}

        count = 0
        data=None
        while count < config.the["nTimes"]:
            # read in the data
            data=Data(config.the["file"])
            data2=Data(config.the["file"])
            # get the "all" and "sway" results
            best,rest,evals_sway = data.sway()
            best2,rest2,evals_sway2 = data2.sway2()
            # get the "xpln" results
            data.best = best
            data.rest = rest
            data2.best = best2
            data2.rest = rest2
            explain = Explain(best,rest)
            explain2 = Explain(best2,rest2)
            rule,_= explain.xpln(data,best,rest)
            rule2,_= explain2.xpln2(data2,best2,rest2)
            # if it was able to find a rule
            if rule != -1 and rule2 != -1:
                # get the best rows of that rule
                data1= Data(data,selects(rule,data.rows))
                data2= Data(data2,selects(rule2,data2.rows))
                results['all'].append(data)
                results['sway1'].append(best)
                results['xpln1'].append(data1)
                results["sway2"].append(best2)
                results["xpln2"].append(data2)
                # get the "top" results by running the betters algorithm
                top2,_ = data.betters(len(best.rows))
                top = Data(data,top2)
                results['top'].append(top)

                # accumulate the number of evals
                n_evals["all"] += 0
                n_evals["sway1"] += evals_sway
                n_evals["xpln1"] += evals_sway
                n_evals["top"] += len(data.rows)
                n_evals["sway2"] += evals_sway2
                n_evals["xpln2"] += evals_sway2
                comparisons = update_comp(comparisons, results, count, data)
                count += 1

        # generate the stats table
        headers = [y.txt for y in data.cols.y]
        table = []
        # for each algorithm's results
        for k,v in results.items():
            # set the row equal to the average stats
            stats = get_stats(v)
            stats_list = [k] + [stats[y] for y in headers]
            # adds on the average number of evals
            stats_list += [float(n_evals[k]/config.the["nTimes"])]
            
            table.append(stats_list)
        
        if config.the["wColor"]:
            # updates stats table to have the best result per column highlighted
            for i in range(len(headers)):
                # get the value of the 'y[i]' column for each algorithm
                header_vals = [v[i+1] for v in table]
                # if the 'y' value is minimizing, use min else use max
                fun = max if headers[i][-1] == "+" else min
                # change the table to have green text if it is the "best" for that column
                table[header_vals.index(fun(header_vals))][i+1] = '\033[93m' + str(table[header_vals.index(fun(header_vals))][i+1]) + '\033[0m'
        print(tabulate(table, headers=headers+["Avg evals"],numalign="right"))
        print()

        
        # generates the =/!= table
        table=[]
        # for each comparison of the algorithms
        #    append the = / !=
        for [base, diff], result in comparisons:
            table.append([f"{base} to {diff}"] + result)
        print(tabulate(table, headers=headers,numalign="right"))



def get_stats(data_array):
    # gets the average stats, given the data array objects
    res = {}
    # accumulate the stats
    for item in data_array:
        stats = item.stats()
        # update the stats
        for k,v in stats.items():
            res[k] = res.get(k,0) + v

    # right now, the stats are summed. change it to average
    for k,v in res.items():
        res[k] /= config.the["nTimes"]
    return res
def update_comp(comparisons, results, count, data):
    # update comparisons
        for i in range(len(comparisons)):
            [base, diff], result = comparisons[i]
            # if they haven't been initialized, mark with true until we can prove false
            if result == None:
                comparisons[i][1] = ["=" for _ in range(len(data.cols.y))]
            # for each column
            for k in range(len(data.cols.y)):
                # if not already marked as false
                if comparisons[i][1][k] == "=":
                    # check if it is false
                    base_y, diff_y = results[base][count].cols.y[k],results[diff][count].cols.y[k]
                    equals = bootstrap(base_y.has(), diff_y.has()) and cliffsDelta(base_y.has(), diff_y.has())
                    if not equals:
                        if i == 0:
                            print("WARNING: all to all {} {} {}".format(i, k, "false"))
                            print(f"all to all comparison failed for {results[base][count].cols.y[k].txt}")
                        comparisons[i][1][k] = "≠"
        return comparisons
main(config.the, config.help)
