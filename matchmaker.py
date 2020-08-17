import json
import sys
import time

#sys.path.append('../excel_tools')
#to get these paths I used the pwd unix command.

sys.path.append('/Users/taylordupuy/Documents/web-development/dev/excel_tools')
path_to_data = '/Users/taylordupuy/Documents/web-development/data/algebra-one/20/f/'
my_system_path ='/Users/taylordupuy/Documents/web-development/dev/submission_tools/'
path_to_variables_j = my_system_path + 'variables.json'
path_to_constants_j = my_system_path + 'constants.json'
path_to_testing_j = my_system_path + 'testing.json'

from table_editor import SheetObject
from table_functions import *
from matchmaker_functions import *
from submission_functions import *


"""
GLOBAL VARIABLES
"""

#testing?
is_test = sys.argv[1]
if is_test ==1:
    tmode(1)
else:
    tmode(0)

#these need to be imported from CONSTANTS.json
roster_name = "roster-test.xlsx"
CURRENT_TIME = int(time.time())

S = SheetObject(path_to_data + roster_name,"submissions")
X = S.get({"new_submission":1})

probs, dictX = dicts_by_key(['assignment','problem'],X)
#dictY = {} #we will store dictY[ [assignment,problem] ] dictionary of replacements
no_matches = []

for prob in probs:
    #INITIALIZE STUFF I NEED TO BUILD THE GRAPH
    V = [v['netid'] for v in dictX[prob]]
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
    try:
        g=match_up(g,V,degree_dict)
        #make a dictionary of replacement entries
        #replacement = {}
        print("FOUND A MATCH:" + str(prob) + "\n")
        for e in g.edges():
            print(e)
            
        for v in V:
            vv=match_key(dictX[prob],'netid',v)[0]
            w = copyd(vv)
            reviewersv = [edge[0] for edge in g.edges(to_node=v)]
            #print(reviewersv)
            w["reviewer1"] = reviewersv[0]
            w["reviewer2"] = reviewersv[1]
            w["reviewer1_assignment_time"] = int(time.time()) #PHP style: =now-197? in sec
            w["reviewer2_assignment_time"] = int(time.time())
            w["new_submission"]=0
            w["submission_locked"]=1
            w["new_match"]=1
            S.replace(vv,w)
            S.save()
            print(" * %s will be reviewed by %s and %s \n" % (v,reviewersv[0],reviewersv[1]))
            #print("matches made and saved for (assignment,problem):"  + str(prob[0]) +" " + str(prob[1]) + "\n" )
       
    
    except ValueError as e:
        print("could not match (problem, assignment):" + str(prob))
        print(e)
        print('\n')
        no_matches.append(prob)
    
    """
    we could store the graphs somewhere if we wanted...
    """
    
    

        
print("\n Here are the (assignment,problems) we couldn't match:")
print(no_matches)
        
        
#    dictY[prob]=replacement

#"""
#for prob in probs:
#    for v in dictX[prob]:
#        S.replace(v,dictY[prob][v])
#        S.save()
#"""
