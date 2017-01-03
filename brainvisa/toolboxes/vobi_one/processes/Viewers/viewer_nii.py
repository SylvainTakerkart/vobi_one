# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Diplays NIFTI-1 and gz compressed NIFTI-1 images using anatomist.

from neuroProcesses import *

import visu_nii

name=_t_('Viewer NIfTI Image')
category=_t_('Viewers')
roles=('viewer',)
userLevel=0 # Always visible

# The parameters
signature = Signature(
	"input", ReadDiskItem( 'OI 2D+t Image' , ['NIFTI-1 image', 'gz compressed NIFTI-1 image'] ), # NIFTI-1 or gz compressed NIFTI-1 input image file name
)

def initialization( self ):
	"""Parameters values initialization
	"""
	self.signature["input"].browseUserLevel = 1 # Browse not visible for basic user

def execution ( self,context ):
	"""The execution process

	Parameters
	----------
	context : BrainVISA context
	"""

	# NIFTI visualization with Anatomist
	view = visu_nii.create_Window(self.input.fullPath() )
	
	return view # launch Anatomist Window
