#Author: Anthony Soroka
#Class: CS 207
#HW 5
#Title: lc.py

import reprlib 
import os
from collections import defaultdict
import itertools
import numbers

def lc_reader(filename):
    lclist=[]
    metadict = {}
    with open(filename) as fp:
        lCount = 0
        for line in fp:
            if line.find('#')==0 and (lCount == 0) :
                facetNames = line
            
            if line.find('#')==0 and (lCount == 1) :
                facetValues = line
            
            if line.find('#')!=0:
                lclist.append([float(f) for f in line.strip().split()])
            
            lCount += 1
    
    facetNames = facetNames[1:].strip().split()
    facetValues = facetValues[1:].strip().split()

    for idx, val in enumerate(facetNames):
        metadict[facetNames[idx]] = facetValues[idx]
    
    return lclist, metadict

class LightCurve:
    
    def __init__(self, data, metadict):
        self._time = [x[0] for x in data]
        self._amplitude = [x[1] for x in data]
        self._error = [x[2] for x in data]
        self.metadata = metadict
        self.filename = None
    
    @classmethod
    def from_file(cls, filename):
        lclist, metadict = lc_reader(filename)
        instance = cls(lclist, metadict)
        instance.filename = filename
        return instance
    
    def __repr__(self):
        class_name = type(self).__name__
        components = reprlib.repr(list(itertools.islice(self.timeseries,0,10)))
        components = components[components.find('['):]
        return '{}({})'.format(class_name, components)        
        
    #your code here
    #Q4
    @property
    def time(self):
        return self._time
    
    @property
    def amplitude(self):
        return self._amplitude
    
    @property
    def timeseries(self):
        return zip(self._time,self._amplitude)
      
        
    #your code here
    #Q5
    def __len__(self):
        return len(self._amplitude)
    
    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, numbers.Integral) or isinstance(index, slice): 
            return list(self.timeseries)[index]
        else:
            msg = '{cls.__name__} indices must be integers' 
            raise TypeError(msg.format(cls=cls))

class LightCurveDB:
    
    def __init__(self):
        self._collection={}
        self._field_index=defaultdict(list)
        self._tile_index=defaultdict(list)
        self._color_index=defaultdict(list)
    
    def populate(self, folder):
        for root,dirs,files in os.walk(folder): # DEPTH 1 ONLY
            for file in files:
                if file.find('.mjd')!=-1:
                    the_path = root+"/"+file
                    self._collection[file] = LightCurve.from_file(the_path)
    
    def index(self):
        for f in self._collection:
            lc, tilestring, seq, color, _ = f.split('.')
            field = int(lc.split('_')[-1])
            tile = int(tilestring)
            self._field_index[field].append(self._collection[f])
            self._tile_index[tile].append(self._collection[f])
            self._color_index[color].append(self._collection[f])
     
    #your code here
    def retrieve(self, facet, value):
        if facet == 'tile':
            return self._tile_index[value]
        elif facet == 'field':
            return self._field_index[value]
        elif facet == 'color':
            return self._color_index[value]
        else:
            msg = 'Not a valid facet' 
            raise TypeError(msg)

