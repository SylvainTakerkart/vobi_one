# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# NIFTI visualization with Anatomist
userLevel = 3 # Never visible

def create_Window( img ):
	"""Anatomist window creation

	Parameters
	----------
	img : numpy array
	    The image to display

	Returns
	-------
	image : Anatomist image object
	    The image displayed by Anatomist
	axial : Anatomist visualization object
	    The visualization window
	"""
	import anatomist.api as anat
	import os
	a=anat.Anatomist() # Anatomist instance initialization
	image=a.loadObject( os.path.join( img )) # Image Anatomist instance creation

	palette=a.getPalette("Blue-Green-Red-Yellow") # Setting colors
	image.setPalette(palette)

	axial=a.createWindow( "Axial" ) # Visualization window creation and setting the visualization plane
	axial.addObjects(image)

	return (image,axial)
