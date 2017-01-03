# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# List of formats

userLevel=3 # Never visible

from brainvisa.data.neuroDiskItems import createFormatList
from brainvisa import shelltools

list_formats = createFormatList(
	'NIFTI formats',
	(
		'gz compressed NIFTI-1 image',
		'NIFTI-1 image',
		)
	)
