#!/usr/bin/env python3

"""
Some of the strings in this file have issues is we don't run python3.
"""

import json
import sys
import os
import inspect

sys.path.append('../excel_tools')
sys.path.append('/Users/taylordupuy/Documents/web-development/dev/excel_tools')
my_system_path ='/Users/taylordupuy/Documents/web-development/dev/submission_tools/'
path_to_variables_j = my_system_path + 'variables.json'
path_to_constants_j = my_system_path + 'constants.json'
path_to_testing_j = my_system_path + 'testing.json'

from table_editor import SheetObject
from table_functions import *


"""
#########################
FLAG FUNCTIONS
#########################
All flags in this project are 0 or 1 rather than true are false.
Unset positive natural numbers are -1. 

The new_review tags are only for the reviewer emails as a receipt.
The new_completion tag is notify submitters and reviewers that the script is locked.
    new_review1
    new_review2
    
The new_match tags are both for the reviwers and the submitter.
    
For total_score1:
    review1_score = -1
    review2_score = -1
    
For total_score2:
    new_completion (should be if both reviewers have submitted)
    

"""

def get_current_directory():
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    return path
    
def set_key(sub,key,entry):
    """
    WARNING: this currently doesn't check that the entry is valid.
    """
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S = SheetObject(path_to_data + roster_name,'submissions')
    S.set(sub,key,entry)
    message = S.save()
    return message
    
def mark_closed(sub):
    message = set_key(sub,'closed',1)
    return message
    
def unmark_closed(sub):
    message = set_key(sub,'closed',0)
    return message
    
def mark_new_completion(sub):
    message = set_key(sub,'new_completion',1)
    return message
    
def unmark_new_completion(sub):
    message = set_key(sub,'new_completion',0)
    return message
    
def mark_new_match(sub):
    message = set_key(sub, 'new_match',1)
    return message
    
def unmark_new_match(sub):
    message = set_key(sub,'new_match',0)
    return message
    
def mark_locked(sub):
    message = set_key(sub,'submission_locked',1)
    return message
    
def get_reviewer_index(user,sub):
    j=0
    if user == sub['reviewer1']:
        j=1
    elif user == sub['reviewer2']:
        j=2
    return j
    
def unmark_new_review(sub,j):
    mykey = "new_review%s" % j
    message = set_key(sub,mykey,0)
    return message
    
def mark_new_review(sub,j):
    mykey = "new_review%s" % j
    message = set_key(sub,mykey,1)
    return message

def mark_review_locked(sub,j):
    mykey = "review%s_locked" % j
    message = set_key(sub,mykey,1)
    return message

def unmark_review_locked(sub,j):
    mykey = "review%s_locked" % j
    message = set_key(sub,mykey,0)
    return message
    
def score1(sub):
    s1 = sub['reviewer1_score']
    s2 = sub['reviewer2_score']
    if s1>-1 and s2>-1:
        s = (s1+s1)/2
        message = set_key(sub,'total_score1',s)
    else:
        raise ValueError("reviews are not complete")
    return message
    
def score2(sub):
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S = SheetObject(path_to_data+roster_name,'submissions')
    assignment = sub['assignment']
    problem = sub['problem']
    reviewer1 = sub['reviewer1']
    reviewer2 = sub['reviewer2']
    s1 = sub['reviewer1_score']
    s2 = sub['reviewer2_score']
    sub1 = S.get({'netid':reviewer1,'assignment':assignment,'problem':problem})
    sub2 = S.get({'netid':reviewer1,'assignment':assignment,'problem':problem})
    r1 = sub1['total_score1']/10
    r2 = sub2['total_score2']/10
    if r1==0 and r2 ==0:
        total_score2 = sub['total_score1']
        message = "r1=r2=0, to total_score1 = total_score2"
    else:
        w1 = r1/(r1+r2)
        w2 = r2/(r1+r2)
        total_score2 = w1*s1 + w2*s2
        message = "the weighed average %s was recorded." % total_score2
        set(sub,'total_score2',total_score2)
    return message
    
    
"""
JSON FILE MANIPULATION: testing mode, server_switching.
"""

def tmode(j):
    """
    Note: this function is named so weirdly because set_test_mode and set_testing_mode seem to be taken by python.
    
    This turns testing mode on and off.
    """
    f=open(path_to_variables_j,'r')
    variables=json.load(f)
    f.close()
    variables['testing'] = j
    with open(path_to_variables_j, 'w') as outfile:
        json.dump(variables,outfile)
    if j==0:
        message = "testing mod off."
    if j==1:
        message = "testing mode on."
    return message
    
def webmode(j):
    """
    set_test_mode
    set_testing_mode
    
    Seem to be taken or something...
    """
    f=open(path_to_variables_j,'r')
    variables=json.load(f)
    f.close()
    variables['server_down'] = j
    with open(path_to_variables_j, 'w') as outfile:
        json.dump(variables,outfile)
    if j==0:
        message = "webpage off."
    if j==1:
        message = "webpage on."
    return message
    

def increment_submission_number():
    f=open(path_to_variables_j,'r')
    variables=json.loads(f.read())
    f.close()
    variables['submission_number'] = variables['submission_number']+1
    f = open(path_to_variables_j,'w')
    json.dump(variables,f)
    f.close()
    
    return "submission number: %s. " % variables['submission_number']

def get_submission_count():
    f=open(path_to_variables_j,'r')
    variables=json.loads(f.read())
    f.close()
    return variables['submission_number']

def get_CONSTANT_DATA():
    ff = open(path_to_variables_j,'r')
    variables = json.load(ff)
    ff.close()
    test_on = variables['testing']

    if test_on ==1:
        f = open(path_to_testing_j,'r')
        
    if test_on==0:
        f = open(path_to_constants_j,'r')
        
    CONSTANT_DATA = json.load(f)
    f.close()
    return CONSTANT_DATA
    
def get_path_to_data():
    CONSTANT_DATA = get_CONSTANT_DATA()
    return CONSTANT_DATA['path_to_data']
    
    
"""
#########################
MAIN FUNCTIONS
#########################
"""

def authenticate(user_id, pass1, pass2, newpass):
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    R = SheetObject(path_to_data + roster_name,'roster')
    students = R.get({'netid':user_id})
    n = len(students)
    authenticated = 0
    if n==0:
        message = "invalid user_id and password. <br>"
        authenticated = 0
    if n==1:
        old_entry = students[0]
        password = old_entry['password']
        if password == pass1:
            authenticated = 1
            if pass1 == pass2 and len(newpass) >0:
                new_entry = old_entry
                new_entry['password'] = newpass
                message = "new password has been set. <br> "
            else:
                message = "<i> %s upload report </i> <br>" % user_id
        else:
            authenticated = 0
            message = "invalid user_id and password. <br>"
                
    if n>2:
        authenticated = 0
        message = """
        invalid user_id and password. (multiple users! please copy-paste this entire upload report in an email to tdupuy@uvm.edu.) <br>
        """
        
    return message, authenticated

def is_valid_assignment(assignment, problem, timestamp, check_due_date=False):
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    A = SheetObject(path_to_data+roster_name,'assignments')
    
    """
    print( "roster name: %s <br>" % roster_name)
    print( "path_to_data: %s <br>" % path_to_data )
    print( "all assignments:" )
    for x in A.get({}):
        print(x)
        print( "<br>" )
    """
    
    """
    y=A.get({})[8]['assignment']
    print('y is %s <br>' % y )
    print('y had type %s <br>' % type(y))
    print('assignment has type %s <br>' % type(assignment) )
    print(type(y)==type(assignment))
    print(type(y)==int)
    print(type(assignment)==int)
    """
    assignment = int(assignment)
    problem = int(problem)
    
    query = {'assignment':assignment, 'problem':problem}
    entries = A.get(query)
    
    """
    for entry in entries:
        print(entry)
        print("<br>")
        print(len(entries))
    """
    
    n=len(entries)
    if n==1:
        return True
    if n==0:
        return False
    if n>0:
        raise ValueError("Assignment data is inconsistent. Please contact Professor Dupuy with this error message. <br>")

def submit_problem(user_id,assignment,problem,timestamp, check_due_date=False):
    """
    
    """
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S = SheetObject(path_to_data + roster_name,'submissions')
    query = {'netid':user_id, 'assignment':assignment,'problem':problem}
    if is_valid_assignment(assignment,problem,timestamp):
        old_entries = S.get(query)
        n = len(old_entries)
        write_file = 1
        
        if n==0:
            new_submission_number = get_submission_count()
            new_entry = {}
            new_entry['netid'] = user_id
            new_entry['assignment'] = assignment
            new_entry['problem'] = problem
            new_entry['submission_number'] = new_submission_number
            new_entry['submission_time'] = timestamp
            new_entry['new_submission']=1
            new_entry['submission_locked']=0
            new_entry['closed']=0
            new_entry['total_score1']=0
            new_entry['total_score2']=0
            new_entry['reviewer1_assignment_time']=-1
            new_entry['reviewer1']=''
            new_entry['reviewer1_score']=-1
            new_entry['review1']=''
            new_entry['review1_timestamp']=-1
            new_entry['review1_locked']=0
            new_entry['reviewer2_assignment_time']=-1
            new_entry['reviewer2']=''
            new_entry['reviewer2_score']=-1
            new_entry['review2']=''
            new_entry['review2_timestamp']=-1
            new_entry['review2_locked']=0
            new_entry['new_submission']=1
            new_entry['new_match']=0
            new_entry['new_review1']=0
            new_entry['new_review2']=0
            new_entry['new_completion']=0
            S.append(new_entry)
            S.save()
            message = """
            *submission %s, assignment %s, problem %s created. new. <br>
            """ % (timestamp, assignment, problem)
            write_file = 1
            
        elif n==1:
            old_entry = old_entries[0]
            
            #The trickiest fucking bug in the world:
            #new_entry = old_entry
            
            #you need to make a new blank dictionary...
            #...otherwise it just points to the old one
            new_entry = {}
            for key in S.set_of_keys:
                new_entry[key] = old_entry[key]
            
            new_submission_number = get_submission_count()
            #new_entry['netid'] = user_id
            #new_entry['assignment'] = assignment
            #new_entry['problem'] = problem
            new_entry['submission_number'] = new_submission_number
            new_entry['submission_time'] = timestamp
            #new_entry['new_submission']=1
            #new_entry['submission_locked']=0
            
            is_locked = old_entry['submission_locked'] #bug: entries -> entry
            
            if is_locked ==1:
                message = """
                *assignment %s, problem %s rejected. locked. <br>
                """ % (assignment,problem)
                write_file =0
                
            if is_locked ==0:
                S.replace(old_entry,new_entry)
                S.save()
                message = """
                *submission %s, assignment %s, problem %s created. <br>
                submission %s overwritten. <br>
                """ % (new_submission_number,assignment,problem,old_entry['submission_number'])
                write_file = 1
                
        else:
            message = """
            *assigment %s, problem %s rejected. multiple entries in database. contact instructor with this message and copy-paste this message. <br> """
            write_file =0
            
        if write_file ==1:
            increment_submission_number()
    
    else:
        message = """
        *assignment %s, problem %s rejected. not a valid submission. <br>
        """ % (assignment,problem)
        write_file = 0
        
    dataentry = {}
    dataentry["uploadOk"] = write_file
    if write_file ==1:
        dataentry["submission_number"]=new_submission_number
    else:
        dataentry["submission_number"]=-1
    return message,dataentry

def is_valid_review(user_id,submission_number,score,review,timestamp):
    """
    returns a message and reviewer number if valid.
    returns a message and j=0 if not valid.
    """
    """
    if any of the entries are empty, kill it.
    if a previous review exists and its not the end of the day, write it.
    if a previous review exists and it its past the end of the day, kill it.
    """
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S=SheetObject(path_to_data + roster_name, "submissions")
    entries = S.get({"submission_number":submission_number})
    n = len(entries)
    j=-1 # returns reviewer number or zero
    message = '' #holy moly if you don't initialize this string it gets mad
    
    if review == '':
        j=0
        message =""
    
    if n==0 and j!=0:
        message = "*review of %s rejected. invalid submission number. <br>" % submission_number
        j=0
    if n==1 and j!=0:
        submission = entries[0]
        old_entry = submission #keep a copy for the replace function later
        reviewer1 = submission['reviewer1']
        reviewer2 = submission['reviewer1']
        is_locked = [submission['review1_locked'],submission['review2_locked']]
    
        if user_id == reviewer1:
            j=1
        elif user_id == reviewer2:
            j=2
        else:
            message = """
            *review of %s rejected. incorrect reviewer. <br>
            """ % submission_number
            j=0
     
    if j>0 and is_locked[j-1]:
        j=0
        message = """
        *review of %s rejected. closed. <br>
        """ % submission_number
    
    if j>0:
        try:
            score = int(score)
            if not (0<=score and score <= 10):
                j=0
                message="""
                *review of %s rejected. score must be between 0 and 10. <br>
                """ % submission_number
        except:
            j=0
            message = """
            review of %s rejected. score must be an integer. <br>
            """ % submission_number
    
    return message, j
    
def write_review(user_id,submission_number,score,review,timestamp):
    message,j=is_valid_review(user_id,submission_number,score,review,timestamp)
        
    if j!=0: #write the review
        CONSTANT_DATA = get_CONSTANT_DATA()
        path_to_data = CONSTANT_DATA['path_to_data']
        roster_name = CONSTANT_DATA['roster_name']
        S=SheetObject(path_to_data + roster_name, "submissions")
        
        old_entry = S.get({'submission_number':submission_number})[0]
        
        #NEVER DO THIS WITH DICTIONARIES: new_entry = old_entry
        #it have new_entry point to old_entry in memory
        #note: copyd function in ../excel_tools/table_functions.py
        new_entry = {}
        for key in S.keys:
            new_entry[key] = old_entry[key]
        
        new_entry['review%s' % j] = review
        new_entry['reviewer%s_score' % j] = int(score) #not scorej, holy shit this bug took me forever.
        new_entry['review%s_timestamp' % j] = timestamp
        new_entry['new_review%s' % j] = 1
        
        #check to see if this new review makes the entry complete.
        k = (j%2) +1 #other index
        if old_entry['reviewer%s_score' % k]>-1:
            new_entry['new_completion']=1
        
        
        #DEBUG
        #A=set(list(new_entry.keys()))
        #B=set(list(old_entry.keys()))
        #print(B.issubset(A))
        #
        #for a in list(old_entry):
        #    print(a)
        #
        #for b in list(new_entry):
        #    print(b)
        #no such entry old_entry
        S.replace(old_entry,new_entry)
        S.save()
            
    return message
