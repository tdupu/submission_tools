"""
PRINT STATEMENTS
"""
import time
import datetime

def date(unixtime, format = '%m/%d/%Y %H:%M'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)
    
def review_assignment_time(sub):
    if len(sub['reviewer1'])>0:
        return date(sub['reviewer1_assignment_time'])
    else:
        return "NA"
    

def print_submission_header(sub):
    #if sub['new_submission']==1:
    message="    %s: assignment %s, problem %s, submit_time=%s, sent_for_review_time=%s \n" % (sub['submission_number'], sub['assignment'], sub['problem'], date(sub['submission_time']), review_assignment_time(sub))
    #else:
    #    message="    %s: assignment %s, problem %s , timestamp %s \n" % (sub['submission_number'], sub['assignment'], sub['problem'], date(sub['submission_time']))
    return message

def print_review(sub,j):
    """
    sub is a dictionary
    j is the reviewer index.
    """
    if [1,2].count(j)==0:
        return ""
    else:
        message = """
                score: %s
                comments: %s
                
        """ % (sub['reviewer%s_score' %j],sub['review%s' %j])
    return message
        
def print_final_score(sub):
    message = """
        raw score: %s
        adjusted score: %s
    """ % sub['total_score1','total_score2']
            
def print_full_problem_report(sub):
    message = print_submission_header(sub) + "\n"
    message =+ "    reviewer 1 \n"
    message += print_review(sub,1) + "\n"
    message =+ "    reviewer 2 \n"
    message += print_review(sub,2) + "\n"
    return message
    
def print_filenames(sub,user,path_to_uploads):
    """
    returns the dict with 'datafile' and 'uploadfile' entries.
    datafile = name of relevant pdf in path_to_data/uploads/
    uploadfile = name of file that will be sent to the user in the email.
    """
    ending1 = '-' + str(sub['submission_number']) + '-' + str(sub['assignment']) + '-'+str(sub['problem']) + '.pdf'
    ending2 = '-' + str(sub['assignment']) + '-'+str(sub['problem']) + '.pdf'
    datafile = path_to_uploads + sub['netid'] + ending2
    uploadfile = 'ForReview'+ ending1
    return {'datafile':datafile, 'uploadfile':uploadfile}
