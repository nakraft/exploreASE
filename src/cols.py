import re
from num import Num
from sym import Sym

class Cols:
    '''Declares a column class that holds a column of data'''

    def __init__(self, t:dict):
        ''' 
        inits Cols with name of col
        :param names: (str) first row containing names of the columns
        :type names: (str) names of the columns
        :type all: (list[col]) every column including skipped columns are included here
        :type x: (list[col]) every independent unskipped column
        :type y: (list[col]) every dependent unskipped column
        :type klass: (col) single dependent col
        
        '''
        self.names = t
        self.all = []
        self.x = []
        self.y = []
        self.klass = None

        for n, s in enumerate(t):
            s = s.strip()
            # Generate Nums and Syms from column names
            col = Num(n, s) if re.findall("^[A-Z]+", s) else Sym(n, s)
            self.all.append(col)

            if not re.findall("X$", s):
                if re.findall("!$", s):
                    self.klass = col
                # if it ends in "!", "+", or "-", append it to self.y, else append to self.x
                self.y.append(col) if re.findall("[!+-]$", s) else self.x.append(col)

    def add(self, row) -> None:
        """
        Updates the columns with details from row
        :param row: Row to add
        """
        for _, t in enumerate([self.x, self.y]):
            for _, col in enumerate(t):
                col.add(row.cells[col.at])


