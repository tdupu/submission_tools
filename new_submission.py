#!/usr/bin/env python

#import json
#import sys

#the following gives an error but it looks like we don't need it.
#sys.path.append('..')
#from excel_tools.table_editor import SheetObject
#from submission_functions import *

#JSON requires double quotes!

"""
Different things happen depending on if you run python3 or python on this file.
"""


import json
import sys
sys.path.append('..')
from submission_functions import *

"""
NOTE TO USERS:
modify constant.json with your information.
"""

path_to_data = get_path_to_data() #rooted from where jupyter was launched

from submission_functions import *

"""
START PROCESSING DATA
"""

temp_filename = "temp.json"
f = open(path_to_data+temp_filename,'r')
data=json.loads(f.read())
f.close()

#startwriting down things
user_id = data['user_id']
pass1 = data['password']
pass2 = data['password2']
newpass = data['new_password']

output_message = ""

"""
AUTHENTICATE USER
"""

message,authenticated = authenticate(user_id,pass1,pass2,newpass)
output_message = output_message + message
files_to_write = {1:0,2:0,3:0,4:0,5:0,6:0}


#for processing if the file should even be considered for upload
temp_filename2 = "temp2.json"
f2 = open(path_to_data+temp_filename2,'r')
data2=json.load(f2)
f2.close()

if authenticated==1:
    """
    PROCESS SUBMISSIONS
    """
    
    submission_message = """
    <br>
    SUBMISSIONS:
    <br>
    """
    output_message = output_message + submission_message
    
    data3 = {}
    
    for i in range(1,6):
        query = {}
        submission_number = get_submission_count()
        assignment = data['assignment%s' % i]
        problem = data['assignment%s' % i]
        timestamp = data['timestamp']
        
        dataEntry={}
        
        if data2[i] ==0:
            message = """
            The file associated with assignment %s, problem %s is not a valid PDF. <br>
            \n
            """ % (assignment,problem)
            dataEntry = {"uploadOk":0,"submission_number":submission_number}
        
        elif is_valid_assignment(assignment,problem,timestamp):
        #if is_valid_assignment(assignment,problem,timestamp):
            query['user_id'] = user_id
            query['assignment'] = assignment
            query['problem'] = problem
            message,dataEntry = submit_problem(user_id,assignment,problem,timestamp)
        
        else:
            message = """
            assignment %s, problem %s is not a valid problem or is past the due date. <br>
            \n
            """ % (assignment,problem)
            dataEntry = {"uploadOk":0,"submission_number":submission_number}
        
        data3[i] = dataEntry
        output_message = output_message + message
        
    #temp3.json will be read by the upload.php
    #used to determine if one should attempt to upload the PDFs
    with open(path_to_data + 'temp3.json', 'w') as outfile:
        json.dump(data3,outfile)
        
    
    """
    PROCESS REVIEWS
    """
    
    review_message = """
    <br>
    SUBMISSIONS:
    <br>
    """
    output_message = output_message + review_message
    
    for i in range(1,11):
        j=0
        user_id = data['user_id']
        timestamp = data['timestamp']
        submission_number = data['subnumber%s' % i] #of the review
        review = data['review%s' % i]
        score = data['score%s' % i]
        
        message = write_review(user_id,submission_number,review,score,timestamp)
        '''
        message, j = is_valid_review(user_id,submission_number,review,score,timestamp)
        
        old_entry = S.get({'submission_number':submission_number})
        new_entry = old_entry

        if j!=0:
            new_entry['review%s' % j] = review
            new_entry['score%s' % j] = int(score)
            new_entry['review%s_timestamp' % j] = timestamp
            S.replace(old_entry,new_entry)
            S.save()
        '''
        
        output_message = output_message + message

print(output_message)




