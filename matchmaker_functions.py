import numpy as np
from graph import *
import json
import sys
import time


#sys.path.append('../excel_tools')
#to get these paths I used the pwd unix command.

sys.path.append('/Users/taylordupuy/Documents/web-development/dev/excel_tools')
my_system_path ='/Users/taylordupuy/Documents/web-development/dev/submission_tools/'
path_to_variables_j = my_system_path + 'variables.json'
path_to_constants_j = my_system_path + 'constants.json'
path_to_testing_j = my_system_path + 'testing.json'

from table_editor import SheetObject
from table_functions import *
from matchmaker_functions import *


def is_admissible(V,degree_dict):
    """
    V=['apple','banana','orange','pear','mango','peach','grape']
    degree_dict = {}
    for v in V:
        degree_dict[v] = {}
        degree_dict[v]['in']=2
        degree_dict[v]['out']=2
    is_admissible(V,degree_dict)
    True
    """
    #this test is incomplete
    total_in_degree = sum([degree_dict[v]['in'] for v in V])
    total_out_degree = sum([degree_dict[v]['out'] for v in V])
    if not total_in_degree==total_out_degree:
        return False
    n = len(V)
    for v in V:
        if not (max_degree(v,degree_dict) <= n-1):
            return False
    return True

def max_degree(v,degree_dict):
    """
    v0 = 'apple'
    max(degree_dict[v0]['in'],degree_dict[v0]['out'])
    2
    """
    return max(degree_dict[v]['in'],degree_dict[v]['out'])

def match_up(g,V,degree_dict):
    """
    One should give a proof that method works.
    V is a list
    g is a Graph()
    degree_dict is a dictionary which has an in-degree and out degree for each vertex.
    """
    m=len(V)
    if m==1:
        return g
    
    if not is_admissible(V,degree_dict):
        raise ValueError('matching error, degree dict not admissible')
        
    else:
        #V = sorted(V, key=(lambda v : degree_dict[v]['out']), reverse=True)
        V = list(np.random.permutation(V))
        V = sorted(V, key=(lambda v : max_degree(v,degree_dict)), reverse=True)
        v = V[0]
        #print('starting point')
        #print(v)
        #print(degree_dict)
        W = V[1:]
        n=m-1
        W = sorted(W, key=(lambda w : degree_dict[w]['in']), reverse=True)
        #print(W)
        #print(degree_dict)
        i=0
        while degree_dict[v]['out']>0:
            w=W[i]
            if degree_dict[w]['in']>0:
                g.add_edge(v,w)
                degree_dict[w]['in'] = degree_dict[w]['in']-1
                degree_dict[v]['out'] = degree_dict[v]['out']-1
            i=i+1
            if i>=n:
                raise AttributeError("can't made edges for v=%s " % v)
        
        W = sorted(W, key=(lambda w : degree_dict[w]['out']), reverse=True)
        #print(W)
        #print(degree_dict)
        i=0
        while degree_dict[v]['in']>0:
            w = W[i]
            if degree_dict[w]['out']>0:
                g.add_edge(w,v)
                degree_dict[w]['out'] = degree_dict[w]['out']-1
                degree_dict[v]['in'] = degree_dict[v]['in']-1
            i=i+1
            if i>=n:
                raise AttributeError("can't made edges for v=%s " % v)
                
    return match_up(g,W,degree_dict)


def get_random_graph(g,V,degree_dict,n):
    if n==0:
        raise AttributeError("exceeded number of tries")
    else:
        try:
            g=match_up(g,V,degree_dict)
        except AttributeError as e:
            g=get_random_graph(g,V,degree_dict,n-1)
            
    return g
            
