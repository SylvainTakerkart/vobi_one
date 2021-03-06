# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

from neuroProcesses import *
from oi_formats import list_formats
import os

# The linear detrending. Divides the whole time series by an affine function

name = _t_('Linear Detrend')
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
    "data", ReadDiskItem( 'OI 2D+t Image' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The input image
    "frame0", String(), # The datas at the begin of a time serie used to detrend the global time serie (time1,time2)
    "frame1", String(), # The datas at the end of a time serie used to detrend the global time serie (time1,time2)
    "detrend_data", WriteDiskItem( 'OI BkSD' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The path of the image after linear detrend
    )

def initValuesDetrend( self , inp ):
    """Parameters autocompletion

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    value = {} # Value dictionary initialization
    if self.data is not None:
        # Key value autocompletion
        value=self.data.hierarchyAttributes()
        value['filename_variable']= os.path.splitext(os.path.splitext(os.path.basename( self.data.fullPath() ))[0])[0]+ '_d'

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
    self.signature["detrend_data"].browseUserLevel = 2 # Browse only visible for expert user

    self.addLink( "detrend_data", "data", self.initValuesDetrend) # Change on detrend_data if change on data
    self.addLink( "detrend_data", "format", self.initValuesDetrend) # Change on detrend_data if change on format
    self.addLink( "detrend_data", "firstlevel_analysis", self.initValuesDetrend) # Change on detrend_data if change on firstlevel_analysis

    self.frame0='[,]' # frame0 initialization
    self.frame1='[,]' # frame1 initialization

def execution( self,context ):
    """The execution process
    
    Parameters
    ----------
    context : BrainVISA context
        import oidata.oitrial_processes as oitrial_processes
    """
    import oidata.oitrial_processes as oitrial_processes

    attributes = self.detrend_data.hierarchyAttributes() # Attributes recuperation

    format =  os.path.splitext(os.path.splitext(self.detrend_data.fullPath())[0])[1]+os.path.splitext(self.detrend_data.fullPath())[1] # Format recuperation

    # The linear detrending. Divides the whole time series by an affine function
    oitrial_processes.linear_detrend_process(
        eval(self.frame0), # The frame0s
        eval(self.frame1), # The frame1s
        self.data.fullPath(), # Data file path
        self.detrend_data.fullPath(), # detrend_data file path
        attributes["_database"],
        attributes["protocol"],
        attributes["subject"],
        'session_'+attributes["session_date"],
        'exp'+attributes["experience_number"],
        'trial'+attributes["trial_number"],
        'blank_based'+attributes["firstlevel_analysis"],
        format=format,
        mode=True, # The database mode
        context=context # BrainVISA context
        )
