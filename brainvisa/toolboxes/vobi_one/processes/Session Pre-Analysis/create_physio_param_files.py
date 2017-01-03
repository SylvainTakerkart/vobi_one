# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Flavien Garcia <flavien.garcia@free.fr>,
#         Caroline Piron <piron.caroline@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@univ-amu.fr>
# License: BSD Style.

# Creates a text file containing one line per trial; each line list the physiological parameters externally estimated (frequency and phase of heartbeat and respiration). The process actually only copies the file (i.e. it assumes the formatting is correct) into the database and renames it properly.

# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path

# Header 
name = _t_('Create physiological params File') # Process name in the GUI
category = _t_('Session Pre-Analysis') # Category name in the GU
userLevel=2 # Experts only because still in testing mode

# The parameters
signature=Signature(
    'raw_physio_file', ReadDiskItem('Unimported physiological parameters', 'Text file' ),# The conditionunimported physiological parameters file path
    'conditions_file', ReadDiskItem( 'Trials+conditions list' , 'Text file' ), # The condition file path
    'physio_params_file', WriteDiskItem( 'Physiological parameters' , 'Text file' )
    )


def initialization( self ):
    """Parameters values initialization
    """
    self.signature[ "raw_physio_file" ].databaseUserLevel = 3 # Database never visible
    self.signature["physio_params_file"].browseUserLevel = 2 # Browse only visible for expert user
    self.signature['conditions_file'].browseUserLevel=2 # Browse only visible for expert user

    # Links between parameters for autocompletion
    self.addLink( 'physio_params_file', 'conditions_file') # Change of physio_params_file if change on conditions_file


def execution( self, context ):
    """The execution process
    
    Parameters
    ----------
    context : BrainVISA context
    """
  
    import oidata.oisession_preprocesses as oisession_preprocesses

    attributes = self.conditions_file.hierarchyAttributes() # Attributes recuperation

    print self.raw_physio_file.fullPath()

    # Creates a condition file, containing the paths of datas and their conditions of experimentation. It is read to perform the session-level processes
    oisession_preprocesses.create_physio_params_file_process(
	    attributes["_database"],
	    attributes["protocol"],
	    attributes['subject'],
	    'session_' + attributes["session_date"],
	    self.raw_physio_file.fullPath())
