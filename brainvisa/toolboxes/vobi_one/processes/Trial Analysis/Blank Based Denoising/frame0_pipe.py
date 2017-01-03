# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Frame0_pipe. This pipeline is a component of blankbased_pipeline. It is used to choice in GUI between frame0_division and frame0_subtraction.
# Makes the link between blankbased_pipeline and those processes.

from neuroProcesses import *

name=_t_('Frame0 Pipe')
category = _t_('Blank Based Denoising')
userLevel=3 # Never visible

# Parameters
signature=Signature(
    "data", ReadDiskItem( 'OI 2D+t Image' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # Input image path
    "frame0", String(), # The datas of a time serie used to subtract the global time serie (time1,time2)
    "f0_data", WriteDiskItem( 'OI BkSD' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
) # The path of the image after frame0 subtraction
    
def selected( self,subproc ):
    """Controls the selection between the two process

    Parameters
    ----------
    subroc : bool
        The choice box value
    """
    if subproc._selected: # If frame0_subtraction is selected
        self.f0_data=self._executionNode.frame0_subtraction.f0_data # Initialization of pipeline's f0_data with frame0_subtraction process's f0_data
        self.frame0=self._executionNode.frame0_subtraction.frame0 # Initialization of pipeline's frame0 with frame0_subtraction process' f0_data
        self._executionNode.addLink('f0_data','frame0_subtraction.f0_data' ) # Link between pipeline's f0_data and frame0_subtraction process' frame0
        self._executionNode.removeLink( 'f0_data','frame0_division.f0_data' ) # Remove link between pipeline's f0_data and frame0_division process' frame0

    else: # If frame0_division is selected
        self.f0_data=self._executionNode.frame0_division.f0_data # Initialization of pipeline's f0_data with frame0_division process' f0_data
        self.frame0=self._executionNode.frame0_division.frame0 # Initialization of pipeline's frame0 with frame0_division process' f0_data
        self._executionNode.addLink('f0_data','frame0_division.f0_data' ) # Link between pipeline's f0_data and frame0_division process' frame0
        self._executionNode.removeLink('f0_data','frame0_subtraction.f0_data' )# Remove link between pipeline's f0_data and frame0_subtraction process' frame0

def initialization( self ):
    """Parameters values initialization
    """
    self.frame0='[,]' # frame0 initialization

    eNode = SelectionExecutionNode( self.name, parameterized = self ) # Declaration of a new selection pipeline
    eNode.addChild( 'frame0_subtraction',ProcessExecutionNode('frame0_subtraction', optional = 1 ) ) # Add frame0_subtraction to pipeline
    eNode.addChild( 'frame0_division',ProcessExecutionNode('frame0_division', optional = 1 ))  # Add frame0_division to pipeline

    # Change of frame0_subtraction signature
    f0sSignature=[ "data", ReadDiskItem( 'OI 2D+t Image' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                   "frame0", String(),
                   "f0_data", WriteDiskItem( 'OI BkSD' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                   ]

    # Change of frame0_division signature
    f0dSignature=[ "data", ReadDiskItem( 'OI 2D+t Image' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                   "frame0", String(),
                   "f0_data", WriteDiskItem( 'OI BkSD' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                   ]
    
    # Applies changes on signatures
    f0s=Signature( *f0sSignature )
    eNode.frame0_subtraction.changeSignature( f0s )
    f0d=Signature( *f0dSignature )
    eNode.frame0_division.changeSignature( f0d )

    self.signature['data'].browseUserLevel=2 # Browse only visible for expert user
    self.signature['f0_data'].browseUserLevel=2 # Browse only visible for expert user

    eNode.frame0_subtraction.signature['data'].browseUserLevel=3 # Browse never visible
    eNode.frame0_subtraction.signature['data'].databaseUserLevel=3 # Database never visible
    eNode.frame0_division.signature['data'].browseUserLevel=3 # Browse never visible
    eNode.frame0_division.signature['data'].databaseUserLevel=3 # Database never visible

    eNode.frame0_subtraction.signature['f0_data'].browseUserLevel=2 # Browse only visible for expert user
    eNode.frame0_subtraction.signature['f0_data'].databaseUserLevel=2 # Database only visible for expert user
    eNode.frame0_division.signature['f0_data'].browseUserLevel=2 # Browse only visible for expert user
    eNode.frame0_division.signature['f0_data'].databaseUserLevel=2 # Database only visible for expert user

    eNode.addLink( 'frame0_subtraction.data','data' ) # Link between frame0_subtraction process' data and pipeline's data
    eNode.addLink( 'frame0_division.data','data' ) # Link between data frame0_division process and data pipeline

    eNode.addLink( 'data','frame0_subtraction.data' ) # Link between pipeline's data and frame0_subtraction process' data
    eNode.addLink( 'data','frame0_division.data' ) # Link between pipeline's data and frame0_division process' data

    # Initialization of pipeline
    if eNode.frame0_subtraction.isSelected(): # If frame0_subtraction is selected
        eNode.addLink('f0_data','frame0_subtraction.f0_data' ) # Link between pipeline's f0_data and frame0_division process' f0_data

    else: # If frame0_division is selected
        eNode.addLink('f0_data','frame0_division.f0_data' ) # Link between pipeline's f0_data and frame0_division process' f0_data

    eNode.frame0_subtraction._selectionChange.add( self.selected ) # Add a track of change on selection

    eNode.addLink( 'frame0_subtraction.frame0','frame0') # Link between frame0_subtraction process' frame0 and pipeline's frame0
    eNode.addLink( 'frame0_division.frame0','frame0' )  # Link between frame0_division process' frame0 and pipeline's frame0

    self.setExecutionNode( eNode ) # Pipeline creation
