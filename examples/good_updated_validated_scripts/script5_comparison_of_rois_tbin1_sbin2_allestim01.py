# Author: Flavien Garcia <flavien.garcia@free.fr>
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.
import os
"""
Description
-----------

This script processes the oidata functions on some selected, by one model and
conditions, denoised files over several ROIs.
The process is decomposed in 3 steps :
1. Conditions file recovery
2. Create a data graph with mean response of linear model over each region
3. Visualization of data graph

This script needs to have already apply linear model

Notes
-----
1. Copy the script in a temporary directory of your choice and cd into this directory
2. Change parameters directly in the script itself
3. Write on a shell : brainvisa --noMainWindow --shell.
4. Write : %run script5_comparison_of_rois.py
"""
############################## SECTION TO CHANGE ###############################
DATABASE = '/riou/work/crise/takerkart/vodev_0.5/' # Database
protocol='protocol_sc' # Protocol name
subject='wallace_tbin1_sbin2' # Subject name
session_date='080313' # Sesion date
analysis_name='_allestim01' # Analysis name
model='GLM' # Model ('GLM' for Linear Model,
            #        'BkS' for Blank Subtraction
            #        'BkSD' for Blank Subtraction + Detrending)
conditions_list=[6] # Conditions list

# First ROI
roi_1=((50,100),(100,150))
# Second ROI
roi_2=((50,150),(100,200))
#roi_2=os.path.join(DATABASE,protocol,subject,'session_'+session_date,'oisession_analysis/mask','mask_145_200_200_250.nii')

################################################################################








########################## DO NOT TOUCH THIS SECTION ###########################
# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path

import numpy as np

import oidata.oisession_postprocesses as oisession_postprocesses # Session-level processing functions

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

except: # If not, data import is needed
    raise ImportError('This script needs to have already apply linear model')
  
print('CREATION OF DATA GRAPH')
# Parameters validation

if model[:3]=='GLM':
    mod='glm_based'
    blank_based_suffix=''
elif model[:4]=='BkSD':
    mod='blank_based'
    blank_based_suffix='_f0d_bks_d'
elif model[:3]=='BkS':
    mod='blank_based'
    blank_based_suffix='_f0d_bks'
else:
    raise SyntaxError('Model is not properly completed')
    
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
# ROIs recovery
rois_list=[]
if type(roi_1)==tuple:
    try:
        c0=eval(str(roi_1[0]))
    except SyntaxError:
        raise SyntaxError('Top left-hand corner of first ROI is not properly completed')
    try:
        if len(c0)==2:
            corner0=c0
        else:
            raise SyntaxError('Top left-hand corner of first ROI is not properly completed')        
    except TypeError:
        raise TypeError('Top left-hand corner of first ROI is not properly completed') 
            # Bottom right-hand corner recovery    
    try:
        c1=eval(str(roi_1[1]))
    except SyntaxError:
        raise SyntaxError('Bottom right-hand corner of first ROI is not properly completed')
    try:
        if len(c1)==2:
            corner1=c1
        else:
            raise SyntaxError('Bottom right-hand corner of first ROI is not properly completed')        
    except TypeError:
        raise TypeError('Bottom right-hand corner of first ROI is not properly completed')
    roi_1_name='_'+str(corner0[0])+'_'+str(corner0[1])+'_'+str(corner1[0])+'_'+str(corner1[1])
    rois_list.append((corner0,corner1))
if type(roi_1)==str:
    if os.path.exists(roi_1.encode('utf8')):
        roi_1_name=os.path.basename[:-len(format)]
        rois_list.append(roi_1)
    else:
        raise SyntaxError('Please check the path of first ROI mask')
        
# Second ROI
if type(roi_2)==tuple:
    try:
        c0=eval(str(roi_2[0]))
    except SyntaxError:
        raise SyntaxError('Top left-hand corner of second ROI is not properly completed')
    try:
        if len(c0)==2:
            corner0=c0
        else:
            raise SyntaxError('Top left-hand corner of second ROI is not properly completed')        
    except TypeError:
        raise TypeError('Top left-hand corner of second ROI is not properly completed') 
            # Bottom right-hand corner recovery    
    try:
        c1=eval(str(roi_2[1]))
    except SyntaxError:
        raise SyntaxError('Bottom right-hand corner of second ROI is not properly completed')
    try:
        if len(c1)==2:
            corner1=c1
        else:
            raise SyntaxError('Bottom right-hand corner of second ROI is not properly completed')        
    except TypeError:
        raise TypeError('Bottom right-hand corner of second ROI is not properly completed')
    roi_2_name='_'+str(corner0[0])+'_'+str(corner0[1])+'_'+str(corner1[0])+'_'+str(corner1[1])
    rois_list.append((corner0,corner1))
if type(roi_2)==str:
    if os.path.exists(roi_2.encode('utf8')):
        roi_2_name=os.path.basename[:-len(format)]
        rois_list.append(roi_2)
    else:
        raise SyntaxError('Please check the path of second ROI mask')

           
info_model_files=oisession_postprocesses.comparison_of_rois_process(
    DATABASE,
    protocol,
    subject,
    'session_'+session_date,
    mod+analysis_name,
    conditions_list,
    blank_based_suffix,
    [roi_1,roi_2],
    data_graph=os.path.join(DATABASE,protocol,subject,'session_'+session_date,'oisession_analysis',mod+analysis_name,model+cdt+'_over_'+roi_1_name+'_and_'+roi_2_name+'.png'),
)

print('VISUALIZATION OF DATA GRAPH')             
from PyQt4 import Qt
import sys
import visu_png

app = Qt.QApplication(sys.argv)

path_data_graph=os.path.join(DATABASE,protocol,subject,'session_'+session_date,'oisession_analysis',mod+analysis_name,model+cdt+'_over_'+roi_1_name+'_and_'+roi_2_name+'.png')
view = mainThreadActions().call(visu_png.DataGraphModel,path_data_graph) # New thread creation and call to png vizualizer    

mainThreadActions().push(view.show) # Displaying new window

sys.exit(app.exec_())

