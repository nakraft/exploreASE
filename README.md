# Final Project CSC 591

## How to run

* Install python 3.9 or newer
* Install requirements: `pip install -r requirements.txt`
* Change directory to src using `cd src`
* Run `python main.py` to generate table for the `auto2.csv` file
* To run all datasets in the data folder at once, please do `sh generate_output.sh`
* Run `python main.py --help` to view possible configuration values

```
project: multi-goal semi-supervised algorithms

USAGE: python3 main.py [OPTIONS] [-g ACTIONS]
  
OPTIONS:
  -b  --bins    initial number of bins       = 16
  -c  --cliffs  cliff's delta threshold      = .147
  -d  --d       different is over sd*d       = .35
  -F  --Far     distance to distant          = .95
  -g  --go      start-up action              = nothing
  -f  --file    file to generate table of    = etc/data/new_SSM_for_FebStudy.csv
  -h  --help    show help                    = false
  -H  --Halves  search space for clustering  = 315
  -m  --min     size of smallest cluster     = .5
  -M  --Max     numbers                      = 512
  -p  --p       dist coefficient             = 2
  -r  --rest    how many of rest to sample   = 50
  -x  --bootstrap   number of samples to bootstrap   = 512
  -R  --Reuse   child splits reuse a parent pole = false
  -n  --nTimes   number of iterations to run  = 20
  -m  --mSeed    true means seed isn't randomized  = false
  -o  --conf        confidence interval      = 0.05
  -s  --seed    random number seed           = 937162211
  -h  --help    show help                    = false
  -w  --wColor      output with color        = true
  -w1 --width    the width for the tile      = 40
  -f1 --Fmt     the format of the tile       = {:.2f}
  -c1 --cohen   effect-size mthod            = .35
```


For Repgrids report, please see docs/repertory_grids.md.

## Project Structure

- Data files are located at [data](https://github.com/nakraft/exploreASE/tree/main/etc/data)
- Output files are located at [out](https://github.com/nakraft/exploreASE/tree/main/etc/out)
- Python files are located at [src](https://github.com/nakraft/exploreASE/tree/main/src)
- A [script](generate_out.sh) is used to generate all output and stored them to `etc/out/data_file.out`
    

## Authors 

- Leo Hsiang
- Ashrita Ramaswamy
- Sanjana Cheerla	
- Natalie Kraft

##  Support

Contributions, issues, and feature requests are welcome!

## Help

Email any queries to the contributors
