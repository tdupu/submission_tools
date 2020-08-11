
import json
import sys
sys.path.append('..')
from submission_functions import *

def test_authenticate1():
    message1,result1 = authenticate('tdupuy','tdupuy','','')
    assert result1 ==0
    
def test_authenticate2():
    message2,result2 = authenticate('cvincen1','carrot','carrot','carrot')
    assert result2 ==1
    
def test_is_valid_assignment():
    value=is_valid_assignment(1,2,1)
    assert value==True
    
def test_is_valid_assignement2():
    user_id = "jschmoe"
    assignment = 1
    problem = 1
    timestamp = 129837
    #there was a bug in submit problem where is_valid_assignment was called with user_id
    assert is_valid_assignment(problem,assignment,timestamp)

def test_get():
    """
    The issue here was that I was using 'user_id' instead of 'netid' in my query.
    """
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S=SheetObject(path_to_data + roster_name, "submissions")
    user_id = "jschmoe"
    assignment = 1
    problem = 1
    timestamp = 129837
    query = {'netid':user_id, 'assignment':assignment,'problem':problem}
    answers=S.get(query)
    assert len(answers)==1

def test_submit_problem_manual():
    """
    note that we used new_entry = old_entry.
    Because of this all changes made to new_entry are made to old_entry.
    We need to *not* do this in other places.
    """
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S = SheetObject(path_to_data + roster_name,'submissions')
    user_id = "jschmoe"
    assignment = 1
    problem = 1
    timestamp = 129837
    query = {'netid':user_id, 'assignment':assignment,'problem':problem}
    old_entries = S.get(query)
    old_entry = old_entries[0]
    new_entry = old_entry
    new_submission_number = get_submission_count()
    new_entry['netid'] = user_id
    new_entry['assignment'] = assignment
    new_entry['problem'] = problem
    new_entry['submission_number'] = new_submission_number
    new_entry['submission_time'] = timestamp
    new_entry['new_submission']=1
    new_entry['submission_locked']=0
    feedback_entries = S.get(old_entry)
    
    assert feedback_entries == old_entries
    
    #message,write_file = submit_problem(user_id,assignment,problem,timestamp)
    #print(message)
    
def test_submit_problem_manual4():
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S = SheetObject(path_to_data + roster_name,'submissions')
    user_id = "jschmoe"
    assignment = 1
    problem = 1
    timestamp = 129837
    query = {'netid':user_id, 'assignment':assignment,'problem':problem}
    old_entries = S.get(query)
    old_entry = old_entries[0]
    new_entry = old_entry
    new_submission_number = get_submission_count()
    new_entry['netid'] = user_id
    new_entry['assignment'] = assignment
    new_entry['problem'] = problem
    new_entry['submission_number'] = new_submission_number
    new_entry['submission_time'] = timestamp
    new_entry['new_submission']=1
    new_entry['submission_locked']=0
    feedback_entries = S.get(old_entry)
    #according to the error this has no entries
    #THE MEMORY POINTS TO THE OLD ONE!
    assert old_entry == new_entry
    
def test_submit_problem_manual5():
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S = SheetObject(path_to_data + roster_name,'submissions')
    user_id = "jschmoe"
    assignment = 1
    problem = 1
    timestamp = 129837
    query = {'netid':user_id, 'assignment':assignment,'problem':problem}
    old_entries = S.get(query)
    old_entry = old_entries[0]
    new_entry = {}
    for key in S.set_of_keys:
        new_entry[key] = old_entry[key]
    new_submission_number = get_submission_count()
    new_entry['netid'] = user_id
    new_entry['assignment'] = assignment
    new_entry['problem'] = problem
    new_entry['submission_number'] = new_submission_number
    new_entry['submission_time'] = timestamp
    new_entry['new_submission']=1
    new_entry['submission_locked']=0
    feedback_entries = S.get(old_entry)
    #according to the error this has no entries
    #THE MEMORY POINTS TO THE OLD ONE!
    assert old_entry == new_entry
    
def test_submit_problem_manual3():
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S = SheetObject(path_to_data + roster_name,'submissions')
    user_id = "jschmoe"
    assignment = 1
    problem = 1
    timestamp = 129837
    query = {'netid':user_id, 'assignment':assignment,'problem':problem}
    old_entries = S.get(query)
    old_entry = old_entries[0]
    feedback_entries = S.get(old_entry)
    #according to the error this has no entries
    assert feedback_entries == old_entries
    
def test_submit_problem_manual2():
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S = SheetObject(path_to_data + roster_name,'submissions')
    user_id = "jschmoe"
    assignment = 1
    problem = 1
    timestamp = 129837
    entries = S.get({'netid':user_id, 'assignment':assignment,'problem':problem})
    entry = entries[0]
    feedbacks = S.get(entry)
    feedback=feedbacks[0]
    #according to the error this has no entries
    assert feedback == entry
    
    #message,write_file = submit_problem(user_id,assignment,problem,timestamp)
    #print(message)

def test_feedback():
    """
    I'm going to make a query and then feed it back to the get function.
    """

    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S=SheetObject(path_to_data + roster_name, "submissions")
    
    submission_number = 3
    entries = S.get({'submission_number':submission_number})
    entry = entries[0]
    feedbacks = S.get(entry)
    feedback=feedbacks[0]
    assert entry == feedback

def test_submit_problem():
    """
    TESTING submit_problem: 
    We have a valid submission for jschmoe (assignment 1, problem 1).
    In replace(old_entry,new_entry) it is not recognizing old_entry as an entry. \n
    -test_get shows that we have the correct length output for our query \n
    -test_feedback shows that you can feed the results into a search and get the same thing. \n
    """
    user_id = "jschmoe"
    assignment = 1
    problem = 1
    timestamp = 129837
    message,write_file = submit_problem(user_id,assignment,problem,timestamp)
    #print(message)
    assert write_file==1
    
def test_is_valid_review1():
    submission_number = 3
    user_id = "tdupuy"
    score = 5
    review = "They did ok."
    timestamp = 300000
    message,j = is_valid_review(user_id,submission_number,score,review,timestamp)
    print(message)
    assert j==1
    
def test_is_valid_entry():
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S=SheetObject(path_to_data + roster_name, "submissions")
    old_query = {"submission_number":3}
    myentry = S.get(old_query)[0]
    #print(myentry)
    
    submission_number = 3
    user_id = "tdupuy"
    score = 5
    review = "They did ok."
    timestamp = 300000
    newentry = myentry
    newentry['reviewer1_score'] = score
    newentry['review1'] = review
    newentry['review1_timestamp']=timestamp
    
    setofnewkeys = set(list(newentry.keys()))
    setofoldkeys = S.set_of_keys
    print(setofnewkeys.difference(setofoldkeys))
    
    #MOTHER FUCKING FOUND IT:
    #print(len(set(list(newentry.keys()))))
    #print(len(S.set_of_keys))
    
    assert S.is_valid_entry(newentry)
    

    
def test_write_review2():
    submission_number = 3
    user_id = "tdupuy"
    score = 5
    review = "They did ok."
    timestamp = 300000
    message= write_review(user_id,submission_number,score,review,timestamp)
    print(message)
    
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S=SheetObject(path_to_data + roster_name, "submissions")
    
    entry = S.get({'submission_number':submission_number})[0]
    assert (entry['review1'] == review) and (entry['new_review1']==1)

def test_valid_review3():
    """
    The issue here was that I was using 'user_id' instead of 'netid' in my query.
    """
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S=SheetObject(path_to_data + roster_name, "submissions")
    user_id = "jschmoe"
    assignment = 1
    problem = 1
    timestamp = 129837
    query = {'netid':user_id, 'assignment':assignment,'problem':problem}
    answers=S.get(query)
    assert len(answers)==1


