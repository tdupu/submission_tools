AUTHOR: TAYLOR DUPUY
DATE: September 2020
DESCRIPTION: Library of functions for pandemic learning. 

Copyright: this library is covered under the GNU Public Licsense. 

*****************
INSTRUCTIONS
*****************
This requires the installation 

ssh-user-root
├── data
│   ├── algebra-one
│   │   └── 20
│   │       └── f
│   │           └── uploads
│   ├── algebraic-topology
│   │   └── 20
│   │       └── f
│   └── email_schedule
├── dev
│   ├── backup
│   ├── email_tools
│   │   └── __pycache__
│   ├── excel_tools
│   │   └── __pycache__
│   └── submission_tools
│       └── __pycache__
└── www-root
    └── algebra-one
        └── 20
            └── f
                └── old

Clone the following repositories on unix. 
    https://github.com/tdupu/submission_tools
    https://github.com/tdupu/excel_tools
    https://github.com/tdupu/email_tools

Set up a cronjob for each of these to pull. I actually, maintain my webpage from a cronjob and pull it off of git. Remember to use which if there is a shell command that you want to run (like a particular version of python or git tailored to the user you have been testing with). The following webpage is incredibly useful for setting up cronjobs: https://crontab.guru

In submission_tools/MOVE_ME/ you will find make.py, roster_test.xlsx, you will need to modify roster_test.xlsx to a roster.xlsx with the same headings and your actual course file. Once you have moved that to your appropriate data file, you need to feed
    PATH_TO_SUBMISSION_TOOLS
    PATH_TO_DATA
    PATH_TO_WEBPAGE
these need to be absolute paths and which you can find by navigating to the appropriate folder and using the bash pwd command. 

The make.py will create CONSTANTS.json which contains file path information used by upload.php, and the submission_tools. 


*****************
OUTLINE OF CODE
*****************



*****************
COMMON BUGS
*****************

*The code is run off of python3 and not python.

*Make sure to have "pip3 install <package>" for the following packages: openpyxl, 

*Make sure there is execute permission on your scripts by running "chmod +x <path to script>". When functions scripts are executed from php,python, or cron they count as a different user and hence have a different collection of permissions in unix.

*Make sure the file paths are ok. When you call python from PHP the file path changes which tends to create a lot of import problems.

*The data types reading in and out of json files/excel files can be different. Friends: the bash commands 'pwd', 'which', the #! header on the python files. 

*PHP and python need the appropriate permissions.


*****************
REFERENCES
*****************
The graph theory library used for the sorting problem is documented here:
    https://pypi.org/project/graph-theory/

Make sure to add permissions to new_submnission.py so that uploads.php can execute it. 
    chmod +x new_submission.py

https://medium.com/flatiron-engineering/recovering-from-a-jupyter-disaster-27401677aeeb

https://stackoverflow.com/questions/1054271/how-to-import-a-python-class-that-is-in-a-directory-above
