
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
    
def test_submit_problem():
    user_id = "jschmoe"
    assignment = 1
    problem = 1
    timestamp = 129837
    message,write_file = submit_problem(user_id,assignment,problem,timestamp)
    print(message)
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
    
def test_is_valid_review2():
    submission_number = 3
    user_id = "tdupuy"
    score = 5
    review = "They did ok."
    timestamp = 300000
    message,j = write_review(user_id,submission_number,score,review,timestamp)
    print(message)
    
    CONSTANT_DATA = get_CONSTANT_DATA()
    path_to_data = CONSTANT_DATA['path_to_data']
    roster_name = CONSTANT_DATA['roster_name']
    S=SheetObject(path_to_data + roster_name, "submissions")
    entry = S.get({'submission_number':submission_number})[0]
    assert (entry['review1'] == review) and (entry['new_review1']==1)


