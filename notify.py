import json
import sys
import time
import datetime

sys.path.append('/Users/taylordupuy/Documents/web-development/dev/excel_tools')
my_system_path ='/Users/taylordupuy/Documents/web-development/dev/submission_tools/'

from table_editor import SheetObject
from table_functions import *
from matchmaker_functions import *
from submission_functions import * #for shutting down server, setting values.
from notify_functions import *

#sys.path.append('../excel_tools')
#to get these paths I used the pwd unix command.

"""
We decided to have three types of emails.

Updates:
these give any modification to the server in a batch email.

Homework Results:
these are transmitted at review deadlines.

Grade Summary:
there are transmitted periodically.

The present file gives a nightly update on progress.
"""


    
"""
Main script.
"""


sys.path.append('/Users/taylordupuy/Documents/web-development/dev/excel_tools')
my_system_path ='/Users/taylordupuy/Documents/web-development/dev/submission_tools/'
path_to_variables_j = my_system_path + 'variables.json'
path_to_constants_j = my_system_path + 'constants.json'
path_to_testing_j = my_system_path + 'testing.json'
path_to_data = get_path_to_data()
roster_name = "roster-test.xlsx"
course_name = "Math 251"

#turn off the server
webmode(0)

R = SheetObject(path_to_data + roster_name, "roster")
students = R.get({})
users = [student["netid"] for student in students]


S = SheetObject(path_to_data + roster_name, "submissions")
updated_subs = kill_repeats(S.get({"new_submission":1})+S.get({"new_match":1})+S.get({"new_review1":1})+S.get({"new_review2":1}))

emails = {}

"""
For every user we are going to generate data to create an email stored as emails[user].
The email consists of four sections
1) All your open submissions and their status (receipt of new submissions)
2) All your submissions that were recently closed, and the response
3) All the referee reports you submitted (a receipt)
4) All the new referee requests

"""


mydate = datetime.datetime.now()
mydate_s = '-'.join([str(mydate.month),str(mydate.day),str(mydate.year)])

for user in users:
    emails[user] = {}
    emails[user]['subject'] = course_name + " Database Updates" + ("%s" % datetime.datetime.now())
    emails[user]['message_parts'] = {}
    emails[user]['attachments'] = []

    
    #we may need to replace message_parts with emails['user']['message_parts'] if we get a bug
    #I'm taking advantage of the way dictionaries point in python here.
    message_parts = emails[user]['message_parts']
    message_parts['header'] = """
    ################
    %s SERVER UPDATE FOR %s
    ################ \n \n
    """ % (mydate_s,user)
    message_parts['open_submissions']= "YOUR OPEN SUBMISSIONS: \n "
    message_parts['new_closed_submissions'] = "NEW CLOSED SUBMISSIONS: \n"
    message_parts['new_reviews'] = "REVIEWS YOU SUBMITTED: \n" #% user
    message_parts['new_referee_requests'] = "NEW REFEREE REQUESTS (see attachments for files): \n"
    message_parts['complete_message'] = """
    
    
    """
    num_open = 0
    num_closed = 0
    num_revs = 0
    num_requests = 0

    for sub in updated_subs:
        if sub['netid']==user:
            
            if sub['new_completion']==0:
               #add to open submission (this should be improved)
               message_parts['open_submissions'] += print_submission_header(sub)
               num_open+=1
               
            elif sub['new_completion']==1:
               #add to new closed submissions
               message_parts['new_closed_submissions'] += print_full_problem_report(sub)
               num_closed+=1
                
        else:
            j = get_reviewer_index(user,sub)
            
            if j!=0:
            
                if sub['new_match']==1:
                    num_requests+=1
                    message_parts['new_referee_requests'] += print_submission_header(sub)
                    num_requests +=1
                        
                elif sub['new_review%s' % j]==1:
                    message_parts['new_reviews']+= print_header(sub)
                    message_parts['new_reviews']+= print_review(sub,j)
                    num_revs+=1
                        
        
    #builds the message

    message = message_parts['header']
    
    if num_open>0:
        message+=message_parts['open_submissions']
    
    if num_closed>0:
        message+=message_parts['new_closed_submissions']
    
    if num_revs>0:
        message+=message_parts['new_reviews']
    
    if num_requests>0:
        message+=message_parts['new_referee_requests']
        
    message_parts['complete_message']=message
    
#temp3.json will be read by the upload.php
#used to determine if one should attempt to upload the PDFs
#json_filename =
with open(path_to_data + 'emails-' + mydate_s +'.json', 'w') as outfile:
    json.dump(emails,outfile)

#turn webpage back on
webmode(1)
