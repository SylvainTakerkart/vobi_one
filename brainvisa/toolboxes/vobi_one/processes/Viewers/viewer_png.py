# Author: Flavien Garcia <flavien.garcia@free.fr>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Displays the PNG image in a Qt window.

# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path
import visu_png # Needed to displays image

# Header
name=_t_('Viewer PNG image') # Viewer name in the GUI
category=_t_('Viewer') # Category name in the GUI
roles=('viewer',) # Role in the toolbox
userLevel=0 # Always visible

# The parameters
signature = Signature(
    'input', ReadDiskItem( 'OI Data Graph' , 'PNG image' ), # The data graph path
    )

def initialization( self ):
    """Parameters values initialization
    """
    self.signature["input"].browseUserLevel = 1 # Browse not visible for basic user

def execution(self, context) :
    """The execution process

    Parameters
    ----------
    context : BrainVISA context
    """
    view = mainThreadActions().call(visu_png.DataGraphModel,self.input.fullPath().encode('utf8')) # New thread creation and call to png vizualizer    
    mainThreadActions().push(view.show) # Displaying new window
    return view


