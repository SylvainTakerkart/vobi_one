# Author: Flavien Garcia <flavien.garcia@free.fr>
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

"""
Description
-----------

This script processes the oidata functions on some selected, by two model
and conditions, denoised files on the same ROIs.
The process is decomposed in 3 steps :
1. Conditions file recovery
2. Create a data graph with mean response of linear model and of standard model
3. Visualization of data graph

This script needs to have already apply linear model

Notes
-----
1. Copy the script in a temporary directory of your choice and cd into this directory
2. Change parameters directly in the script itself
3. Write on a shell : brainvisa --noMainWindow --shell.
4. Write : %run script4_comparison_of_analyses.py
"""
############################## SECTION TO CHANGE ###############################
DATABASE = '/home/garcia/data/brainvisa_db/' # Database
protocol='protocol_sc' # Protocol name
subject='subject_sc' # Subject name
# First analysis
session_date_1='080313' # Sesion date
model_1='GLM' # Model ('GLM' for Linear Model,
              #        'BkS' for Blank Subtraction
              #        'BkSD' for Blank Subtraction + Detrending)
analysis_name_1='_1' # Analysis name
conditions_list_1=[6] # Conditions list

# Second analysis
session_date_2='080313' # Sesion date
model_2='BkS' # Model ('GLM' for Linear Model,
              #        'BkS' for Blank Subtraction
              #        'BkSD' for Blank Subtraction + Detrending)
analysis_name_2='_1' # Analysis name
conditions_list_2=[6] # Conditions list

# Others parameters
corner0=(125,250) # Top left-hand corner
corner1=(200,300) # Bottom right_hand corner
format='.nii' # NIfTI (by default) or gz compressed NIfTI
################################################################################








########################## DO NOT TOUCH THIS SECTION ###########################
# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path

import os
import numpy as np

import oidata.oisession_postprocesses as oisession_postprocesses # Session-level processing functions

# Parameters validation

# Top left-hand corner
try:
    c0=eval(str(corner0)) # Values recovery
except SyntaxError:
    raise SyntaxError('Top left-hand corner is not properly completed')
try:
    if len(c0)==2:
        corner0=c0
    else:
        raise SyntaxError('Top left-hand corner is not properly completed')        
except TypeError:
    raise TypeError('Top left-hand corner is not properly completed')
    
# Bottom right-hand corner
try:
    c1=eval(str(corner1)) # Values recovery
except SyntaxError:
    raise SyntaxError('Bottom right-hand corner is not properly completed')
try:
    if len(c1)==2:
        corner1=c1
    else:
        raise SyntaxError('Top left-hand corner is not properly completed')        
except TypeError:
    raise TypeError('Bottom right-hand corner is not properly completed')
region='Over_'+str(corner0[0])+'_'+str(corner0[1])+'_'+str(corner1[0])+'_'+str(corner1[1])+'_'    

attributes_list=[]
# Linear Model analysis attributes recovery
attributes={}
attributes['_database']=DATABASE   
attributes['protocol']=protocol
attributes['subject']=subject
attributes['session_date']=session_date_1
attributes['conditions_list']=conditions_list_1
# Model
if model_1[:3]=='GLM':
    model='glm_based'
    blank_based_suffix_1=''
elif model_1[:4]=='BkSD':
    model='blank_based'
    blank_based_suffix_1='_f0d_bks_d'
elif model_1[:3]=='BkS':
    model='blank_based'
    blank_based_suffix_1='_f0d_bks'
else:
    raise SyntaxError('Model of first analysis is not properly completed')
attributes['analysis_name']=model+analysis_name_1
attributes['blank_based_suffix']=blank_based_suffix_1
attributes_list.append(attributes)

# Standard Model analysis attributes recovery
attributes={}
attributes['_database']=DATABASE   
attributes['protocol']=protocol
attributes['subject']=subject
attributes['session_date']=session_date_2
if model_2[:3]=='GLM':
    model='glm_based'
    blank_based_suffix_2=''
elif model_2[:4]=='BkSD':
    model='blank_based'
    blank_based_suffix_2='_f0d_bks_d'
elif model_2[:3]=='BkS':
    model='blank_based'
    blank_based_suffix_2='_f0d_bks'
else:
    raise SyntaxError('Model of first analysis is not properly completed') 
attributes['analysis_name']=model+analysis_name_2
attributes['blank_based_suffix']=blank_based_suffix_2
attributes['conditions_list']=conditions_list_2
attributes_list.append(attributes)

# Conditions lists
cdt_1=''
try:
    eval_cdt_list=sorted(eval(str(conditions_list_1))) # Str to int
    if len(eval_cdt_list)>1 and type(eval_cdt_list[0])!=int:
        raise SyntaxError('Conditions list of first analysis is not properly completed')
    for g in range(len(eval_cdt_list)): # For each group
        cdt_1+='_c'
        if type(eval_cdt_list[g])==int:
            eval_cdt_list[g]=[eval_cdt_list[g]]
            for c in range(len(eval_cdt_list[g])-1):
                cdt_1+=str(eval_cdt_list[g][c])+'+'
            cdt_1+=str(eval_cdt_list[g][len(eval_cdt_list[g])-1])
except SyntaxError:
    raise SyntaxError('Conditions list of first analysis is not properly completed')
    
cdt_2=''
try:
    eval_cdt_list=sorted(eval(str(conditions_list_2))) # Str to int
    if len(eval_cdt_list)>1 and type(eval_cdt_list[0])!=int:
        raise SyntaxError('Conditions list of second analysis is not properly completed')
    for g in range(len(eval_cdt_list)): # For each group
        cdt_2+='_c'
        if type(eval_cdt_list[g])==int:
            eval_cdt_list[g]=[eval_cdt_list[g]]
            for c in range(len(eval_cdt_list[g])-1):
                cdt_1+=str(eval_cdt_list[g][c])+'+'
            cdt_2+=str(eval_cdt_list[g][len(eval_cdt_list[g])-1])
except SyntaxError:
    raise SyntaxError('Conditions list of second analysis is not properly completed')  
          
print('CREATION OF DATA GRAPHS')
info_model_files=oisession_postprocesses.comparison_of_analyses_process(
    attributes_list,
    data_graph=os.path.join(DATABASE,protocol,subject,region+'on_'+model_1\
               +'_session_'+session_date_1+'_analysis'+analysis_name_1+cdt_1
               +'_and_on_'+model_2+'_session_'+session_date_2+'_analysis'+analysis_name_2+cdt_2+'.png'),
)

print('VISUALIZATION OF DATA GRAPH')              
from PyQt4 import Qt
import sys
import visu_png

app = Qt.QApplication(sys.argv)

path_data_graph=os.path.join(DATABASE,protocol,subject,region+'on_'+model_1\
               +'_session_'+session_date_1+'_analysis'+analysis_name_1+cdt_1
               +'_and_on_'+model_2+'_session_'+session_date_2+'_analysis'+analysis_name_2+cdt_2+'.png')
view = mainThreadActions().call(visu_png.DataGraphModel,path_data_graph) # New thread creation and call to png vizualizer    

mainThreadActions().push(view.show) # Displaying new window

sys.exit(app.exec_())

