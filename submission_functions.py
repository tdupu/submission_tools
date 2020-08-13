#!/usr/bin/env python3

"""
Some of the strings in this file have issues is we don't run python3.

"""

import json
import sys
#sys.path.append('../excel_tools')
#
#to get these paths I used the pwd unix command.
#
sys.path.append('/Users/taylordupuy/Documents/web-development/dev/excel_tools')

my_system_path ='/Users/taylordupuy/Documents/web-development/dev/submission_tools/'
path_to_variables_j = my_system_path + 'variables.json'
path_to_constants_j = my_system_path + 'constants.json'
path_to_testing_j = my_system_path + 'testing.json'

from table_editor import SheetObject


def tmode(j):
    """
    set_test_mode
    set_testing_mode
    
    Seem to be taken or something...
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
                message = "new password has been set... <br> "
            else:
                message = "user_id and password match... <br> "
        else:
            authenticated = 0
            message = "invalid user_id and password. <br>"
                
    if n>2:
        authenticated = 0
        message = """
        invalid user_id and password. (Something unusual happened. Please contact the instructor.) <br>
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
            Submission number %s created for assignment %s, problem %s. This is new. <br> Passing to PDF recorder... <br>.
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
                Submission for assignment %s, problem %s was rejected. This submission is  now locked. (It has been passed to reviewers or is past the due date) <br>
                """ % (assignment,problem)
                write_file =0
                
            if is_locked ==0:
                S.replace(old_entry,new_entry)
                S.save()
                message = """
                Submission number %s for assignment %s, problem %s was created. Submission number %s has been overwritten. Passing to PDF writer...<br>
                """ % (new_submission_number, old_entry['submission_number'],assignment,problem)
                write_file = 1
                
        else:
            message = "The database is broken! Multiple submissions for this problem exist in the database! Please send this error message to the person running this course. <br> "
            write_file =0
            
        if write_file ==1:
            increment_submission_number()
    
    else:
        message = """
        Submission for assignment %s, problem %s rejected. This is not a valid submission. <br>
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
    j=0 # returns reviewer number or zero
    message = '' #holy moly if you don't initialize this string it gets mad
    if n==0:
        message = "Review for submission number %s rejected. Invalid submission number. <br>" % submission_number
        j=0
    if n==1:
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
            Review for submission number %s rejected. Not a valid reviewer. <br>
            """ % submission_number
            j=0
     
    if j!=0 and is_locked[j-1]:
        j=0
        message = """
        Review for submission number %s rejected. Submission is closed. <br>
        """ % submission_number
    
    if j!=0:
        try:
            score = int(score)
            if not (0<=score and score <= 10):
                j=0
                message="""
                Review for submission number %s rejected. Score must be between 0 and 10. <br>
                """ % submission_number
        except:
            j=0
            message = """
            Review for submission number %s rejected. Score is not a valid integer. <br>
            """ % submission_number
        
        if review == '':
            j=0
            message ="""
            Review for submission number %s was rejected. Empty review. <br>
            """
    
    return message, j
    
def write_review(user_id,submission_number,score,review,timestamp):
    message,j=is_valid_review(user_id,submission_number,score,review,timestamp)
        
    if j!=0: #write the review
        CONSTANT_DATA = get_CONSTANT_DATA()
        path_to_data = CONSTANT_DATA['path_to_data']
        roster_name = CONSTANT_DATA['roster_name']
        S=SheetObject(path_to_data + roster_name, "submissions")
        
        old_entry = S.get({'submission_number':submission_number})[0]
        
        #NEVER DO THIS WITH DICTIONARIES
        #new_entry = old_entry
        new_entry = {}
        for key in S.keys:
            new_entry[key] = old_entry[key]
        
        
        #With the old command...
        #commands below just modify old_entry in memory.
        new_entry['review%s' % j] = review
        new_entry['reviewer%s_score' % j] = int(score) #not scorej, holy shit this bug took me forever.
        new_entry['review%s_timestamp' % j] = timestamp
        new_entry['new_review%s' % j] = 1
        
        #debuggin
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
    


#def write_review(user_id,submission_number,score,review,timestamp):
#    S = SheetObject(path_to_data + "roster.xlsx", "submissions")

