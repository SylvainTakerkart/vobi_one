# Author: Flavien Garcia <flavien.garcia@free.fr>
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

"""
Description
-----------

This script processes the oidata functions on some selected, by
conditions ,residuals files.
The process is decomposed in 3 steps :
1. Conditions file recovery
2. Apply Durbin-Watson test on each residuals file
3. Visualization of results in an histogram

This script needs to have already apply linear model

Notes
-----
1. Copy the script in a temporary directory of your choice and cd into this directory
2. Change parameters directly in the script itself
3. Write on a shell : brainvisa --noMainWindow --shell.
4. Write : %run script6_durbin_watson_test.py
"""
############################## SECTION TO CHANGE ###############################
DATABASE = '/home/garcia/data/brainvisa_db/' # Database
protocol='protocol_sc' # Protocol name
subject='subject_sc' # Subject name
session_date='080313' # Sesion date
analysis_name='_1' # Analysis name
conditions_list=[6] # Conditions list

################################################################################








########################## DO NOT TOUCH THIS SECTION ###########################
# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path

import os
import numpy as np

import oidata.oisession_postprocesses as oisession_postprocesses # Session-level processing functions

# Parameters validation

# Conditions list
cdt=''
try:
    eval_cdt_list=sorted(eval(str(conditions_list))) # Str to int
    if len(eval_cdt_list)>1 and type(eval_cdt_list[0])!=int:
        raise SyntaxError('Conditions list not properly completed')
except SyntaxError:
    raise SyntaxError('Conditions list is not properly completed')
for c in range(len(eval_cdt_list)): # For each condition
    cdt+='_c'+str(eval_cdt_list[c])
    
print('CONDITIONS FILE RECOVERY')
info_file_list=[] # Path initialization
try: # Verify if a conditions file already exists
    # Conditions file path creation
    path_cond=os.path.join(DATABASE\
                          ,protocol\
                          ,subject\
                          ,'session_'+session_date \
                          ,'oitrials_analysis/conditions.txt')
                          
    # Conditions file path recovery                      
    raw_name,experiences,trials,conditions,selected=np.loadtxt(path_cond\
                                                              ,delimiter='\t'\
                                                              ,unpack=True\
                                                              ,dtype=str)
    
    # Recovery of files informations    
    for name in raw_name: # For each trial
        session=name[1:7] # Session recovery
        exp=name[9:11] # Experiment recovery
        trial=name[13:17] # Trial recovery
        condition=name[19:22] # Conditions recovery
        path=os.path.join(os.path.split(path_cond)[0]\
                         ,'exp'+exp,'trial'+trial,'raw',name) # Path creation
        info_file={'session':session\
                  ,'exp':exp,'trial':trial\
                  ,'condition':condition,'path':path} # Put them on info_file
        info_file_list.append(info_file) # Add info file

except: # If not, data import is needed
    raise ImportError('This script needs to have already apply linear model')

print('CREATION OF DATA GRAPH')
# Data graph creation
info_model_files=oisession_postprocesses.durbin_watson_test_process(
    database=DATABASE, # Database path
    protocol=protocol, # Protocol name
    subject=subject, # Subject name
    session='session_'+session_date , # Session
    analysis='glm_based'+analysis_name, # Analysis type or name
    conditions=conditions_list,
    data_graph=os.path.join(DATABASE,protocol,subject,'session_'+session_date,'oisession_analysis/glm_based'+analysis_name,'durbin_watson_test'+cdt+'.png'),
)

print('VISUALIZATION OF DATA GRAPH')            
from PyQt4 import Qt
import sys
import visu_png

app = Qt.QApplication(sys.argv)

path_data_graph=os.path.join(DATABASE,protocol,subject,'session_'+session_date,'oisession_analysis/glm_based'+analysis_name,'durbin_watson_test'+cdt+'.png')
view = mainThreadActions().call(visu_png.DataGraphModel,path_data_graph) # New thread creation and call to png vizualizer    

mainThreadActions().push(view.show) # Displaying new window

sys.exit(app.exec_())
