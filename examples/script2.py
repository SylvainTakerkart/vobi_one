# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

"""
This script processes the oidata functions on some selected files (blank, low- and high-contrast images).
The process is decomposed in 6 steps :
1. data import
2. model creation
3. model application on data
4. outputs averaging
5. region averaging
6. plots

Notes
----------
1. Define environmant variables.
    * export DATA_BLK=$DATA_BLK:path
    * export DATABASE=$DATABASE:path
   Where DATA_BLK is the path of the input datas and DATABASE is the path os th output datas.
2. Write on a shell brainvisa -b --shell.
3. Write : from oidata.examples import script2
"""

# imports
import os
from os import environ
from pylab import figure, plot, show

import oidata.oitrial_processes as oitrial_processes # trial-level processing functions
import oidata.oisession_processes as oisession_processes # session-level processing functions

# global variables
# reading environment variable
DATA_BLK = environ.get("DATA_BLK") # Path to BLK file
DATABASE = environ.get("DATABASE") # Path to database

BLANK_DIRECTORY="TC00" # directory in DATA_BLK which contains blank data
LOWCONTRAST_DIRECTORY="TC01" # directory in DATA_BLK which contains low-contrasted data
HIGHCONTRAST_DIRECTORY="TC06" # directory in DATA_BLK which contains high-contrasted data

# protocole, subject, analysis definitions
protocol='Protocole_test1'
subject='wallace'
analysis_name='gerard'

frame0_window=[0,10]
detrend_window=([0,10],[99,109])

# Creation of lists of blank files
blk_list=os.listdir( os.path.join(DATA_BLK,BLANK_DIRECTORY) )
# Creation of lists of files with different contrasts
lc_list=os.listdir( os.path.join(DATA_BLK,LOWCONTRAST_DIRECTORY) )
hc_list=os.listdir( os.path.join(DATA_BLK,HIGHCONTRAST_DIRECTORY) )

format='.nii' # NIFTI or gz compressed NIFTI

# Parameters definition
param= (
    110.0,
    0.999,
    0.86,
    '(1.74,10,40,41,50)',
    '(1,1,1,1,1)',
    10,
    '(0.02,0.03,0.45,0.06)',
    '(0.12,0.3,0.6,0.15)')

paths=[] # Path initialization

print 'DENOISING'
print 'data loading'

for data_name in lc_list+hc_list:
    # Load datas
    info_file=oitrial_processes.load_data( 
        os.path.join( DATA_BLK,data_name[0:4],data_name ),
        period = 0.0909,
        database=DATABASE,
        protocol=protocol,
        sujet=subject,
        format=format,
        mode=True )

    paths.append(info_file["path"])

print 'model construction'
# Linear Model construction
info_model_files=oisession_processes.construct_model(
    database=DATABASE,
    protocol=protocol,
    subject=subject,
    session=info_file["session"],
    param=param,
    analysis='glm_based'+analysis_name,
    mode=True )

print 'applying model'
for path in paths:
    # Linear Model application
    oitrial_processes.apply_model(
        data=path,
        glm=info_model_files["path_def"],
        analysis='glm_based'+analysis_name,
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

print 'denoised files averaging'
# Processing images averaging
path_averaged=oisession_processes.average(
    DATABASE,
    protocol,
    subject,
    info_file["session"],
    'glm_based' + analysis_name,
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
    'glm_based'+analysis_name,
    info_file["session"][8:16]+'_averaged_1'+format,
    (116,224), (136,254),
    format=format,
    mode=True
    )

(y_6,pathAv6) = oisession_processes.average_region(
    DATABASE,
    protocol,
    subject,
    info_file["session"],
    'glm_based'+analysis_name,
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
