
import json
import sys
sys.path.append('..')
from excel_tools.table_editor import SheetObject

def tmode(j):
    """
    set_test_mode
    set_testing_mode
    
    Seem to be taken or something...
    """
    f=open('variables.json','r')
    variables=json.load(f)
    f.close()
    variables['testing'] = j
    with open('variables.json', 'w') as outfile:
        json.dump(variables,outfile)
    if j==0:
        message = "testing mod off."
    if j==1:
        message = "testing mode on."
    return message

def increment_submission_number():
    f=open('variables.json','r')
    variables=json.loads(f.read())
    f.close()
    variables['submission_number'] = variables['submission_number']+1
    f = open('variables.json','w')
    json.dump(variables,f)
    f.close()
    
    return "submission number: %s. " % variables['submission_number']

def get_submission_count():
    f=open('variables.json','r')
    variables=json.loads(f.read())
    f.close()
    return variables['submission_number']

def get_CONSTANT_DATA():
    ff = open('variables.json','r')
    variables = json.load(ff)
    ff.close()
    test_on = variables['testing']

    if test_on ==1:
        f = open('testing.json','r')
        
    if test_on==0:
        f = open('constants.json','r')
        
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
    
    """
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S = SheetObject(path_to_data + roster_name,'submissions')
    #query = {'user_id':user_id, 'assignment':assignment,'problem':problem}
    if is_valid_assignment(user_id,assignment,problem):
        
        new_entry = {}
        new_entry['user_id'] = user_id
        new_entry['assignment'] = assignment
        new_entry['problem'] = problem
        new_entry['submission_number'] = get_submission_count()
        new_entry['submission_time'] = timestamp
        new_entry['new_submission']=1
        
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
            message = "Oh boy... multiple submissions for this problem exist in the database! <br> Please alert Professor Dupuy that the database is recording multiple entries. <br> "
            write_file =0
            
        if write_file ==1:
            increment_submission_number()
    
    else:
        message = """
        Submission for assignment %s, problem %s rejected. This is not a valid submission. <br>
        """ % (assignment,problem)
        write_file = 0
            
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
        new_entry = old_entry
        
        new_entry['review%s' % j] = review
        new_entry['score%s' % j] = int(score)
        new_entry['review%s_timestamp' % j] = timestamp
        new_entry['new_review%s' % j] = 1
        S.replace(old_entry,new_entry)
        S.save()
            
    return message
    


#def write_review(user_id,submission_number,score,review,timestamp):
#    S = SheetObject(path_to_data + "roster.xlsx", "submissions")

