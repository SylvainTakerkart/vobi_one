# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Flavien Garcia <flavien.garcia@free.fr>,
#         Sylvain Takerkart <Sylvain.Takerkart@univ-amu.fr>
# License: BSD Style.

# Displays the dye bleaching, the main components and
# the example-shapes responses created using construct_model

from neuroProcesses import *

name=_t_('Viewer Linear Model')
category=_t_('Viewers')
roles=('viewer',)
userLevel=0 # Always visible

import visu_plot
import pickle
import numpy as np
import os

# The parameters
signature = Signature(
    'input', ReadDiskItem( 'OI GLM Design Matrix' , 'Text file' ), # The condition file, containing the paths of datas and their conditions of experimentation
    'parameters_file', ReadDiskItem( 'OI GLM Parameters', 'Numpy Dump file' ), # The condition file, containing the paths of datas and their conditions of experimentation
)

def initParametersFile( self, inp ):
    """Path of Parameter File in input autocompletion
    
    Parameters
    ----------
    """
    values={} # Value dictionary initialization

    if self.input is not None:
        # Key value autocompletion
        values=self.input.hierarchyAttributes()

    values['filename_variable' ] = 'param' # Key value autocompletion
    return values

def initialization( self ):
    """Parameters values initialization
    """
    self.signature['input'].browseUserLevel = 1 # Browse not visible for basic user
    self.signature['parameters_file'].browseUserLevel = 2 # Browse not visible for basic user
    self.addLink('parameters_file','input',self.initParametersFile) # Change on parameters_file if change on input

def execution(self, context) :
    """The execution process

    Parameters
    ----------
    context : BrainVISA context
    """

    # read in the parameter file
    f=open(self.parameters_file.fullPath().encode("utf8"),'r') # Opening parameters_file
    param=pickle.load(f) # Parameters recuperation
    f.close() # Closing parameters_file*
    
    # compute the time_vector
    time_vector=np.arange(0,round(param[1]*param[0])) / param[0]




    X=np.loadtxt(self.input.fullPath()) # Load X from file

    f=open(os.path.join(os.path.split(self.input.fullPath())[0]\
                                     ,'param.npz').encode("utf8")) # Open parameters file
    L=pickle.load(f)[5] # Load L (number of components)
    f.close() # Close parameters file
 
    series=[X[:,X.shape[1]-L-1],X[:,X.shape[1]-L:X.shape[1]]] # Noise components and components of response model
    titles=("Noise components","Components of the response model","Representative examples of generated responses") # Titles for next figure plot
    try:
        path=os.path.join(os.path.split(self.input.fullPath())[0]\
                                       ,'r_alpha_light').encode("utf8") # By default, second level analysis
        
        source=os.path.split(os.path.split(os.path.split(os.path.split(os.path.split(self.input.fullPath())[0])[0])[0])[0])[0]
        extension=os.path.split(os.path.split(os.path.split(os.path.split(os.path.split(self.input.fullPath())[0])[0])[0])[0])[1]
        session=source[-6:]
        
        if extension=='oitrials_analysis': # First-level analysis
            path=os.path.join(source,'oisession_analysis','glm_based_'\
                             +session,'r_alpha_light').encode("utf8")
            
        f=open(path,'rb') # Open example-shapes response file
        r_alpha=pickle.load(f) # Load r_alpha (example-shapes matrix)
        f.close() # Close example-shapes response file
        series.append(r_alpha) # Add example-shapes to series
    except:    
        context.write("The file does not exist") # The file which includes example-shapes responses does not exist
         
    view = mainThreadActions().call(visu_plot.PlotModel,series,titles,time_vector) # New thread creation and call to plot vizualizer
    mainThreadActions().push( view.show ) # Displaying new window
    return view
