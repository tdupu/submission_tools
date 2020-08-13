import json
import sys
import time
from matchmaker_functions import *
from submission_functions import *

#sys.path.append('../excel_tools')
#to get these paths I used the pwd unix command.

sys.path.append('/Users/taylordupuy/Documents/web-development/dev/excel_tools')
my_system_path ='/Users/taylordupuy/Documents/web-development/dev/submission_tools/'
path_to_variables_j = my_system_path + 'variables.json'
path_to_constants_j = my_system_path + 'constants.json'
path_to_testing_j = my_system_path + 'testing.json'

from table_editor import SheetObject

path_to_data = get_path_to_data()
rostername = "roster-test.xlsx"
#turn off the server


S = SheetObject(path_to_data + rostername, "submissions")

new_matches = S.key({"new_match":1})
new_completions = S.key({"new_submission":1})

