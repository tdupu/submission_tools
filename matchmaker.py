import json
import sys

import time
from matchmaker_functions import *

#sys.path.append('../excel_tools')
#to get these paths I used the pwd unix command.

sys.path.append('/Users/taylordupuy/Documents/web-development/dev/excel_tools')
my_system_path ='/Users/taylordupuy/Documents/web-development/dev/submission_tools/'
path_to_variables_j = my_system_path + 'variables.json'
path_to_constants_j = my_system_path + 'constants.json'
path_to_testing_j = my_system_path + 'testing.json'

from table_editor import SheetObject

"""
TODO: import the function that shuts down the server when using this code.
"""


"""
GLOBAL VARIABLES
"""

#confirm that we are testing
tmode(1)


#these need to be imported from CONSTANTS.json
path_to_data = ""
roster_name = "roster-test.xlsx"
CURRENT_TIME = int(time.time())

S = SheetObject(path_to_data + roster_name,"submissions.xlsx")
X = S.get({"new_submission":1})

probs, dictX = dicts_by_key(['assignment','problem'],X)
dictY = {} #we will store dictY[ [assignment,problem] ] dictionary of replacements

for prob in probs:
    
    #INITIALIZE STUFF I NEED TO BUILD THE GRAPH
    V = dictX[prob]
    g = Graph()
    for v in V:
        g.add_node(v)
        
        
    indeg=2
    outdeg=2
      
    degree_dict = {}
    for v in V:
        degree_dict[v] = {}
        degree_dict[v]['in']=indeg
        degree_dict[v]['out']=outdeg
    
    #BUILD THE DIRECTED RANDOM GRAPH
    g=match_up(g,V,degree_dict)
    
    """
    we could store the graphs somewhere if we wanted...
    """
    
    
    #make a dictionary of replacement entries
    replacement = {}
    for v in V:
        w = copyd(v)
        reviewersv = [edge[0]['netid'] for edge in g.edges(to_node=v)]
        w["reviewer1"] = reviewersv[0]
        w["reviewer2"] = reviewersv[1]
        w["reviewer1_assignment_time"] = int(time.time()) #PHP style: =now-197? in sec
        w["reviewer2_assignment_time"] = int(time.time())
        w["new_submission"]=0
        w["submission_locked"]=1
        w["new_match"]=1
        replacement[v]=w
        
    dictY[prob]=replacement
    
for prob in probs:
    for v in dictX[prob]:
        S.replace(v,dictY[prob][v])
        S.save()
