# Author: Flavien Garcia <flavien.garcia@free.fr>
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

"""
Description
-----------

This script processes the oidata functions on some selected raw files.
The process is decomposed in 2 steps :
1. Model construction from a parameter file
2. Application of the model on all trials

This script needs to have already import files

Notes
-----
1. Copy the script in a temporary directory of your choice and cd into this directory
2. Change parameters directly in the script itself
3. Write on a shell : brainvisa --noMainWindow --shell.
4. Write : %run script1_linear_model.py
"""
############################## SECTION TO CHANGE ###############################
DATABASE = '/riou/work/crise/takerkart/vodev_0.3_scripts_gui/' # Database
protocol='protocol_sc' # Protocol name
subject='subject_sc_tbin1_sbin2_alldata' # Subject name
session_date='080313' # Sesion date
analysis_name='_allalexparams01_script' # Analysis name
# Linear model parameters definition
param=(
    110.0, # Sampling frequency
    0.999, # Trial duration
    0.86, # Tau for dye bleaching
    '(1.74,10,40,41,50)', # Frequencies with heartbeat frequency in first
    '(1,1,1,1,1)', # Orders' frequencies
    10, # L = Number of main components used
    '(0.02,0.,0.03,0.45,0.06,0.,0.,0.)', # Alphas min
    '(0.12,0.,0.3,0.6,0.15,0.,0.,0.)') # Alphas max
# corners of the region on the image to define a rectangle
# the figure plots the results averaged on all pixels of this rectangle
corner0=(62,125) # Top left-hand corner for parameters estimation
corner1=(100,150) # Bottom right_hand corner for parameters estimation
format='.nii'
################################################################################








########################## DO NOT TOUCH THIS SECTION ###########################
# Imports
import os
import numpy as np

import oidata.oitrial_processes as oitrial_processes # Trial-level processing functions
import oidata.oisession_preprocesses as oisession_preprocesses # Session-level processing functions

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
    raise ImportError('This script needs to have already import files')
   
print('MODEL CONSTRUCTION')
# Linear Model construction
info_model_files=oisession_preprocesses.construct_model_process(
    database=DATABASE, # Database path
    protocol=protocol, # Protocol name
    subject=subject, # Subject name
    session='session_'+session_date, # Session
    param=param, # Paramaters
    pathX=os.path.join(DATABASE,protocol,subject,'session_'+session_date\
                      ,'oisession_analysis','glm_based'+analysis_name,'glm.txt'), # GLM matrix path
    pathParam=os.path.join(DATABASE,protocol,subject,'session_'+session_date\
                      ,'oisession_analysis','glm_based'+analysis_name,'param.npz'), # Parameters file path
    analysis='glm_based'+analysis_name,
    mode=True,
    script=True)

print('APPLICATION OF THE MODEL')
current_img=0 # Index of current image
for name in raw_name: # For each trial
    # Linear Model application
    oitrial_processes.estimate_model_process(
        info_file_list[current_img]['path'], # Raw data path
        glm=info_model_files['path_def'], # GLM matrix path
        analysis='glm_based'+analysis_name,
        format=format,
        data_graph=os.path.join(os.path.split(os.path.split(info_file_list[current_img]['path'])[0])[0],'glm_based'+analysis_name,name[:-4]+'.png'),
        corner0=corner0,
        corner1=corner1,
        mode=True,
        script=True)
    current_img+=1    
    print('\tProcessed trials:'+str(current_img)+'/'+str(len(raw_name)))    

print('Script was successfully executed')
