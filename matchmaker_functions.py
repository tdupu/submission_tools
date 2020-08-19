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
        raise ValueError("exceeded number of tries")
    else:
        try:
            g=match_up(g,V,degree_dict)
        except AttributeError as e:
            g=get_random_graph(g,V,degree_dict,n-1)
            
    return g
    
    
def splice(g,v,d,forbiddena=[],forbiddenb=[]):
    """
    Take two (a,b), (c,d) with a neq c and b neq d
    Remove the edges and add (a,v),(v,b),(c,v),(v,d)
    """
    edges=[e for e in np.random.permutation(g.edges())]
    e=edges[0]
    myedges=[]
    myedges.append(e)
    forbiddena.append(e[0])
    forbiddenb.append(e[1])
    n=d
    for f in edges[1:]:
        if forbiddena.count(f)==0 and forbiddenb.count(f[1])==0:
            myedges.append(f)
            forbiddena.append(f[0])
            forbiddenb.append(f[1])
            found_next=True
            n = n-1
            
        if n==0:
            break
            
    for e in myedges:
        g.del_edge(e)
        g.add_edge(e[0],v)
        g.add_edge(v,e[1])
        
    return g
        
def random_graph_spliced(g,V,degree_dict):
    """
    Start with three then splice in vertices as you go.
    """
    if len(V)==3:
        g.add_edge(V[0],V[1])
        g.add_edge(V[0],V[2])
        g.add_edge(V[1],V[0])
        g.add_edge(V[1],V[2])
        g.add_edge(V[2],V[0])
        g.add_edge(V[2],V[1])
        return g
        
    elif len(V)<3:
        raise ValueError
        
    else:
        W = V[1:]
        return splice(random_graph_spliced(g,W,degree_dict),V[0],degree_dict[V[0]]['in'])
    

