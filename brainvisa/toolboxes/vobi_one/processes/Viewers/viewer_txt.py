# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Displays the conditions file, created using condition_file process.

from neuroProcesses import *

name=_t_('Viewer Text File')
category=_t_('Viewers')
roles=('viewer',)
userLevel=0 # Always visible

import visu_txt
import numpy as np

# The parameters
signature = Signature(
	'input', ReadDiskItem( 'Trials+conditions list' , 'Text file' ), # The condition file path
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
	
	raw_name,experiences,trials,conditions,selected=np.loadtxt(self.input.fullPath(),delimiter='\t', unpack=True,dtype=str) # Extraction of conditions_file informations :
	        # 1. Filename
                # 2. Experience
                # 3. Trial
                # 4. Condition
	        # 5. Selected (if file is selected or not)

	conditions=np.vstack((raw_name,experiences,trials,conditions,selected))
	view = mainThreadActions().call(visu_txt.WidgetModel,conditions) # New thread creation and call to txt vizualizer
	mainThreadActions().push( view.show ) # Displaying new window
	return view
