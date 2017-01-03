# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

"""
This script processes the oidata functions on some selected files (blank, low- and high-contrast images).
The process is decomposed in 8 steps :
1. data import (removed)
2. blank averaging
3. frame0 division
4. blank substraction
5. linear detrending
6. outputs averaging
7. region averaging
8. plot

Notes
----------
1. Define environmant variables.
    * export DATA_BLK=$DATA_BLK:path
    * export DATABASE=$DATABASE:path
   Where DATA_BLK is the path of the input datas and DATABASE is the path os th output datas.
2. Write on a shell brainvisa -b --shell.
3. Write : from oidata.exemples import script1
"""

############################## SECTION TO CHANGE ###############################
DATABASE = '/riou/work/crise/takerkart/vodev_0.5/' # Database
#DATA_BLK = '/riou/work/invibe/DATA/OPTICAL_IMAGING/Monkey_IO/wallace/080313'
protocol='protocol_sc' # Protocol name
subject='wallace_tbin1_sbin2_testblank' # Subject name
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
frame0_window=[0,10]
detrend_window=([0,10],[99,109])
format='.nii' # NIfTI (by default) or gz compressed NIfTI
################################################################################



########################## DO NOT TOUCH THIS SECTION ###########################
# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path
import os
from os import environ
from pylab import figure, plot, show
import numpy as np

import oidata.oitrial_processes as oitrial_processes # trial-level processing functions
import oidata.oisession_postprocesses as oisession_postprocesses # session-level processing functions
import oidata.oisession_preprocesses as oisession_preprocesses # session-level processing functions

print('CONDITIONS FILE RECOVERY')
blank_info_file_list=[] # Path initialization
stimul_info_file_list=[] # Path initialization
try: # Verify if a conditions file already exists
    # Conditions file path creation
    path_cond=os.path.join(DATABASE\
                          ,protocol\
                          ,subject\
                          ,'session_'+session_date \
                          ,'oitrials_analysis/conditions.txt')
                          
    # Conditions file path recovery                      
    raw_name,experiences,trials,conditions_list,selected=np.loadtxt(path_cond\
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
        if blank_conditions_list.count(int(condition)):
            blank_info_file_list.append(info_file) # Add info filelist of blank trials
        else:
            stimul_info_file_list.append(info_file) # Add info filelist of trials with stim
            

except: # If not, data import is needed
    raise ImportError('This script needs to have already import files')






"""# global variables
# reading environment variable
DATA_BLK = environ.get("DATA_BLK") # Path to BLK file
DATABASE = environ.get("DATABASE") # Path to database

BLANK_DIRECTORY="TC00" # directory in DATA_BLK which contains blank data
LOWCONTRAST_DIRECTORY="TC01" # directory in DATA_BLK which contains low-contrasted data
HIGHCONTRAST_DIRECTORY="TC06" # directory in DATA_BLK which contains high-contrasted data

# protocole, subject, analysis definitions
protocol='Protocole_test1'
subject='wallace'
analysis_name='_patate'


# Creation of lists of blank files
blk_list=os.listdir( os.path.join(DATA_BLK,BLANK_DIRECTORY) )
# Creation of lists of files with different contrasts
lc_list=os.listdir( os.path.join(DATA_BLK,LOWCONTRAST_DIRECTORY) )
hc_list=os.listdir( os.path.join(DATA_BLK,HIGHCONTRAST_DIRECTORY) )
"""

"""
print 'BLANK AVERAGING'
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
"""


"""
# Importation of blank images
for blk_name in blk_list:
    info_file = oitrial_processes.import_blk_data( 
        os.path.join( DATA_BLK,BLANK_DIRECTORY,blk_name ),
        period = 0.0909,
        database=DATABASE,
        protocol=protocol,
        sujet=subject,
        format=format,
        mode=True )

print 'conditions list creation'
# Creation of a condition file
oisession_processes.create_list( 
    DATABASE,
    protocol,
    subject,
    info_file["session"],
    mode=True
    )
"""

print 'blanks averaging'
# Processing blanks averaging
path=oisession_postprocesses.average_trials_process(
    DATABASE,
    protocol,
    subject,
    'session_'+info_file["session"],
    'raw',
    blank_conditions_list,
    format=format,
    mode=True,
    script=True
    )

blank_averaged=os.path.join(path,info_file["session"][8:16]+'_averaged_0'+format)

"""
print 'DENOISING'
for data_name in lc_list+hc_list:
    # Load datas
    info_file = oitrial_processes.load_data( 
        os.path.join( DATA_BLK,data_name[0:4],data_name ),
        period = 0.0909,
        database=DATABASE,
        protocol=protocol,
        sujet=subject,
        format=format,
        mode=True )

    # The frame0 division
    path=oitrial_processes.frame0_division(
        frame0_window,
        info_file["path"],
        database=DATABASE,
        protocol=protocol,
        sujet=subject,
        session=info_file["session"],
        exp=info_file["exp"],
        trial=info_file["trial"],
        analysis='blank_based'+analysis_name,
        format=format,
        mode=True )

    # The blank substraction
    path=oitrial_processes.blank_substraction(
        path,
        path_average=blank_averaged,
        database=DATABASE,
        protocol=protocol,
        sujet=subject,
        session=info_file["session"],
        exp=info_file["exp"],
        trial=info_file["trial"],
        analysis='blank_based'+analysis_name,
        format=format,
        mode=True )

    # The linear detrend
    path=oitrial_processes.linear_detrend(
        detrend_window[0],
        detrend_window[1],
        path,
        database=DATABASE,
        protocol=protocol,
        sujet=subject,
        session=info_file["session"],
        exp=info_file["exp"],
        trial=info_file["trial"],
        analysis='blank_based'+analysis_name,
        format=format,
        mode=True )

print 'BKSD AVERAGING'
print 'conditions list creation'
# Creation of a condition file
oisession_processes.create_list( 
    DATABASE,
    protocol,
    subject,
    info_file["session"],
    mode=True
    )

print 'bksd averaging'
# Processing images averaging
path_averaged=oisession_processes.average(
    DATABASE,
    protocol,
    subject,
    info_file["session"],
    'blank_based'+analysis_name,
    ([1,],[6,],),
    format=format,
    mode=True
    )

print 'REGION AVERAGING'
# Processing region averaging
(y_1,pathAv1) = oisession_processes.average_region(
    DATABASE,
    protocol,
    subject,
    info_file["session"],
    'blank_based'+analysis_name,
    info_file["session"][8:16]+'_averaged_1'+format,
    (116,224), (136,254),
    mode=True
    )

(y_6,pathAv6) = oisession_processes.average_region(
    DATABASE,
    protocol,
    subject,
    info_file["session"],
    'blank_based'+analysis_name,
    info_file["session"][8:16]+'_averaged_6'+format,
    (116,224), (136,254),
    format=format,
    mode=True
    )

# Plot
figure(1)
plot(y_1)
figure(2)
plot(y_6)
show()
"""
