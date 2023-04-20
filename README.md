# Final Project CSC 591

## How to run

* Install python 3.9 or newer
* Install requirements: `pip install -r requirements.txt`
* Change directory to src using `cd src`
* Run `python main.py` to generate table for the `auto2.csv` file
* To run all datasets in the data folder at once, please do `sh generate_output.sh`


For Repgrids report, please see docs/repertory_grids.md.

## Structure

- Data files are located at [data](https://github.com/nakraft/exploreASE/tree/main/etc/data)
- Output files are located at [out](out) and are named using the csv file name
- Python files are located at [src](src)
- A [script](generate_out.sh) is used to generate all output. It iterates over all data files, runs them through our program, and concatenates output to the output directory
    - The output and how long the process takes is saved to to `out/data_file.out
    
TODO:
Provide links for outputs, and information about how to run with help string

## Authors 

- Leo Hsiang
- Ashrita Ramaswamy
- Sanjana Cheerla	
- Natalie Kraft

##  Support

Contributions, issues, and feature requests are welcome!

## Help

Email any queries to the contributors
