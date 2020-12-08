import sys
import numpy as np
import datetime

#INSTALL_PATH = '/users/t/d/tdupuy/dev/submission_tools/'
INSTALL_PATH ='/Users/taylordupuy/Documents/web-development/dev/submission_tools/'
sys.path.append(INSTALL_PATH+"../excel_tools")

from table_editor import SheetObject
from table_functions import *
from matchmaker_functions import *
from submission_functions import *


def get_date(unixtime):
    return datetime.fromtimestamp(unixtime)

def time_difference(timestamp2,timestamp1):
    """
    t1 = timestamps[1]
    t2 = timestamps[2]
    time_difference(t2,t1)
    """
    t1 = datetime.datetime.fromtimestamp(timestamp1)
    t2 = datetime.datetime.fromtimestamp(timestamp2)
    delta = t2-t1
    return delta.days

def clean_dec(x):
    return format(x,'.3f')

def searchd(list_of_dicts,sdict):
    new_list = []
    keys=sdict.keys()
    for x in list_of_dicts:
        ok = 1
        for key in keys:
            if x[key]!=sdict[key]:
                ok=0
                break
        
        if ok==1:
            new_list.append(x)
    return new_list

def update(S,mylist):
    message = ""
    for m in mylist:
        snum=m['submission_number']
        mold=S.get({'submission_number':m['submission_number']})
        S.remove(mold)
        S.append(m)
        message = message + f" {snum}"
    return "updated:" + message + "\n unsaved changes will be lost"


def save_hist(subs,key,S,filename,plot_title=""):
    n=len(subs)
    data=[x[key] for x in subs]
    plt.hist(data,bins=7)
    plt.title(plot_title)
    plt.savefig(filename)
    plt.clf()

def score1_hist(p0,scored1):
    """
    TODO: Add the n=X feature
    """
    ass=p0["assignment"]
    pro=p0["problem"]
    n=len(scored1)
    plt.hist(scored1, bins=7)  # arguments are passed to np.histogram
    plt.title(f"score1: assignment {ass}, problem {pro} (n={n})")
    plt.savefig(f"score1-{ass}-{pro}")
    
    """
    savefig(fname, dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    """
    
def score2_hist(p0,scored2,filepath="./"):
    ass=p0["assignment"]
    pro=p0["problem"]
    n=len(scored2)
    plt.hist(scored2, bins=7)  # arguments are passed to np.histogram
    plt.title(f"score2: assignment {ass}, problem {pro} (n={n})")
    filename=f"score2-{ass}-{pro}"
    plt.savefig(filepath+f"score2-{ass}-{pro}")
    return filename + ".png"


"""
tmatch
treview1
treview2
"""
def get_times(subs):
    """
    submissions need to be complete
    """
    matching_times=[]
    review_times=[]
    for m in subs:
        t0 = m['submission_time']
        t1 = m['reviewer1_assignment_time']
        t2 = m['reviewer2_assignment_time']
        t11 = m['review1_timestamp']
        t22 = m['review2_timestamp']
        tmatch = time_difference(max(t1,t2),t0)
        treview1 = time_difference(t11,t1)
        treview2 = time_difference(t22,t2)
        matching_times.append(tmatch)
        review_times.append(treview1)
        review_times.append(treview2)
    return {"review_times":review_times,"matching_times":matching_times}

#
# NEEDS INPUT HANDLING.
#

PATH_TO_DATA = '/Users/taylordupuy/Documents/web-development/data/algebra-one/20/f/'

roster_name = get_roster_name(PATH_TO_DATA)
course_name = get_course_name(PATH_TO_DATA)

today = datetime.date.today()
todays = today.strftime("%B %d, %Y")

path_to_sheet = PATH_TO_DATA + "roster.xlsx"
S = SheetObject(path_to_sheet,"submissions")
P = SheetObject(path_to_sheet,"assignments")
U = SheetObject(path_to_sheet,"roster")

exercises = P.get({})[1:]
users = U.get({})
submissions = S.get({})

matched = S.get({"submission_locked":1,"closed":0})

with open(PATH_TO_DATA+'late_reviews.json','r') as f:
    late_reviews = json.load(f)


cleaned=[]

for s0 in matched:
    tnow=time.time()
    tmatch=s0['reviewer1_assignment_time']
    trev1=s0['review1_timestamp']
    trev2=s0['review2_timestamp']
    reviewer1 = s0['reviewer1']
    reviewer2 = s0['reviewer2']
    sub_num=s0['submission_number']
    
    if time_difference(tnow,tmatch)>7:
        snew =copyd(s0)
        snew['review1_locked']=1
        snew['review2_locked']=1
    
        if trev1==-1 and trev2==-1:
            snew['review1']='DOUBLE LATE REVIEW; FREEBIE.'
            snew['review2']='DOUBLE LATE REVIEW; FREEBIE.'
            snew['review1_timestamp']=tnow
            snew['review2_timestamp']=tnow
            snew['total_score1']=10
            snew['total_score2']=10
            snew['w1']=1
            snew['w2']=1
            snew['closed']=1
            late_reviews[reviewer1].append(sub_num)
            late_reviews[reviewer2].append(sub_num)
        
        elif trev1==-1:
            #the first review is late and we are going to lock the review
            snew['review1']='LATE REVIEW; WEIGHTED ZERO.'
            snew['reviewer1_score']=0
            snew['w1'] = 0
            snew['w2'] = 1
            snew['total_score1']=s0['reviewer2_score']
            snew['total_score2']=s0['reviewer2_score']
            snew['review1_timestamp']=tnow
            late_reviews[reviewer1].append(sub_num)
            snew['closed']=1
            
        elif trev2==-1:
            #the second review is late and we lock the review.
            snew['review2']='LATE REVIEW; WEIGHTED ZERO.'
            snew['reviewer2_score']=0
            snew['w1'] = 1
            snew['w2'] = 0
            snew['total_score1']= m['reviewer1_score']
            snew['total_score2']=m['reviewer1_score']
            snew['review2_timestamp']=tnow
            snew['closed']=1
            late_reviews[reviewer2].append(sub_num)
            
        if time_difference(tnow,trev1)>2:
            snew['new_review1']=0
        
        if time_difference(tnow,trev2)>2:
            snew['new_review2']=0
            
        cleaned.append(snew)

        f=open(PATH_TO_DATA+'late_reviews.json','w')
        json.dump(late_reviews,f)
        f.close()
        
update(S,cleaned)
S.save()

#############
#Now we update the participation scores
#############

matched=S.get({'submission_locked':1})
for m in matched:
    matched_dict[m['netid']].append(m['submission_number'])
    
for user in users:
    usernew=copyd(user)
    total=14 + 2*len(matched_dict[user['netid']])
    num=total-len(late_reviews[user['netid']])
    usernew['participation']=num/total
    U.remove([user])
    U.append(usernew)
    U.save()
