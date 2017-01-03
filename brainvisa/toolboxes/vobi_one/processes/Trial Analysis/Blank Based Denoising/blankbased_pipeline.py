# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Pipeline containings the whole BkSD processes :
    # Frame0-based processes
        # frame0_division
        # frame0_division
        # linear_detrend
    # Blank-based processes
        # blank_subtraction
        # blank_division

from neuroProcesses import *
from oi_formats import list_formats
import os

name=_t_('Blank Based Pipeline')
category = _t_('Blank Based Denoising')
userLevel=0 # Always visible

# Parameters
signature=Signature(
    "format", apply( Choice,[('<auto>',None)] + map( lambda x: (x,getFormat(x)), list_formats ) ), # Saving format of images. It can be NIFTI-1 Image ('.nii') or gzip compressed NIFTI-1 Image ('.nii.gz')
    "firstlevel_analysis", WriteDiskItem( 'Secondlevel Blank Directory','Directory' ), # Trial-level directory
    "input", ReadDiskItem( 'OI 2D+t Image' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The input image file name
    "frame0", String(), # The datas at the begin of a time serie used to detrend the global time serie (time1,time2)
    "frame1", String(),# The datas at the end of a time serie used to detrend the global time serie (time1,time2)
    "average_file", ReadDiskItem('OI 2D+t Blank Mean' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The averaged raw image
    "output", WriteDiskItem( 'OI 2D+t Image' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),  # Output image after BkSD denoising
)

def initValuesf0Subtraction( self , inp ):
    """F0 subtraction parameters initialization

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    value = {} # Value dictionary initialization
    if self._executionNode.frame0_pipe.data is not None: # If f0_pipe's data (selection pipeline) is None
        # Key value autocompletion
        value=self._executionNode.frame0_pipe.data.hierarchyAttributes()
        value['filename_variable']= os.path.splitext(os.path.splitext(os.path.basename( self._executionNode.frame0_pipe.data.fullPath() ))[0])[0]+ '_f0s'

    if self.firstlevel_analysis is not None:
        # Key value autocompletion
        value['firstlevel_analysis']=self.firstlevel_analysis.hierarchyAttributes()['secondlevel_analysis']

        
    if self.format is not None:
        result=WriteDiskItem( 'OI BkSD', self.format ).findValue( value )

    else:
        result=WriteDiskItem( 'OI BkSD', 'NIFTI-1 image' ).findValue( value ) # Check list_formats in oiformats.py

    if self.frame0 != '[,]':
        self._executionNode.frame0_pipe.frame0=self.frame0
        
    if result is not None:
        return result # While opening process, result is not created
    else:
        return value

def initValuesf0Division( self , inp ):
    """F0 division parameters initialization

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    value = {} # Value dictionary initialization
    if self._executionNode.frame0_pipe.data is not None: # If f0_pipe's data (selection pipeline) is None
        # Key value autocompletion
        value=self._executionNode.frame0_pipe.data.hierarchyAttributes()
        value['filename_variable']= os.path.splitext(os.path.splitext(os.path.basename( self._executionNode.frame0_pipe.data.fullPath() ))[0])[0]+ '_f0d'

    if self.firstlevel_analysis is not None:
        # Key value autocompletion
        value['firstlevel_analysis']=self.firstlevel_analysis.hierarchyAttributes()['secondlevel_analysis']

    if self.format is not None:
        result=WriteDiskItem( 'OI BkSD', self.format ).findValue( value )

    else:
        result=WriteDiskItem( 'OI BkSD', 'NIFTI-1 image' ).findValue( value ) # Check list_formats in oiformats.py
    
    if self.frame0 != '[,]':
        self._executionNode.frame0_pipe.frame0=self.frame0
        
    if result is not None:
        return result # While opening process, result is not created
    else:
        return value

def initValuesBlankSubtraction( self , inp ):
    """Blank subtraction parameters initialization

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    value = {} # Value dictionary initialization
    if self._executionNode.blank_pipe.data is not None: # If blank_pipe's data (selection pipeline) is None
        # Key value autocompletion
        value=self._executionNode.blank_pipe.data.hierarchyAttributes()
        value['filename_variable']= os.path.splitext(os.path.splitext(os.path.basename( self._executionNode.blank_pipe.data.fullPath() ))[0])[0]+ '_bks'

    if self.firstlevel_analysis is not None:
        # Key value autocompletion
        value['firstlevel_analysis']=self.firstlevel_analysis.hierarchyAttributes()['secondlevel_analysis']

    if self.format is not None:
        result=WriteDiskItem( 'OI BkSD', self.format ).findValue( value )

    else:
        result=WriteDiskItem( 'OI BkSD', 'NIFTI-1 image' ).findValue( value ) # Check list_formats in oiformats.py

    if result is not None:
        return result # While opening process, result is not created
    else:
        return value

def initValuesBlankDivision( self , inp ):
    """Blank division parameters initialization

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    value = {} # Value dictionary initialization
    if self._executionNode.blank_pipe.data is not None: # If blank_pipe's data (selection pipeline) is None
        # Key value autocompletion
        value=self._executionNode.blank_pipe.data.hierarchyAttributes()
        value['filename_variable']= os.path.splitext(os.path.splitext(os.path.basename( self._executionNode.blank_pipe.data.fullPath() ))[0])[0]+ '_bkd'

    if self.firstlevel_analysis is not None:
        # Key value autocompletion
        value['firstlevel_analysis']=self.firstlevel_analysis.hierarchyAttributes()['secondlevel_analysis']

    if self.format is not None:
        result=WriteDiskItem( 'OI BkSD', self.format ).findValue( value )

    else:
        result=WriteDiskItem( 'OI BkSD', 'NIFTI-1 image' ).findValue( value ) # Check list_formats in oiformats.py

    if result is not None:
        return result # While opening process, result is not created
    else:
        return value

def initValuesAverage( self,inp ):
    """Averaged file autocompletion

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    value = {} # Value dictionary initialization
    if self._executionNode.average_file is not None:
        # Key value autocompletion
        value=self._executionNode.average_file.hierarchyAttributes()

    return value

def initValuesLinearDetrend( self,inp ):
    """Linear detrend parameters initialization

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    value = {} # Value dictionary initialization
    if self._executionNode.linear_detrend.data is not None: # If linear_detrend's data process is None
        # Key value autocompletion
        value=self._executionNode.linear_detrend.data.hierarchyAttributes()
        value['filename_variable']= os.path.splitext(os.path.splitext(os.path.basename( self._executionNode.linear_detrend.data.fullPath() ))[0])[0]+ '_d'

    if self.firstlevel_analysis is not None:
        # Key value autocompletion
        value['firstlevel_analysis']=self.firstlevel_analysis.hierarchyAttributes()['secondlevel_analysis']

    if self.format is not None:
        result=WriteDiskItem( 'OI BkSD', self.format ).findValue( value )

    else:
        result=WriteDiskItem( 'OI BkSD', 'NIFTI-1 image' ).findValue( value ) # Check list_formats in oiformats.py
    
    if self.frame0 != '[,]':
        self._executionNode.linear_detrend.frame0=self.frame0
    if self.frame1 != '[,]':
        self._executionNode.linear_detrend.frame1=self.frame1
    if result is not None:
        return result # While opening process, result is not created
    else:
        return value

def initInput( self, subproc ):
    """Input file autocompletion

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    if self._executionNode.frame0_pipe.isSelected(): # If frame0_pipe (selection pipeline) is selected
        self._executionNode.frame0_pipe.data = self.input # Initialization of frame0_pipe's data with pipeline's input
        self._executionNode.blank_pipe.data=self._executionNode.frame0_pipe.f0_data # Initialization of blank_pipe's data with frame0_pipe's f0_data
        
        self._executionNode.addLink('frame0_pipe.data','input') # Link between pipeline's input and frame0_pipe's data
        self._executionNode.addLink('blank_pipe.data','frame0_pipe.f0_data') # Link between  frame0_pipe's f0_data and blank_pipe's data
        
    elif self._executionNode.blank_pipe.isSelected(): # If blank_pipe (selection pipeline) is selected
        self._executionNode.blank_pipe.data = self.input # Initialization of blank_pipe's data with pipeline's input
        self._executionNode.linear_detrend.data=self._executionNode.blank_pipe.bksd_data # Initialization of linear_detrend's data with blank_pipe's bksd_data
        
        self._executionNode.addLink('blank_pipe.data','input') # Link between pipeline's input and blank_pipe's data
        self._executionNode.addLink('linear_detrend.data','blank_pipe.bksd_data') # Link between linear_detrend's data and blank_pipe's bksd_data

        try:
            self._executionNode.removeLink('frame0_pipe.data','input') # Remove link between pipeline's input and frame0_pipe's data
        except:
            pass

        try:
            self._executionNode.removeLink('blank_pipe.data','frame0_pipe.f0_data') # Remove link between frame0_pipe's f0_data and blank_pipe's data
        except:
            pass
            
    elif self._executionNode.linear_detrend.isSelected(): # If linear_detrend process is selected
        self._executionNode.linear_detrend.data=self.input # Initialization of linear_detrend's data with pipelines' input
        self._executionNode.addLink('linear_detrend.data','input') # Link between pipeline's input and linear_detrend's data

        try:
            self._executionNode.removeLink('blank_pipe.data','input') # Remove link between pipeline's input and linear_detrend's data
        except:
            pass  

def initOutput( self,subproc ):
    """Output file autocompletion

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    if self._executionNode.linear_detrend.isSelected(): # If linear_detrend process is selected
        self.output=self._executionNode.linear_detrend.detrend_data # Initialization of pipeline's output with linear_detrend's detrend_data
        self._executionNode.addLink('output','linear_detrend.detrend_data') # Link between linear_detrend's detrend_data and pipeline's output

    elif self._executionNode.blank_pipe.isSelected(): # If blank_pipe (selection pipeline) is selected
        self.output=self._executionNode.blank_pipe.bksd_data # Initialization of pipeline's output with blank_pipe's bksd_data
        self._executionNode.addLink('output','blank_pipe.bksd_data') # Link between blank_pipe's bksd_data and pipeline's output

        try:
            self._executionNode.removeLink('output','linear_detrend.detrend_data') # Remove link between linear_detrend's detrend_data and pipeline's output
        except:
            pass

        try:
            self._executionNode.removeLink('linear_detrend.data','blank_pipe.bksd_data') # Remove link between blank_pipe's bksd_data and linear_detrend's data
        except:
            pass

    elif self._executionNode.frame0_pipe.isSelected(): # If frame0_pipe (selection pipeline) is selected
        self.output=self._executionNode.frame0_pipe.f0_data # Initialization of pipeline's output with frame0_pipe's f0_data
        self._executionNode.addLink('output','frame0_pipe.f0_data') # Link between frame0_pipe's f0_data and output pipeline

        try:
            self._executionNode.removeLink('output','blank_pipe.bksd_data') # Remove link between blank_pipe's bksd_data and output pipeline
        except:
            pass

        try:
            self._executionNode.removeLink('blank_pipe.data','frame0_pipe.f0_data') # Remove link between frame0_pipe's f0_data and blank_pipe's bksd_data
        except:
            pass

def blankIsSelected( self, subproc ):
    """Controls the selection between processes

    Parameters
    ----------
    subroc : bool
        The choice box value
    """
    if self._executionNode.blank_pipe.isSelected()==False: # If blank_pipe (selection pipeline) is selected
        try:
            self._executionNode.removeLink('blank_pipe.data','frame0_pipe.f0_data') # Remove link between frame0_pipe's f0_data and blank_pipe's bksd_data
        except:
            pass
                
        try:
            self._executionNode.removeLink('linear_detrend.data','blank_pipe.bksd_data') # Remove link between blank_pipe's bksd_data and linear_detrend's data
        except:
            pass
            

        if self._executionNode.linear_detrend.isSelected() and self._executionNode.frame0_pipe.isSelected(): # If linear_detrend process is selected
            self._executionNode.linear_detrend.data=self._executionNode.frame0_pipe.f0_data  # Initialization of linear_detrend's data with frame0_pipe's f0_data
            self._executionNode.addLink('linear_detrend.data','frame0_pipe.f0_data')

    else: # If blank_pipe (selection pipeline) is not selected
        try:
            self._executionNode.removeLink('linear_detrend.data','frame0_pipe.f0_data') # Remove link beween frame0_pipe's f0_data and linear_detrend's data
        except:
            pass
            
        if self._executionNode.frame0_pipe.isSelected(): # If frame0_pipe (selection pipeline) is selected
            self._executionNode.blank_pipe.data=self._executionNode.frame0_pipe.f0_data  # Initialization of blank_pipe's data with frame0_pipe's f0_data
            self._executionNode.addLink('blank_pipe.data','frame0_pipe.f0_data') # Link between frame0_pipe's f0_data and blank_pipe's bksd_data

        if self._executionNode.linear_detrend.isSelected(): # If linear_detrend process is selected
            self._executionNode.linear_detrend.data=self._executionNode.blank_pipe.bksd_data  # Initialization of linear_detrend's data with blank_pipe's bksd_data
            self._executionNode.addLink('linear_detrend.data','blank_pipe.bksd_data') # Link between blank_pipe's bksd_data and linear_detrend's data

def initialization( self ):
    """Parameters values initialization
    """
    # Optional parameters
    self.setOptional( 'format' )
    self.setOptional( 'firstlevel_analysis' )

    eNode = SerialExecutionNode( self.name, parameterized = self ) # Declaration of a new selection pipeline

    eNode.addChild( 'frame0_pipe',ProcessExecutionNode('frame0_pipe', optional = True ) ) # Add frame0_pipe to pipeline
    eNode.addChild( 'blank_pipe',ProcessExecutionNode('blank_pipe', optional = True ) ) # Add blank_pipe to pipeline
    eNode.addChild( 'linear_detrend',ProcessExecutionNode('linear_detrend', optional = True ) ) # Add linear_detrend to pipeline
    self.signature["firstlevel_analysis"].browseUserLevel=3 # Browse never visible
    self.signature["input"].browseUserLevel=2 # Browse only visible for expert user
    self.signature["output"].browseUserLevel=2 # Browse only visible for expert user
    self.frame0='[,]'
    self.frame1='[,]'
    # Change of linear_detrend signature
    detrendSignature=["data", ReadDiskItem( 'OI 2D+t Image' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                      "frame0", String(),
                      "frame1", String(),
                      "detrend_data", WriteDiskItem( 'OI BkSD' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                      ]

    # Applies changes on signatures
    detrend=Signature( *detrendSignature )
    eNode.linear_detrend.changeSignature( detrend )

    eNode.linear_detrend.signature['data'].browseUserLevel=2 # Browse only visible for expert user
    eNode.linear_detrend.signature['detrend_data'].browseUserLevel=2 # Browse only visible for expert user

    # frame0_pipe links
    eNode.addLink('frame0_pipe.data','input') # Link between frame0_pipe's data and pipeline's input

    eNode.addLink( "frame0_pipe.frame0_subtraction.f0_data", "frame0_pipe.frame0_subtraction.data", self.initValuesf0Subtraction) # Link between frame0_subtraction's f0_data and frame0_subtraction's data
    eNode.addLink( "frame0_pipe.frame0_subtraction.f0_data", "format", self.initValuesf0Subtraction) # Link between frame0_subtraction's f0_data and frame0_subtraction's format
    eNode.addLink( "frame0_pipe.frame0_subtraction.f0_data", "firstlevel_analysis", self.initValuesf0Subtraction) # Link between frame0_subtraction's f0_data and pipeline's firstlevel_analysis
    eNode.addLink( "frame0_pipe.frame0_subtraction.f0_data", "frame0", self.initValuesf0Subtraction)
    
    eNode.addLink( "frame0_pipe.frame0_division.f0_data", "frame0_pipe.frame0_division.data", self.initValuesf0Division) # Link between frame0_division's f0_data and frame0_division's data
    eNode.addLink( "frame0_pipe.frame0_division.f0_data", "format", self.initValuesf0Division) # Link between frame0_division's f0_data and frame0_division's format
    eNode.addLink( "frame0_pipe.frame0_division.f0_data", "firstlevel_analysis", self.initValuesf0Division) # Link between frame0_division's f0_data and pipeline's firstlevel_analysis
    eNode.addLink( "frame0_pipe.frame0_division.f0_data", "frame0", self.initValuesf0Division)
    
    # blank_pipe links
    eNode.addLink( "blank_pipe.blank_subtraction.bks_data", "blank_pipe.blank_subtraction.data", self.initValuesBlankSubtraction) # Link between blank_subtraction's bks_data and blank_subtraction's data
    eNode.addLink( "blank_pipe.blank_subtraction.bks_data", "format", self.initValuesBlankSubtraction) # Link between blank_subtraction's bks_data and blank_subtraction's format
    eNode.addLink( "blank_pipe.blank_subtraction.bks_data", "firstlevel_analysis", self.initValuesBlankSubtraction) # Link between blank_subtraction's bks_data and pipeline's firstlevel_analysis

    eNode.addLink( "blank_pipe.blank_division.bkd_data", "blank_pipe.blank_division.data", self.initValuesBlankDivision) # Link between blank_division's bkd_data and blank_division's data
    eNode.addLink( "blank_pipe.blank_division.bkd_data", "format", self.initValuesBlankDivision) # Link between blank_division's bks_data and blank_division's format
    eNode.addLink( "blank_pipe.blank_division.bkd_data", "firstlevel_analysis", self.initValuesBlankDivision) # Link between blank_division's bks_data and pipeline's firstlevel_analysis

    # linear_detrend links
    eNode.addLink( "linear_detrend.detrend_data", "linear_detrend.data", self.initValuesLinearDetrend) # Link between linear_detrend's detrend_data and linear_detrend's data
    eNode.addLink( "linear_detrend.detrend_data", "format", self.initValuesLinearDetrend) # Link between linear_detrend's detrend_data and linear_detrend's format
    eNode.addLink( "linear_detrend.detrend_data", "firstlevel_analysis", self.initValuesLinearDetrend) # Link between linear_detrend's detrend_data and pipeline's firstlevel_analysis
    eNode.addLink( "linear_detrend.detrend_data", "frame0", self.initValuesLinearDetrend) # Link between linear_detrend's detrend_data and pipeline's frame0
    eNode.addLink( "linear_detrend.detrend_data", "frame1", self.initValuesLinearDetrend) # Link between linear_detrend's detrend_data and pipeline's frame1
    
    # links between pipes
    eNode.addLink('blank_pipe.data','frame0_pipe.f0_data') # Link between blank_pipe's data and frame0_pipe's data
    eNode.addLink('blank_pipe.average_file','average_file',self.initValuesAverage)# Link between blank_pipe's average file and input data
    eNode.addLink('linear_detrend.data','blank_pipe.bksd_data') # Link between linear_detrend's data and blank_pipe's bksd_data
    eNode.addLink('output','linear_detrend.detrend_data') # Link between pipeline's output and linear_detrend's data

    # Add a track of changes on selection
    eNode.frame0_pipe._selectionChange.add( self.initInput ) 
    eNode.blank_pipe._selectionChange.add( self.initInput )
    eNode.linear_detrend._selectionChange.add( self.initInput )

    eNode.blank_pipe._selectionChange.add( self.blankIsSelected )

    eNode.linear_detrend._selectionChange.add( self.initOutput )
    eNode.blank_pipe._selectionChange.add( self.initOutput )
    eNode.frame0_pipe._selectionChange.add( self.initOutput )
    self.setExecutionNode( eNode ) # Pipeline creation
