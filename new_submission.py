
"""
Usage:

Testing mode off
    python3 new_submission.py PATH_TO_DATA 0
Testing mode on
    python3 new_submission.py PATH_TO_DATA 1
Default Algebra file
    python3 new_submission.py


NOTES:
--Different things happen depending on if you run python3 or python on this file.
--Always use absolute paths.
--Information about the particular course is stored in constants.json which you can load as a python dictionary. It should path_to_data, roster_name, course_name information. Git does not track this file.
"""

import json
import sys
from submission_functions import *

"""
HANDLE OPTIONS
"""

if len(sys.argv)>1:
    PATH_TO_DATA = sys.argv[1]
else:
    PATH_TO_DATA = '/Users/taylordupuy/Documents/web-development/data/algebra-one/20/f/'
    
if len(sys.argv)>2:
    k = sys.argv[2]
    tmode(k,PATH_TO_DATA)
else:
    tmode(1,PATH_TO_DATA)

CONSTANTS = get_constant_data(PATH_TO_DATA)
ROSTER_NAME = CONSTANTS['roster_name']
COURSE_NAME = CONSTANTS['course_name']
PATH_TO_UPLOADS = PATH_TO_DATA + '/uploads/'

from submission_functions import *

"""
START PROCESSING DATA
"""

#THIS FILE IS WHERE THE INFORMATION FROM upload.php IS SENT.
f = open(PATH_TO_DATA+"temp.json",'r')
data=json.loads(f.read())
f.close()


"""
AUTHENTICATE USER
"""

#AUTHENTICATION DATA
user_id = data['user_id']
pass1 = data['password']
pass2 = data['password2']
newpass = data['new_password']

output_message = ""

#print(data)

message,authenticated = authenticate(user_id,pass1,pass2,newpass,PATH_TO_DATA)
output_message = output_message + message

#for processing if the file should even be considered for upload
f2 = open(PATH_TO_DATA+"temp2.json",'r')
data2=json.load(f2)
f2.close()

if authenticated==1:
    """
    PROCESS SUBMISSIONS
    """
    
    submission_message = """
    <h4> submissions </h4>
    """
    output_message = output_message + submission_message
    
    #dictionary we are throwing back to PHP
    data3 = {}
    
    for i in range(1,6):
        query = {}
        submission_number = get_submission_count(PATH_TO_DATA)
        
        """
        There was some massive crude-ass debugging that went on here.
        I'm a terrible person.
        As it turns out, the empty string is not an integer and this is what happens when the variables are not set.
        """
        
        
        #print(" <br> <br> submission number (top of loop): %s <br>" % submission_number)
        
        #print(" dumping data (looking for assignment and problem values): <br>")
        #for key in data.keys():
        #    print( "%s <br>" % data[key] )
        #print(data)
        #print('<br>')
        
        #xx=int(mydata) #this throws an error.
        """
        if isinstance(mydata,str):
            print("its a string! <br>")
        print( "is digit: %s <br>" % mydata.isdigit())
        print( "first character: %s <br>" % mydata[0] ) #this throws an error
        print( "what it looks like after concat:" + mydata + "<br>")
        try:
            xx=int(mydata)
            print("its an integer now! <br>")
        except:
            print("it throws an error when I do int(mydata) <br>")
        """
        """
        try:
            xx=int(assignment)
            yy=int(problem)
            zz=int(timestamp)
            print("they are all integers now! <br>")
        except:
            print("now I get an error")
        """
        assignment = data['assignment%s' % i]
        problem = data['problem%s' % i]
        timestamp = int(data['timestamp'])
        
        #The empty string does not convert to an integer
        try:
            assignment = int(assignment) #PHP exports ints as strings for some reason.
            problem = int(problem)
        except:
            pass
            #do nothing
        
        """
        print('assignment %s,problem %s, timestamp:%s' % (assignment,problem,timestamp))
        print('<br>')
        print('data2 (file information): <br>')
        print(data2)
        """
        
        dataEntry={}
        
        #reminder: data2 contains testing if a file has an empty string or not.
        if data2[str(i)]==0:
            message = ""
            #message = """
            #*assignment %s, problem %s rejected. not a valid PDF. <br>
            #\n
            #""" % (assignment,problem)
            #print("submission_number %s <br>" % submission_number )
            dataEntry = {"uploadOk":0,"submission_number":submission_number}
            
            #The next step checks to see if this is a made up problem.
        
        elif is_valid_assignment(assignment,problem,timestamp,PATH_TO_DATA):
            query['user_id'] = user_id
            query['assignment'] = assignment
            query['problem'] = problem
            message,dataEntry = submit_problem(user_id,assignment,problem,timestamp,PATH_TO_DATA)
        
        else:
            message = """
            *assignment %s, problem %s rejection. not an assigned problem or is past due date. <br>
            \n
            """ % (assignment,problem)
            dataEntry = {"uploadOk":0,"submission_number":submission_number}
        
        data3[i] = dataEntry
        output_message = output_message + message
        
    #temp3.json will be read by the upload.php
    #used to determine if one should attempt to upload the PDFs
    with open(PATH_TO_DATA + 'temp3.json', 'w') as outfile:
        json.dump(data3,outfile)
        
    
    """
    PROCESS REVIEWS
    """
    
    review_message = """
    <h4> reviews </h4>
    """
    output_message = output_message + review_message
    
    for i in range(1,11):
        
        user_id = data['user_id']
        timestamp = data['timestamp']
        sub_number = data['subnumber%s' % i] #of the review
        score = data['score%s' % i]
        review = data['review%s' % i]
        
        try:
            timestamp = int(data['timestamp'])
            sub_number = int(data['subnumber%s' % i]) #of the review
            score = int(data['score%s' % i])
        except:
            pass
        
        
        message = write_review(user_id,sub_number,score,review,timestamp,PATH_TO_DATA)
        
        output_message = output_message + message

output_message = output_message + """
<br> <i>
Resubmission will overwrite the current entry.
Submissions are locked after two reviewers have been notified.
Reviews are locked after a deadline or once two reviews have been recorded.
Processing occurs at midnight every night.
</i>
<br>
"""

print(output_message)




