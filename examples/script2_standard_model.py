# Author: Flavien Garcia <flavien.garcia@free.fr>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

"""
This script processes the oidata functions on some selected files (10 trials
by condition).
The process is decomposed in 4 or 6 steps :
1. Data import (if not imported yet)
2. Conditions file creation (if not created yet)
3. Blanks averaging
4. Frame0 division
5. Blank subtraction
6. Linear detrending

Notes
-----
1. Copy the script in a temporary directory of your choice and cd into this directory
2. Change parameters directly in the script itself
3. Write on a shell : brainvisa --noMainWindow --shell.
4. Write : %run script_standard_model.py
"""
############################## SECTION TO CHANGE ###############################
DATABASE = '/home/garcia/data/brainvisa_db/' # Database
DATA_BLK = '/home/garcia/spawn/work/dyva/DATA/OPTICAL_IMAGING/Monkey_IO/wallace/080313/'
protocol='protocol_sc' # Protocol name
subject='subject_sc' # Subject name
session_date='080313' # Sesion date
analysis_name='_1' # Analysis name
period = 0.0909 # Period between two samples

blk_conditions_list=['00','01','02','03','04','05','06','15'] # Conditions list of BLK files to import
nb_files_by_cdt=0 # The number of files, by conditions, to import.
                  # Let to 0 to apply on all session
                  # If not, type 2 or more (1 is not accepted, and will be replaced by 2)
blank_conditions_list=[0] # Raw files to averages trials
not_blank_conditions_list=['01','02','03','04','05','06'] # Conditions list of not blank files

frame0_window=[0,10] # Frames selection for frame0 division
detrend_window=([0,10],[100,110]) # Frames selection for linear detrending
format='.nii' # NIfTI (by default) or gz compressed NIfTI
################################################################################








########################## DO NOT TOUCH THIS SECTION ###########################
# imports
import os
import numpy as np

import oidata.oitrial_processes as oitrial_processes # Trial-level processing functions
import oidata.oisession_preprocesses as oisession_preprocesses # Session-level processing functions
import oidata.oisession_postprocesses as oisession_postprocesses # Session-level processing functions

# Parameters validation

# Conditions list
cdt=''
try:
    eval_cdt_list=sorted(eval(str(blank_conditions_list))) # Str to int
    if len(eval_cdt_list)>1 and type(eval_cdt_list[0])!=int:
        raise SyntaxError('Conditions list not properly completed')
except SyntaxError:
    raise SyntaxError('Conditions list is not properly completed')
cdt=''
for i in eval_cdt_list:
    if len(str(i))==1:
        cdt+='_c00'+str(i)
    elif len(str(i))==2:
        cdt+='_c0'+str(i)

# Creation of lists of BLK files
blk_list=[] # BLK files list initialization
counter={}
if nb_files_by_cdt==0: # If user want to apply script on all session
    nb_files_by_cdt=len(os.listdir(DATA_BLK))
if nb_files_by_cdt==1:
    nb_files_by_cdt=2

for c in blk_conditions_list:
    counter[c]=0
for name in os.listdir(DATA_BLK): # For each file
    if name[-4:]=='.BLK' and name[2:4] in blk_conditions_list and counter[name[2:4]]<nb_files_by_cdt: # If current file extension is '.BLK'                
        blk_list.append(name) # Add BLK file name
        counter[name[2:4]]+=1
        
info_file_list=[] # Path initialization

print('DATA IMPORT')
try: # Verify if a conditions file already exists
    # Conditions file path creation
    path_cond=os.path.join(DATABASE\
                          ,protocol\
                          ,subject\
                          ,'session_'+session_date\
                          ,'oitrials_analysis/conditions.txt')
                          
    # Conditions file path recovery                      
    raw_name,experiences,trials,conditions,selected=np.loadtxt(path_cond, delimiter='\t', unpack=True,dtype=str)
    
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
    
    print('Data already imported') # Inform user data are already imported
    imported=True # Data already imported
except: # If not, data import is needed
    imported=False # Data not imported yet

if imported==False: # If data not imported yet
    print('Data loading')
    # Load datas
    current_img=0 # Index of current image
    for blk_name in blk_list: # For each blk file
        info_file=oitrial_processes.import_external_data_process( 
            input=os.path.join(DATA_BLK,blk_name), # File path
            period = period, # Period between two frames
            database=DATABASE, # Database path
            protocol=protocol, # Protocol name
            subject=subject, # Subject name
            format=format,
            mode=True,
            script=True)
        current_img+=1
        print('\tData loaded:'+str(current_img)+'/'+str(len(blk_list)))
        info_file_list.append(info_file)
        
    print('CONDITIONS FILE CREATION')
    # Creation of a condition file
    oisession_preprocesses.create_trials_conds_file_process( 
        DATABASE, # Database path
        protocol, # Protocol name
        subject, # Subject name
        'session_'+session_date, # Session
        mode=True,
        script=True)
        
    # Conditions file path creation
    path_cond=os.path.join(DATABASE\
                          ,protocol\
                          ,subject\
                          ,'session_'+session_date\
                          ,'oitrials_analysis/conditions.txt')
    # Conditions file path recovery
    raw_name,experiences,trials,conditions,selected=np.loadtxt(path_cond, delimiter='\t', unpack=True,dtype=str)

print 'FRAME0 DIVISION'
current_img=0 # Index of current image
f0d_list=[]
for data_name in raw_name: # For each file
    # The frame0 division
    path=oitrial_processes.frame0_division_process(
        frame0_window, # First frames
        info_file_list[current_img]['path'], # Files path
        database=DATABASE, # Database path
        protocol=protocol, # Protocol name
        subject=subject, # Subject name
        session='session_'+session_date, # Session
        exp='exp'+info_file_list[current_img]['exp'], # Experiment
        trial='trial'+info_file_list[current_img]['trial'], # Trial
        analysis='blank_based'+analysis_name,  
        format=format,
        mode=True,
        script=True)
    f0d_list.append(path)
    current_img+=1
    print('\tProcessed trials:'+str(current_img)+'/'+str(len(raw_name)))
print('All trials processed by frame0 division')
    
print('BLANKS AVERAGING')
# Processing blanks averaging
path=oisession_postprocesses.average_trials_process(
    DATABASE, # Database path
    protocol, # Protocol name
    subject, # Subject name
    'session_'+session_date, # Session
    'blank_based'+analysis_name, # Only on raw data
    (blank_conditions_list), # Only blank files
    format=format,
    blank_based_suffix='_f0d',
    mode=True,
    script=True
    )


blank_averaged=os.path.join(path,'s'+info_file['session']+'_blank_based'+analysis_name+cdt+'_mean'+format)
print('BLANK SUBTRACTION AND LINEAR DETRENDING')
for current_img in range(len(raw_name)): # For each file
    if info_file_list[current_img]['condition'] not in not_blank_conditions_list: # Only not blank files

        # The blank subtraction
        path=oitrial_processes.blank_subtraction_process(
            f0d_list[current_img], # Path of file obtained after frame0 division
            path_average=blank_averaged, # Mean of blanks path
            database=DATABASE, # Database path
            protocol=protocol, # Protocol name
            subject=subject, # Subject name
            session='session_'+session_date, # Session
            exp='exp'+info_file_list[current_img]['exp'], # Experiment
            trial='trial'+info_file_list[current_img]['trial'], # Trial
            analysis='blank_based'+analysis_name,
            format=format,
            mode=True,
            script=True)

        # The linear detrend
        path=oitrial_processes.linear_detrend_process(
            detrend_window[0], # First frames
            detrend_window[1], # Last frames
            path, # Path of files obtained after blank subtraction
            database=DATABASE, # Database path
            protocol=protocol, # Protocol name
            subject=subject, # Subject name
            session='session_'+session_date, # Session
            exp='exp'+info_file_list[current_img]['exp'], # Experiment
            trial='trial'+info_file_list[current_img]['trial'], # Trial
            analysis='blank_based'+analysis_name,
            format=format,
            mode=True,
            script=True)
    print('\tProcessed trials:'+str(current_img+1)+'/'+str(len(raw_name)))
    
print('Script was successfully executed')
