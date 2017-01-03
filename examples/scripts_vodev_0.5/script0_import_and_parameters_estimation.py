# Author: Flavien Garcia <flavien.garcia@free.fr>
#         Sylvain Takerkart <Sylvain.Takerkart@univ-amu.fr>
# License: BSD Style.

"""
Description
-----------

This script processes the oidata functions on some selected blk files or
on some raw file already imported.
The process is decomposed in 4 or 6 steps :
1. Data import (if not imported yet)
2. Conditions file creation (if not created yet)
3. Calculates the mean of spectrums of each file and save a data graph
4. Averages each file over a same ROI
5. Estimates the time constant 'tau' for the dye bleaching and the heartbeat
frequency by executing a non-linear fit thanks to Nelder-Mead simplex direct
search method and save results as an histogram data graph
6. Visualization of a data graphs

Notes
-----
1. Copy the script in a temporary directory of your choice and cd into this directory
2. Change parameters directly in the script itself
3. Write on a shell : brainvisa --noMainWindow --shell.
4. Write : %run script0_import_and_parameters_estimation.py
"""
############################## SECTION TO CHANGE ###############################
DATABASE = '/riou/work/crise/takerkart/vodev_0.5/' # Database
DATA_BLK = '/riou/work/crise/takerkart/tethys_data_for_jarron/raw_unimported_data/vobi_one_demo_data/raw_blk_data'
#DATA_BLK = '/riou/work/invibe/DATA/OPTICAL_IMAGING/Monkey_IO/wallace/080313'
protocol='protocol_sc' # Protocol name
subject='wallace_tbin1_sbin2' # Subject name
session_date='080313' # Sesion date (must be in format YYMMDD)
temporal_binning=1
spatial_binning=2
analysis_name='_1' # Analysis name
period = 1./110 # Period between two samples (before the temporal binning)
#conditions_list=['00','01','02','03','04','05','06','15'] # Conditions list of BLK files to import
conditions_list=['00','01','02','03','04','05','06','15'] # Conditions list of BLK files to import
nb_files_by_cdt=2 # The number of files, by conditions, to import.
                  # Let to 0 to apply on all session
                  # If not, type 2 or more (1 is not accepted, and will be replaced by 2)
blank_conditions_list=[0,15] # Raw files to spectral analysis and parameters estimations processes
tau_max=6 # Maximum tau value [in seconds]
corner0=(50,100) # Top left-hand corner for parameters estimation
corner1=(100,150) # Bottom right_hand corner for parameters estimation
format='.nii' # NIfTI (by default) or gz compressed NIfTI
################################################################################


# orig alex values (with spatial binning = 1)
#corner0=(125,250) # Top left-hand corner for parameters estimation
#corner1=(200,300) # Bottom right_hand corner for parameters estimation





########################## DO NOT TOUCH THIS SECTION ###########################
# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path

import os
import numpy as np

import oidata.oisession_preprocesses as oisession_preprocesses # Session-level processing functions
import oidata.oitrial_processes as oitrial_processes # Trial-level processing functions
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import oidata.oisession as oisession

# Parameters validation

# Conditions list
cdt=''
try:
    eval_cdt_list=sorted(eval(str(blank_conditions_list))) # Str to int
    if len(eval_cdt_list)>1 and type(eval_cdt_list[0])!=int:
        raise SyntaxError('Conditions list not properly completed')
except SyntaxError:
    raise SyntaxError('Conditions list is not properly completed')
    
# Maximum value of tau
try:
    tau_max=eval(str(tau_max))
except:
    raise SyntaxError('Please select a number value [in seconds] for maximum tau value')
    
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
    
# Creation of lists of BLK files
blk_list=[] # BLK files list initialization
counter={}
if nb_files_by_cdt==0: # If user want to apply script on all session
    nb_files_by_cdt=len(os.listdir(DATA_BLK))
if nb_files_by_cdt==1:
    nb_files_by_cdt=2
    
for cdt in conditions_list:
    counter[cdt]=0
for name in os.listdir(DATA_BLK): # For each file
    if name[-4:]=='.BLK' and name[2:4] in conditions_list and counter[name[2:4]]<nb_files_by_cdt: # If current file extension is '.BLK'                
        blk_list.append(name) # Add BLK file name
        counter[name[2:4]]+=1

info_file_list=[] # Path initialization

print('IMPORTING RAW DATA INTO THE DATABASE')
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
    print('Importing data...')
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
            temporal_binning=temporal_binning,
            spatial_binning=spatial_binning,
            mode=True,
            script=True)
        current_img+=1
        print('\tImported trial:'+str(current_img)+'/'+str(len(blk_list)))
        info_file_list.append(info_file)
        
    print('CREATION OF THE CONDITIONS FILE FOR EACH SESSION')
    # Creation of the conditions file
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
    raw_name,experiences,trials,conditions,selected=np.loadtxt(path_cond\
                                                              ,delimiter='\t'\
                                                              ,unpack=True\
                                                              ,dtype=str)
  
print('ESTIMATION OF NOISE PARAMETERS ON BLANK TRIALS')
# Conditions list recovery
for c in range(len(eval_cdt_list)): # For each condition
    cdt+='_c'+str(eval_cdt_list[c])

# Region recovery
region='_'+str(corner0[0])+'_'+str(corner0[1])+'_'+str(corner1[0])+'_'+str(corner1[1])

print('\tSpectral analysis')
# Data graph creation
info_model_files=oisession_preprocesses.spectral_analysis_process(
    database=DATABASE, # Database path
    protocol=protocol, # Protocol name
    subject=subject, # Subject name
    session='session_'+session_date , # Session
    analysis='raw', # Analysis type or name
    conditions=blank_conditions_list,
    corner0=corner0,
    corner1=corner1,
    data_graph=os.path.join(DATABASE,protocol,subject,'session_'+session_date,'oisession_analysis/raw','spectral_analysis'+cdt+'.png'),
)

print('\tTau and heartbeat frequency estimation')   
# Data graph creation
info_model_files=oisession_preprocesses.tau_and_heartbeat_frequency_estimation_process(
    DATABASE, # Database path
    protocol, # Protocol name
    subject, # Subject name
    'session_'+session_date , # Session
    'raw', # Analysis type or name
    blank_conditions_list,
    tau_max,
    corner0=corner0,
    corner1=corner1,
    data_graph=os.path.join(DATABASE,protocol,subject,'session_'+session_date,'oisession_analysis/raw','tau_and_fh_histograms'+cdt+region+'.png'),
)

print('PLOTTING ESTIMATION RESULTS')
from PyQt4 import Qt
import sys
import visu_png

app = Qt.QApplication(sys.argv)

view = mainThreadActions().call(visu_png.DataGraphModel,os.path.join(DATABASE,protocol,subject,'session_'+session_date,'oisession_analysis/raw','spectral_analysis'+cdt+'.png')) # New thread creation and call to png vizualizer    

mainThreadActions().push(view.show) # Displaying new window

view2 = mainThreadActions().call(visu_png.DataGraphModel,os.path.join(DATABASE,protocol,subject,'session_'+session_date,'oisession_analysis/raw','tau_and_fh_histograms'+cdt+region+'.png')) # New thread creation and call to png vizualizer

mainThreadActions().push(view2.show) # Displaying new window

sys.exit(app.exec_())
