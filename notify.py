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
PRINT STATEMENTS
"""

def print_submission_header(sub):
    if sub['new_submission'==1]:
        message="    %s (new): assignment %s, problem %s \n" % (sub['submission_number'], sub['assignment'], sub['problem'])
    else:
        message="    %s: assignment %s, problem %s \n" % (sub['submission_number'], sub['assignment'], sub['problem'])
    return message

def print_review(sub,j):
    """
    sub is a dictionary
    j is the reviewer index.
    """
    if [1,2].count(j)=0:
        return ""
    else:
        message = """
                score: %s
                comments: %s
                
        """ % (sub['reviewer%s_score' %j],sub('review%s' %j))
    return message
        
def print_final_score(sub):
    message = """
        raw score: %s
        adjusted score: %s
    """ % sub['total_score1','total_score2']
            
def print_full_problem_report(sub):
    message = print_header(sub) + "\n"
    message =+ "    reviewer 1 \n"
    message += print_review(sub,1) + "\n"
    message =+ "    reviewer 2 \n"
    message += print_review(sub,2) + "\n"
    return message
    
def print_filenames(sub,user):
    """
    returns the dict with 'datafile' and 'uploadfile' entries.
    datafile = name of relevant pdf in path_to_data/uploads/
    uploadfile = name of file that will be sent to the user in the email.
    """
    ending = '-' + sub['submission_number'] + '-' + sub['assignment'] + sub['problem'] + '.pdf'
    datafile = sub['user'] + ending
    uploadfile = 'ForReview'+ending
    return {'datafile':datafile, 'uploadfile':uploadfile}
    
"""
Main script.
"""


sys.path.append('/Users/taylordupuy/Documents/web-development/dev/excel_tools')
my_system_path ='/Users/taylordupuy/Documents/web-development/dev/submission_tools/'
path_to_variables_j = my_system_path + 'variables.json'
path_to_constants_j = my_system_path + 'constants.json'
path_to_testing_j = my_system_path + 'testing.json'
path_to_data = get_path_to_data()
rostername = "roster-test.xlsx"
course_name = "Math 251"

#turn off the server
webmode(0)



R = SheetObject(path_to_data + roster_name, "roster")
users = R.get({})
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
mydate_s = '-'.join([str(date.month),str(date.day),str(date.year)])

for user in users:
    emails[user] = {}
    emails[user]['subject'] = course_name + " Database Updates" + ("%s" % datetime.datetime.now())
    emails[user]['message_parts'] = {}
    emails[user]['attachments'] = []

    emails[user]['header'] = """
    ################
    %s SERVER UPDATE FOR %s
    ################ \n \n
    """ % (mydate_s,user)
    
    #we may need to replace message_parts with emails['user']['message_parts'] if we get a bug
    message_parts = emails['user']['message_parts']
    message_parts['open_submissions']= "YOUR OPEN SUBMISSIONS: \n " %user
    message_parts['new_closed_submissions'] = "NEW CLOSED SUBMISSIONS: \n"
    message_parts['new_reviews'] = "REVIEWS YOU SUBMITTED: \n" % user
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
               message_parts['open_submissions'] += print_header(sub)
               num_open+=1
               
            else if sub['new_completion']==1:
               #add to new closed submissions
               message_parts['new_closed_submissions'] += print_full_problem_report(sub)
               num_closed+=1
                
        else:
           j = get_reviewer_index(user):
                if j!=0:
                    if sub['new_match']==1:
                        num_requests+=1
                        message_parts['new_referee_requests'] += print_header(sub)
                        new_requests +=1
                        
                    else if sub['new_review%s' % j]==1:
                        message_parts['new_reviews']+= print_header(sub)
                        message_parts['new_reviews']+= print_review(sub,j)
                        new_revs+=1
                        
        
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
json_filename =
with open(path_to_data + 'emails-' + mydate_s +'.json', 'w') as outfile:
    json.dump(emails,outfile)

#turn webpage back on
webmode(1)
