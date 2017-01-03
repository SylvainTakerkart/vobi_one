# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Displays the averaged region of interest time series, created using average_region process

from neuroProcesses import *

name=_t_('Viewer Averaged Region')
category=_t_('Viewers')
roles=('viewer',)
userLevel=0 # Always visible

import visu_plot
import pickle
import numpy as np
import os

# The parameters
signature = Signature(
	'input', ReadDiskItem( 'OI Time Series' , 'Text file' ), # The path of the time series (a txt file)
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
	X=np.loadtxt(self.input.fullPath()) # Loads time series from file

	view = mainThreadActions().call(visu_plot.PlotModel,(X,)) # New thread creation and call to plot vizualizer
	mainThreadActions().push( view.show ) # Displaying new window
	return view
