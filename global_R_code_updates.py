# MAKE GLOBAL CHANGES TO SCRIPTS & PUSH CHANGES TO GITLAB
# WRITTEN BY: KAYLEE HODGSON

# import relevant packages

import pandas as pd
import numpy as np
import glob
import os
import time
# Repo installed in the command prompt using "conda install gitpython"
from git import Repo

# import entity information

entity_info = pd.read_csv(r'folder/entity_info.csv')
entity_info = pd.DataFrame(entity_info, columns = ['entity_name','folder_name'])

#-------------------------------------------------
#-------------------------------------------------
# MANUALLY INPUT RELEVANT INFORMATION

# What script needs to be augmented?
R_script = "R_script.R"

# old lines that should be replaced
old_lines = ["""old code 1""", """old code 2"""]

# new lines that should replace old lines
new_lines = ["""new code 1""", """new code 2"""]

# git commit message
commit_message = "scripts updated using python global updates code"
#-------------------------------------------------
#-------------------------------------------------

##############################################################################
## CODE UPDATES

# create a file to track update success
tracker = pd.DataFrame(entity_info, columns = ['entity_name'])
tracker["status"] = ""

for i in range(len(entity_info.entity_name)):
 
        try:
            # define file path for the R script
            file = entity_info.folder_name[i] + '\\ ' + entity_info.entity_name[i] + '_' + R_script
            
            # find and replace all specified lines in the R code
            for le in range(len(old_lines)):
                with open(file, 'r') as script:
                    lines = script.readlines()
                with open(file, 'w') as script:
                    for line in lines:
                        line = line.replace(old_lines[le], new_lines[le])
                        script.write(line)  
                        
            # track update success
            tracker.status[i] = "Pass"
            
        except:
            # mark if there's an error & track update failure
            print('Some error occured while augmenting the R code for ' + entity_info.entity_name[i])   
            tracker.status[i] = "Fail"
##############################################################################
    

##############################################################################
## REPLACEMENT QUALITY CHECKS 
     
# create a file and variables to track quality checks for each entity                       
quality_checks = pd.DataFrame(entity_info, columns = ['entity_name'])
quality_checks["size"] = 0
quality_checks["time"] = 0
quality_checks["lines_updated"] = False

for i in range(len(entity_info.entity_name)):
    
    # define file path for R code
    file = entity_info.folder_name[i] + '\\ ' + entity_info.entity_name[i] + '_' + R_script
    
    #### check that the file sizes are greater than 0
    quality_checks.size[i] = os.path.getsize(file)
    
    #### check that the file has been updated
    quality_checks.time[i] = time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(file)))
    
    #### check that each file's lines have been updated correctly
    
    # separate if any of the new lines added multiple lines to the code
    new_lines =  [y for x in new_lines for y in x.split('\n')]      
    # create a list to mark whether each new line is found in the code
    script_lines = [False] * len(new_lines)
    # Iteratively search for each new line in the code, and mark whether each is found
    for le in range(len(new_lines)):
        with open(file, 'r') as script:
            index = 0
            for line in script:
                index += 1
                if new_lines[le] in line:
                    script_lines[le] = True
                    break
    # if all new lines are present, mark in checks file
    if np.all(script_lines):
        quality_checks.lines_updated[i] = True       

# Look through quality_checks
quality_checks[['entity_name','size']]
quality_checks[['entity_name','time']]
quality_checks[['entity_name','lines_updated']]
##############################################################################


##############################################################################
## GIT PUSHES 
                

tracker["git"] = ""                            

for i in range(len(entity_info.entity_name)):
     
    # specify location of git repository      
    path_of_git_repo = entity_info.folder_name[i] + '\\.git'
    def git_push():
        # push code changes to gitlab with the commit message specified above
        # track success of git push
        try:
            repo = Repo(path_of_git_repo)
            repo.git.add(update=True)
            repo.index.commit(commit_message)
            origin = repo.remote(name='origin')
            origin.push()
            tracker.git[i] = "Pass"
        # if the push is unsuccessful, track so we can manually update
        except:
            print('Some error occured while pushing the code for ' + entity_info.entity_name[i])  
            tracker.git[i] = "Fail"
    git_push()
##############################################################################
    
    