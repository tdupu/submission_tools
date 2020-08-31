import json
import sys
import time


"""
BE SURE TO UPDATE THE ABSOLUTE INSTALL PATH:

    test with path:
        "matchmaker.py /path/to/data/ 1
    test:
        matchmaker.py
    real deal:
        matchmaker.py /path/to/data 0
        
    #sys.path.append('../excel_tools')
    #to get these paths I used the pwd unix command.
    
PATH_TO_DATA = '/Users/taylordupuy/Documents/web-development/data/algebra-one/20/f/'

"""

INSTALL_PATH = '/users/t/d/tdupuy/dev/submission_tools/'
#INSTALL_PATH ='/Users/taylordupuy/Documents/web-development/dev/submission_tools/'
sys.path.append(INSTALL_PATH+"../excel_tools")
#sys.path.append('/Users/taylordupuy/Documents/web-development/dev/excel_tools')

from table_editor import SheetObject
from table_functions import *
from matchmaker_functions import *
from submission_functions import *
        
#path_to_variables_j = INSTALL_PATH + 'variables.json'
#path_to_constants_j = INSTALL_PATH + 'constants.json'
#path_to_testing_j = INSTALL_PATH + 'testing.json'

CURRENT_TIME = int(time.time())

"""
PARSE INPUTS:
"""
if len(sys.argv)==1:
    PATH_TO_DATA = get_path_to_data()
    tmode(1,PATH_TO_DATA)
elif len(sys.argv)>=2:
    PATH_TO_DATA = sys.argv[1]
    tmode(1,PATH_TO_DATA)
elif len(sys.argv)==3:
    is_test = int(sys.argv[2])
    tmode(is_test,PATH_TO_DATA)
else:
    tmode(1)

roster_name = get_roster_name(PATH_TO_DATA)
course_name = get_course_name(PATH_TO_DATA)

print("running matchmaker.py... ")
print("test mode: %s " % get_test_mode(PATH_TO_DATA))
print("path to data: %s " % PATH_TO_DATA)
print("roster name: %s " % roster_name)
print("course name: %s " % course_name)


"""
GLOBAL VARIABLES
"""


    

#testing?


S = SheetObject(PATH_TO_DATA + roster_name,"submissions")
X = S.get({"new_submission":1})

probs, dictX = dicts_by_key(['assignment','problem'],X)
#dictY = {} #we will store dictY[ [assignment,problem] ] dictionary of replacements
no_matches = []

for prob in probs:
    #INITIALIZE STUFF I NEED TO BUILD THE GRAPH
    V = [v['netid'] for v in dictX[prob]]
    V = kill_repeats(V) #not sure why we have repeats
    """
    The method below still probably works.
    """
    #g = Graph()
    #for v in V:
    #    g.add_node(v)
    #
    #indeg=2
    #outdeg=2
    #
    #degree_dict = {}
    #for v in V:
    #    degree_dict[v] = {}
    #    degree_dict[v]['in']=indeg
    #    degree_dict[v]['out']=outdeg
    #
    #BUILD THE DIRECTED RANDOM GRAPH
    #worked = None
    #try:
    #    g = get_random_graph(g,V,degree_dict,100)
    #    #g=random_graph_spliced(g,V,degree_dict)
    #    make a dictionary of replacement entries
    #    replacement = {}
    #    print("FOUND A MATCH:" + str(prob) + "\n")
    #    worked = True
    #except ValueError as e:
    #    print("could not match (problem, assignment)=" + str(prob) + "not enough entries")
    #    no_matches.append(prob)
        
    n = len(V)
    if n<=2:
        print("could not match (problem,assignment)=" + str(prob) + ", not enough entries")
        no_matches.append(prob)
        
    if n>=3:
        g = get_easy_graph(V)
        #print("SIZE")
        #print(n)
        #print("GRAPH")
        for e in g.edges():
            print(e)
        #for v in V:
        #    print(v)
        #    print(g.edges(to_node=v))
        print("FOUND A MATCH:" + str(prob) + "\n")
        
        for v in V:
            #vv=match_key(dictX[prob],'netid',v)[0]
            vv = S.get({'assignment':prob[0],'problem':prob[1],'netid':v})[0]
            w = copyd(vv)
            reviewersv = [edge[0] for edge in g.edges(to_node=v)]
            #print(len(reviewersv))
            w["reviewer1"] = reviewersv[0]
            w["reviewer2"] = reviewersv[1]
            
            print(" * %s will be reviewed by %s and %s \n" % (v,reviewersv[0],reviewersv[1]))
            w["reviewer1_assignment_time"] = int(time.time()) #PHP style: =now-197? in sec
            w["reviewer2_assignment_time"] = int(time.time())
            w["new_submission"]=0
            w["submission_locked"]=1
            w["new_match"]=1
            #print(vv)
            #print(w)
            S.replace(vv,w)
            S.save()

    
    """
    we could store the graphs somewhere if we wanted...
    """
    
print("""
Here are the (assignment,problems) we couldn't match:""")
print(no_matches)
        
        
#    dictY[prob]=replacement

#"""
#for prob in probs:
#    for v in dictX[prob]:
#        S.replace(v,dictY[prob][v])
#        S.save()
#"""


