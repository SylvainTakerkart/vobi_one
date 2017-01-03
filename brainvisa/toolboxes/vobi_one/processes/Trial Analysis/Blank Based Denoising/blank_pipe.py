# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Blank_pipe. This pipeline is a component of blankbased_pipeline. It is used to choice in GUI between blank_division and blank_subtraction.
# Makes the link between blankbased_pipeline and those processes.

from neuroProcesses import *

name=_t_('Blank Pipe')
category = _t_('Blank Based Denoising')
userLevel=3 # Never visible

# Parameters
signature=Signature(
    "data", ReadDiskItem( 'OI 2D+t Image' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # Input image path
    "average_file", ReadDiskItem( 'OI 2D+t Blank Mean' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The averaged raw image
    "bksd_data", WriteDiskItem( 'OI BkSD' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The path of the image after blank division
)

def initValuesAverage( self,inp ):
    """Averaged file autocompletion

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    value = {} # Value dictionary initialization
    if self.data is not None:
        # Key value autocompletion
        attributes=self.data.hierarchyAttributes()
        value['protocol']=self.data.hierarchyAttributes()['protocol']
        value['subject']=self.data.hierarchyAttributes()['subject']
        value['session_date']=self.data.hierarchyAttributes()['session_date']

        if 'firstlevel_analysis' in value == True:
            value['firstlevel_analysis']=self.data.hierarchyAttributes()['secondlevel_analysis']

    return value

def selected( self,subproc ):
    """Controls the selection between the two process

    Parameters
    ----------
    subroc : bool
        The choice box value
    """
    if subproc._selected: # If blank_subtraction is selected
        self.bksd_data=self._executionNode.blank_subtraction.bks_data # Initialization of pipeline's bksd_data with blank_subtraction process's bks_data
        self.average_file=self._executionNode.blank_subtraction.average_file # Initialization of pipeline's average_file with blank_subtraction process' average_file
        self._executionNode.addLink('bksd_data','blank_subtraction.bks_data' ) # Link between pipeline's bksd_data and blank_subtraction process' bks_data
        self._executionNode.removeLink( 'bksd_data','blank_division.bkd_data' ) # Remove ink between pipeline's bksd_data and blank_division process' bkd_data

    else: # If blank_division is selected
        self.bksd_data=self._executionNode.blank_division.bkd_data# Initialization of pipeline bksd_data with blank_division process' bkd_data
        self.average_file=self._executionNode.blank_division.average_file # Initialization of pipeline's average_file with blank_division process' average_file
        self._executionNode.addLink('bksd_data','blank_division.bkd_data' ) # Link between pipeline's bksd_data and blank_division process' bkd_data
        self._executionNode.removeLink('bksd_data','blank_subtraction.bks_data' ) # Remove link between pipeline's bksd_data and blank_subtraction process' bks_data

def initialization( self ):
    """Parameters values initialization
    """
    eNode = SelectionExecutionNode( self.name, parameterized = self ) # Declaration of a new selection pipeline
    eNode.addChild( 'blank_subtraction',ProcessExecutionNode('blank_subtraction', optional = 1, selected=1 ) ) # Add blank_subtraction to pipeline
    eNode.addChild( 'blank_division',ProcessExecutionNode('blank_division', optional = 1, selected = 0 ) ) # Add blank_division to pipeline

    # Change of blank_subtraction signature
    bksSignature=[ "data", ReadDiskItem( 'OI 2D+t Image' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                   "average_file", ReadDiskItem( 'OI 2D+t Blank Mean' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                   "bks_data", WriteDiskItem( 'OI BkSD' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                   ]

    # Change of blank_division signature
    bkdSignature=[ "data", ReadDiskItem( 'OI 2D+t Image' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                   "average_file", ReadDiskItem( 'OI 2D+t Blank Mean' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                   "bkd_data", WriteDiskItem( 'OI BkSD' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                   ]

    # Applies changes on signatures
    bks=Signature( *bksSignature )
    eNode.blank_subtraction.changeSignature( bks )
    bkd=Signature( *bkdSignature )
    eNode.blank_division.changeSignature( bkd )

    self.signature['data'].browseUserLevel=2 # Browse only visible for expert user
    self.signature['average_file'].browseUserLevel=2 # Browse only visible for expert user
    self.signature['bksd_data'].browseUserLevel=2 # Browse only visible for expert user

    eNode.blank_subtraction.signature['data'].browseUserLevel=3 # Browse never visible
    eNode.blank_subtraction.signature['data'].databaseUserLevel=3 # Database never visible
    eNode.blank_division.signature['data'].browseUserLevel=3 # Browse never visible
    eNode.blank_division.signature['data'].databaseUserLevel=3 # Database never visible

    eNode.blank_subtraction.signature['average_file'].browseUserLevel=3 # Browse never visible
    eNode.blank_subtraction.signature['average_file'].databaseUserLevel=3 # Database never visible
    eNode.blank_division.signature['average_file'].browseUserLevel=3 # Browse never visible
    eNode.blank_division.signature['average_file'].databaseUserLevel=3 # Database never visible

    eNode.blank_subtraction.signature['bks_data'].browseUserLevel=2 # Browse only visible for expert user
    eNode.blank_subtraction.signature['bks_data'].databaseUserLevel=2 # Database only visible for expert user
    eNode.blank_division.signature['bkd_data'].browseUserLevel=2 # Browse only visible for expert user
    eNode.blank_division.signature['bkd_data'].databaseUserLevel=2 # Database only visible for expert user

    self.addLink( 'average_file','data',self.initValuesAverage) # Change on average_file if change on data
    eNode.addLink( 'blank_subtraction.data','data' ) # Link between blank_subtraction process' data and pipeline's data
    eNode.addLink( 'blank_division.data','data' ) # Link between blank_division process' data and pipeline's data

    eNode.addLink( 'data','blank_subtraction.data' ) # Link between pipeline's data and blank_subtraction process' data
    eNode.addLink( 'data','blank_division.data' ) # Link between pipeline's data and blank_division process' data

    if eNode.blank_subtraction.isSelected(): # If blank_subtraction is selected
        eNode.addLink('bksd_data','blank_subtraction.bks_data' ) # Link between pipeline's bksd_data and blank_subtraction process' bks_data

    else: # If blank_division is selected
        eNode.addLink('bksd_data','blank_division.bkd_data' ) # Link between pipeline's bksd_data and blank_division process' bkd_data
        
    eNode.blank_subtraction._selectionChange.add( self.selected ) # Add a track of change on selection

    eNode.addLink( 'blank_subtraction.average_file','average_file') # Link between blank_subtraction process' average and pipeline's average_file
    eNode.addLink( 'blank_division.average_file','average_file' ) # Link between blank_division process' average and pipeline's average_file
    
    self.setExecutionNode( eNode ) # Pipeline creation
