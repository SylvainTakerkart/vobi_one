# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Creates a condition file, containing the paths of datas and their conditions of experimentation. It is read to perform the session-level processes.

# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path

# Header 
name = _t_('Create Conditions File') # Process name in the GUI
category = _t_('Session Pre-Analysis') # Category name in the GU
userLevel=0 # Always visible

# The parameters
signature=Signature(
    'conditions_file', WriteDiskItem( 'Trials+conditions list' , 'Text file' ),
    )

def initialization( self ):
    """Parameters values initialization
    """
    self.signature["conditions_file"].browseUserLevel = 2 # Browse only visible for expert user

def execution( self, context ):
    """The execution process
    
    Parameters
    ----------
    context : BrainVISA context
    """
    import oidata.oisession_preprocesses as oisession_preprocesses

    attributes = self.conditions_file.hierarchyAttributes() # Attributes recuperation

    # Creates a condition file, containing the paths of datas and their conditions of experimentation. It is read to perform the session-level processes
    oisession_preprocesses.create_trials_conds_file_process(
        attributes["_database"],
        attributes["protocol"],
        attributes['subject'],
        'session_' + attributes["session_date"],
        context)
