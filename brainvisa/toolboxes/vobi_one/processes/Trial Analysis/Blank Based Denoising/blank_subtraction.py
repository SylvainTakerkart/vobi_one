# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# The blank subtraction. Subtracts the averaged blank datas to image

from neuroProcesses import *
from oi_formats import list_formats
import os

name = _t_('Blank Subtraction')
category = _t_('Blank Based Denoising')
userLevel=1 # Not visible for basic user

def validation( self ):
    """Check if imports are possible ans raises errors if not
    """
    try:
        import oidata.oitrial_processes
    except ImportError:
        raise ValidationError(_t_('Impossible to import oidata.oitrial_processes')) # Raises an exception

# The parameters
signature=Signature(
    "format", apply( Choice,[('<auto>',None)] + map( lambda x: (x,getFormat(x)), list_formats ) ), # Saving format of images. It can be NIFTI-1 Image ('.nii') or gzip compressed NIFTI-1 Image ('.nii.gz')
    "firstlevel_analysis", WriteDiskItem( 'Secondlevel Blank Directory','Directory' ), # Trial-level directory
    "data", ReadDiskItem( 'OI 2D+t Image' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # Input image path
    "average_file", ReadDiskItem( 'OI 2D+t Blank Mean' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The averaged raw image
    "bks_data", WriteDiskItem( 'OI BkSD' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The path of the image after blank subtraction
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

    return value
  
def initValuesbksd( self , inp ):
    """Output file autocompletion

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    value = {} # Value dictionary initialization
    if self.data is not None:
        # Key value autocompletion
        value=self.data.hierarchyAttributes()
        value['filename_variable']= os.path.splitext(os.path.splitext(os.path.basename( self.data.fullPath() ))[0])[0]+ '_bks'

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
   
def initialization( self ):
    """Parameters values initialization
    """
    # Optional parameters
    self.setOptional( 'format' )
    self.setOptional( 'firstlevel_analysis' )

    self.signature["firstlevel_analysis"].browseUserLevel=3 # Browse never visible
    self.signature["data"].browseUserLevel = 2 # Browse only visible for expert user
    self.signature["average_file"].browseUserLevel = 2 # Browse only visible for expert user
    self.signature["bks_data"].browseUserLevel = 2 # Browse only visible for expert user

    self.addLink( "average_file", "data",self.initValuesAverage) # Change on average_file if change on data

    self.addLink( "bks_data", "format", self.initValuesbksd) # Change on bks_data if change on format
    self.addLink( "bks_data", "firstlevel_analysis", self.initValuesbksd) # Change on bks_data if change on firstlevel_analysis
    self.addLink( "bks_data", "data", self.initValuesbksd) # Change on bks_data if change on data

def execution( self,context ):
    """The execution process
    
    Parameters
    ----------
    context : BrainVISA context
    import oidata.oitrial_processes as oitrial_processes
    """
    import oidata.oitrial_processes as oitrial_processes

    attributes = self.bks_data.hierarchyAttributes() # Attributes recuperation

    format =  os.path.splitext(os.path.splitext(self.bks_data.fullPath())[0])[1]+os.path.splitext(self.bks_data.fullPath())[1] # Format recuperation

    # The blank subtraction. Subtracts the averaged blank datas to image
    oitrial_processes.blank_subtraction_process(
	path_data=self.data.fullPath(), # Data file path
        path_average=self.average_file.fullPath(), # The averaged raw image
	path_bksd=self.bks_data.fullPath(), # The path of the image after blank subtraction
	database=attributes["_database"],
	protocol=attributes["protocol"],
	subject=attributes["subject"],
	session='session_'+attributes["session_date"],
	exp='exp'+attributes["experience_number"],
	trial='trial'+attributes["trial_number"],
	analysis='blank_based'+attributes["firstlevel_analysis"],
        format=format,
	mode=True, # The database mode
	context=context ) # BrainVISA context
