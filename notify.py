import json
import sys
import os
import time
import datetime


INSTALL_PATH = "/users/t/d/tdupuy/dev/submission_tools/"
#INSTALL_PATH ='/Users/taylordupuy/Documents/web-development/dev/submission_tools/'
sys.path.append("/users/t/d/tdupuy/dev/excel_tools")
sys.path.append("/users/t/d/tdupuy/dev/email_tools")

from table_editor import SheetObject
from table_functions import *
from matchmaker_functions import *
from submission_functions import * #for shutting down server, setting values.
from notify_functions import *
from email_functions import *

"""
MORE INFORMATION ON HANDLING OPTIONS
https://www.tutorialspoint.com/python/python_command_line_arguments.htm

You call this scripts as follows:
    python3 notify.py /path/to/data/ 0 1
If you just run
    python3 notify.py
It will assume the path like my local folder and that we are testing.
Testing to be 1 and non-testing to be 0.
The second flag will be emails and no-emails.
To send the emails set it to 0.
Email sending is by default off.
"""


    
"""
We decided to have three types of emails.

Server Updates:
these give any modification to the server in a batch email.

Homework Results:
these are transmitted at review deadlines.

Grade Summary:
there are transmitted periodically.

The present file gives a nightly update on progress.
"""

#filename = "emails-%s.json" % mydate_s
#path_to_variables_j = INSTALL_PATH + 'variables.json'
#path_to_constants_j = INSTALL_PATH + 'constants.json'
#path_to_testing_j = INSTALL_PATH + 'testing.json'
#f = open(PATH_TO_DATA+'constants.json','r')
#CONSTANTS=json.loads(f.read())
#f.close()

"""
PARSE INPUTS:
"""
if len(sys.argv)==1:
    tmode(1)
    PATH_TO_DATA = get_path_to_data()
    DONT_SEND_EMAILS=1

elif len(sys.argv)==2:
    PATH_TO_DATA = sys.argv[1]
    tmode(1,PATH_TO_DATA)
    DONT_SEND_EMAILS=1

elif len(sys.argv)==3:
    PATH_TO_DATA = sys.argv[1]
    IS_TEST = sys.argv[2]
    DONT_SEND_EMAIL=1
    tmode(IS_TEST,PATH_TO_DATA)

elif len(sys.argv)==4:
    PATH_TO_DATA = sys.argv[1]
    IS_TEST = sys.argv[2]
    DONT_SEND_EMAILS=int(sys.argv[3])
    tmode(IS_TEST,PATH_TO_DATA)
    
else:
    tmode(1)
    DONT_SEND_EMAILS=1

roster_name = get_roster_name(PATH_TO_DATA)
course_name = get_course_name(PATH_TO_DATA)

print("running notify.py... ")
print("test mode: %s " % get_test_mode(PATH_TO_DATA))
print("don't send emails: %s " % DONT_SEND_EMAILS)
print("path to data: %s " % PATH_TO_DATA)
print("roster name: %s " % roster_name)
print("course name: %s " % course_name)


PATH_TO_UPLOADS = PATH_TO_DATA + '/uploads/'


#turn off the server
server_down =1
out_msg=webmode(server_down,PATH_TO_DATA)
print(out_msg)

R = SheetObject(PATH_TO_DATA + roster_name, "roster")
students = R.get({})
users = [student["netid"] for student in students]


S = SheetObject(PATH_TO_DATA + roster_name, "submissions")
new_matches = S.get({"new_match":1})
new_completions = S.get({"new_completion":1})

for sub in new_completions:
    score1(sub,S)
    score2(sub,S)

updated_subs = kill_repeats(S.get({"new_submission":1})+S.get({"new_completion":1})+S.get({"new_review1":1})+S.get({"new_review2":1}))


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
    emails[user]['subject'] = course_name + " Database Updates " + ("%s" % datetime.datetime.now())
    #emails[user]['message_parts'] = {}
    emails[user]['message'] =''
    emails[user]['attachments'] = []
    emails[user]['receiver'] = R.get({'netid':user})[0]['email']

    
    #we may need to replace message_parts with emails['user']['message_parts'] if we get a bug
    #I'm taking advantage of the way dictionaries point in python here.
    #message_parts = emails[user]['message_parts']
    message_parts = {}
    message_parts['header'] = """
    Dear %s,
    
    Below you will find updates on the server pertaining to the coursework in the class.
    These include
       A) receipts for new open submissions,
       B) newly closed submissions (grades),
       C) receipts for reviews you have submitted,
       D) new referee requests.
    Reviews are due approximately one week from this email.
    
    If any of the items (A)-(D) don't appear, that is because there are no updates on the server.
    
    TIPS ON REVIEWS:
    Don't make too much work for yourself (it is a pandemic after all). They should be super quick after you get used to doing them. Reviews can be a sentence or two. If you are feeling generous you can explain to the submitter what they missed. The most important part is that your comments have pinpoint accuracy. This includes finding missing implications and logical gaps (e.g. "the writer forgot to prove the converse" or "the base case of the induction proof is missing"), pointing to errors by their line numbers/sentence/part ("the equality displayed below the second sentence is incorrect" -- give counter-examples when you can!), pointing to specific errors like missing definitions undefined symbols etc. ("The symbol 'A' in the first sentence of the second paragraph is not defined."). When a submission is good, make your life easy. Writing a single word like "perfect" suffices.
    
    Best,
    Taylor's Automated Emailer
    
    
    
    ##############################
    %s SERVER UPDATES FOR %s
    ##############################
    """ % (user, mydate_s,user)
    message_parts['open_submissions']= "YOUR OPEN SUBMISSIONS: \n  "
    message_parts['new_closed_submissions'] = "NEW CLOSED SUBMISSIONS: \n "
    message_parts['new_reviews'] = "REVIEWS YOU SUBMITTED: \n " #% user
    message_parts['new_referee_requests'] = "NEW REFEREE REQUESTS (see attachments for files): \n"
    message_parts['complete_message'] = """
    
    
    """
    num_open = 0
    num_closed = 0
    num_revs = 0
    num_requests = 0

    for sub in updated_subs:
        if sub['netid']==user:
            
            if int(sub['new_completion'])==0:
               #add to open submission (this should be improved)
               message_parts['open_submissions'] += print_submission_header(sub)
               num_open+=1
               
            elif int(sub['new_completion'])==1:
               #add to new closed submissions
               message_parts['new_closed_submissions'] += print_full_problem_report(sub)
               num_closed+=1
               
        else:
            j = get_reviewer_index(user,sub,S)
            
            if j!=0:
            
                if int(sub['new_match'])==1:
                    num_requests+=1
                    message_parts['new_referee_requests'] += print_submission_header(sub)
                    num_requests +=1
                    owner = sub['netid']
                    emails[user]['attachments'].append(print_filenames(sub,owner,PATH_TO_DATA + "uploads/"))
                        
                elif int(sub['new_review%s' % j])==1:
                    message_parts['new_reviews']+= print_submission_header(sub)
                    message_parts['new_reviews']+= print_review(sub,j)
                    num_revs+=1

                        
        
    #BUILD MESSAGE
    message = message_parts['header']
    
    if num_open>0:
        message+=message_parts['open_submissions']
    
    if num_closed>0:
        message+=message_parts['new_closed_submissions']
    
    if num_revs>0:
        message+=message_parts['new_reviews']
    
    if num_requests>0:
        message+=message_parts['new_referee_requests']
    
    if num_open+num_closed+num_revs+num_requests>0:
        emails[user]['message'] = message

"""
EMAILS
"""
path_to_emails = PATH_TO_DATA + 'emails-' + mydate_s +'.json'
print("dumping emails: " + path_to_emails + "\n")
with open(path_to_emails,'w') as outfile:
    json.dump(emails,outfile)

print("DONT_SEND_EMAILS:%s \n" % DONT_SEND_EMAILS)
if DONT_SEND_EMAILS==0:
    print("sending emails: \n")
    for k in emails.keys():
        mymessage = emails[k]['message']
        if len(mymessage)>0:
            out_msg=send_email(emails[k])
            print(out_msg)
            print(emails[k]['message'])
    
"""
CLEAN EVERYTHING UP.

KEYS:
submission_number
submission_locked
netid
assignment
problem
closed
submission_time
total_score1
total_score2
reviewer1_assignment_time
reviewer1
reviewer1_score
review1
review1_timestamp
review1_locked
reviewer2_assignment_time
reviewer2
reviewer2_score
review2
review2_timestamp
review2_locked
new_submission
new_match
new_review1
new_review2
new_completion
"""

for sub in new_matches:
    new_entry = copyd(sub)
    new_entry["new_match"]=0
    new_entry["submission_locked"]=1
    #message=unmark_new_match(sub,S)
    #print(message)
    #message=mark_locked(sub,S)
    #print(message)
    S.replace(sub,new_entry)
    S.save()
    print("%s: new_match =0, submission_locked=1 \n" % sub["submission_number"])

for sub in new_completions:
    """
    THIS IS BUGGY.
    """
    mysub = S.get({"submission_number":sub["submission_number"]}) #to preserve scores
    new_entry = copyd(mysub)
    new_entry["new_completion"]=0
    new_entry["new_review1"]=0
    new_entry["new_review2"]=0
    new_entry["review1_locked"]=1
    new_entry["review2_locked"]=1
    S.replace(mysub,new_entry)
    S.save()
    print("%s: new_completion=0, new_review1=0, new_review2=0, review1_locked=1, review2_locked=1 \n" % new_entry["submission_number"])
    #message=unmark_new_completion(sub,S)
    #print(message)
    #message=unmark_newreview(sub,1,S)
    #print(message)
    #message=unmark_newreview(sub,2,S)
    #print(message)
    #message = mark_review_locked(sub,1,S)
    #print(message)
    #message = mark_review_locked(sub,2,S)
    #print(message)
    #message=mark_closed(sub)
    #print(message)
    

"""
TURN WEBPAGE BACK ON
"""
server_down=0
out_msg=webmode(server_down,PATH_TO_DATA)
print(out_msg)
