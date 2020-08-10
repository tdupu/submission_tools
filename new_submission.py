#!/usr/bin/env python

import sys
import json

#https://stackoverflow.com/questions/1054271/how-to-import-a-python-class-that-is-in-a-directory-above
sys.path.append('..')
from excel_tools.table_editor import SheetObject

path_to_data = "../../data/algebra-one/20/f/" #rooted from where jupyter was launched


def authenticate(user_id, pass1, pass2, newpass):
    R = SheetObject(path_to_data + 'roster.xlsx','roster')
    students = R.get_entries({'netid':user_id})
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
    A = SheetObject(path_to_data+'roster.xlsx','assignments')
    query = {'assignment':assignment, 'problem':problem}
    entries = A.get(query)
    n=len(entries)
    if n==1:
        return True
    if n==0:
        return False
    if n>0:
        raise ValueError("Something is terribly wrong with Professor Dupuy's assignment data. <br> Please contact him and tell him about this message. <br>")

def submit_problem(user_id,assignment,problem,timestamp, check_due_date=False):
    """
    Assumes SheetObject S, with submission data is already opened and is global.
    """
    S = SheetObject(path_to_data + 'roster.xlsx','submissions')
    query = {'user_id':user_id, 'assignment':assignment,'problem':problem}
    if is_valid_assignment(query):
        
        new_entry = {}
        new_entry['user_id'] = user_id
        new_entry['assignment'] = assignment
        new_entry['problem'] = problem
        new_entry['submission_number'] = timestamp
        new_entry['submission_time'] = timestamp
        
        old_entries = S.get(query)
        n = len(old_entries)
        write_file = 1
        
        if n==0:
            S.append(new_entry)
            S.save()
            message = """
            submission number %s: assignment: %s, problem %s, <br> Passing to PDF recorder... <br>.
            """ % (timestamp, assignment, problem)
            write_file = 1
            
        elif n==1:
            old_entry = old_entries[0]
            is_locked = old_entries['submission_locked']
            if is_locked ==1:
                message = """
                Submission for assignment %s, problem %s is locked because it has been passed to reviewers or is past the due date.
                <br> If this message is incorrect please contact Professor Dupuy. <br>
                """ % (assignment,problem)
                write_file =0
                
            elif is_locked ==0:
                S.replace(old_entry,new_entry)
                S.save()
                message = """
                submission number %s: submission number %s for assignment %s, problem %s will be overwritten. Passing to PDF recorder... <br>
                """ % (timestamp, old_entries['submission_number'],assignment,problem)
                write_file = 1
        else:
            message = "Oh boy... multiple submissions for this problem exist in the database! <br> Please alert Professor Dupuy that the database is recording multiple entries. <br> ")
            write_file =0
        
        return message,write_file

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
    
    
    S=SheetObject(path_to_data + "roster.xlsx", "submissions")
    entries = S.get({"submission_number":submission_number})
    n = len(entries)
    j=0 # returns reviewer number or zero
    if n==0:
        message = "Review for submission number %s rejected. Invalid submission number. <br>" % submission_number
        j=0
    if n==1:
        submission = entries[0]
        old_entry = submission #keep a copy for the replace function later
        reviewer1 = submission['reviewer1']
        reviewer2 = submission['reviewer1']
        is_locked = [relevant_sub['review1_locked'],relevant_sub['review2_locked']]
    
    #we need the user to be a reviewer
    if j!=0:
        if user_id == reviewer1:
            j=1
        elif user_id == reviewer2:
            j=2
        else:
            message = """
            Review for submission number %s rejected. Not a valid reviewer. <br>
            """ % submission_number
            j=0
        else:
            if is_locked[j-1]:
                j=0
                message = """
                Review for submission number %s rejected. Submission is closed. <br>
                """ % submission_number
    if j!=0:
        try score = int(score):
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
    S = SheetObject(path_to_data + "roster.xlsx", "submissions")
    

"""
START PROCESSING DATA
"""
        
user_id = data['user_id']
temp_filename = "temp.json"
f = open(path_to_data+temp_filename,'r')
data=json.loads(f.read())

"""
PROCESS SUBMISSIONS
"""

write_file = {1:1,2:1,3:1,4:1,5:1,6:1}

for i in range(1,6):
    query = {}
    submission_number = data['timestamp']
    assignment = data['assignment%s' % i]
    problem = data['assignment%s' % i]
    timestamp = data['timestamp']
    
    if is_valid_assignment(assignment,problem,timestamp)
        query['user_id'] = user_id
        query['assignment'] = assignment
        query['problem'] = problem
        is_allowed, message = submit_problem(user_id,assignment,problem,timestamp)
        write_file[i]=is_allowed
    
    else:
        message = """
        assignment %s, problem %s is not a valid problem or is past the due date. <br>
        \n
        """ % (assignment,problem)
        write_file[i]=0
        
    output_message = output_message + message.


#this will be read by the PHP file to determine if one should attempt to upload the PDFs
with open(path_to_data + 'temp.json', 'w') as outfile:
    json.dump(write_file, outfile)

"""
PROCESS REVIEWS
"""

for i in range(1,11):
    j=0
    user_id = data['user_id']
    timestamp = data['timestamp']
    submission_number = data['subnumber%s' % i] #of the review
    review = data['review%s' % i]
    score = data['score%s' % i]
    
    message, j = is_valid_review(user_id,submission_number,review,score,timestamp)
    
    old_entry = S.get({'submission_number':submission_number})
    new_entry = old_entry

    if j!=0:
        new_entry['review%s' % j] = review
        new_entry['score%s' % j] = int(score)
        new_entry['review%s_timestamp' % j] = timestamp
        S.replace(old_entry,new_entry)
        S.save()
    
    output_message = output_message + message
        
print(output_message)




