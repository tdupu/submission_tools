"""
Different things happen depending on if you run python3 or python on this file.
"""


import json
import sys
sys.path.append('..')
from submission_functions import *

"""
note to devs:
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

#print(data)

message,authenticated = authenticate(user_id,pass1,pass2,newpass)
output_message = output_message + message

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
    
    #dictionary we are throwing back to PHP
    data3 = {}
    
    for i in range(1,6):
        query = {}
        submission_number = get_submission_count()
        
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
        
        elif is_valid_assignment(assignment,problem,timestamp):
            query['user_id'] = user_id
            query['assignment'] = assignment
            query['problem'] = problem
            message,dataEntry = submit_problem(user_id,assignment,problem,timestamp)
        
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
    with open(path_to_data + 'temp3.json', 'w') as outfile:
        json.dump(data3,outfile)
        
    
    """
    PROCESS REVIEWS
    """
    
    review_message = """
    <br>
    REVIEWS:
    <br>
    """
    output_message = output_message + review_message
    
    for i in range(1,11):
        user_id = data['user_id']
        timestamp = data['timestamp']
        submission_number = data['subnumber%s' % i] #of the review
        review = data['review%s' % i]
        score = data['score%s' % i]
        
        message = write_review(user_id,submission_number,review,score,timestamp)
        
        output_message = output_message + message

print(output_message)




