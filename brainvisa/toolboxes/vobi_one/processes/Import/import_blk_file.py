# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# This process converts the BLK file created by VSDI imaging acquisition system to a NIFTI-1 file and import it in BrainVISA database.

# Imports
from neuroProcesses import *
# In BrainVISA library
try:
    import os
except ImportError:
    raise ValidationError(_t_('Impossible to import os')) # Raises an exception
# In toolbox Vobi One
from oi_formats import list_formats

# Header
name=_t_('Import BLK File') # Process name in the GUI
categorie=_t_('Import') # Category name in the GUI
userLevel=0 # Always visible
roles = ('importer',)

# The parameters
signature=Signature(
	"input", ReadDiskItem( 'OI BLK Camera File' , 'BLK Camera file' ), # BLK file name
	"subject", WriteDiskItem( 'Subject','Directory' ), # The subject's directory
	"format", apply( Choice,[('<auto>',None)] + map( lambda x: (x,getFormat(x)), list_formats ) ), # Saving format of images. It can be NIFTI-1 Image ('.nii') or gzip compressed NIFTI-1 Image ('.nii.gz')
	"period", Float(), # The acquisition period
	"temporal_binning", Integer(), # Time averaging
	"spatial_binning", Integer(), # Size of spatial window averaging
	"output", WriteDiskItem( 'OI Raw Imported Data' , list_formats ), # Output NIFTI-1 or gz compressed NIFTI-1 file name
)

def initValues( self, inp ):
	"""Parameters values autocompletion

	Parameters
	----------
	inp : BrainVISA parameter type
	     The parameter whose changes will be tracked to autocomplete the others
	"""
	value = {} # Value dictionary initialization

	if self.subject is not None:
		# Key value autocompletion
		value['_database']=self.subject.hierarchyAttributes()['_database']
		value['protocol']=self.subject.hierarchyAttributes()['protocol']
		value['subject']=self.subject.hierarchyAttributes()['subject']

	if self.input is not None:
		filename=os.path.splitext(os.path.basename(self.input.fullPath()))[0]

		# session_date was 20080327 and now is 080327
		# Key value autocompletion
		value['session_date']=filename[8:10] + filename[6:8] + filename[4:6]
		value['experience_number']=filename[18:20]
		# trial_number was 128, is now 0128 (ST change on 20110201)
		value['trial_number'] = '0' + filename[21:24]
		# output filename should now look like s080326_e01_t004_c00
		value['filename_variable']= 's' + value['session_date'] + '_e' + value['experience_number'] + '_t' + value['trial_number'] + '_c0' + filename[2:4]

	if self.format is not None:
		# Change of format
		result=WriteDiskItem( 'OI RAW Imported Data', self.format ).findValue( value ) # Use NIFTI-1 format

	else:
		result=WriteDiskItem( 'OI RAW Imported Data', 'NIFTI-1 image' ).findValue( value ) # Check on list_format in oi_formats.py and use the default value

	if result is not None:
		return result # While opening process, result is not created
	else:
		return value

def initialization( self ):
	"""Parameters values initialization
	"""

	# Optional parameters
	self.setOptional( 'subject' )
	self.setOptional( 'period' )
	self.setOptional( 'format' )
	self.setOptional( 'temporal_binning' )
	self.setOptional( 'spatial_binning' )

	self.format = None
	self.period = 0.009090909 # Default value for INT data
	self.temporal_binning = 1
	self.spatial_binning = 1

	self.signature[ 'subject' ].browseUserLevel=3 # Browse never visible
	self.signature[ 'output' ].browseUserLevel = 2 # Browse only visible for expert user
	self.signature[ 'input' ].databaseUserLevel = 3 # Database never visible

	# Links between parameters for autocompletion
	self.addLink( 'output', 'subject', self.initValues ) # Change of output if change on subject
	self.addLink( 'output', 'input', self.initValues ) # Change of output if change on input
	self.addLink( 'output', 'format' , self.initValues ) # Change of output if change on format

def execution( self,context ):
	"""The execution process

	Parameters
	----------
	context : BrainVISA context
	"""
	import oidata.oitrial_processes as oitrial_processes

	if self.period is not None:
		period = self.period
	else:
		period = 1.0

	attributes = self.output.hierarchyAttributes() # Attributes recuperation

	format =  os.path.splitext(os.path.splitext(self.output.fullPath())[0])[1]+os.path.splitext(self.output.fullPath())[1] # Format recuperation

	# Importation of a data file, containing the raw image
	# Image saved as NIFTI-1 image or gz compressed NIFTI-1 image.
	oitrial_processes.import_external_data_process(
		input = self.input.fullPath(), # Input file path
		output = self.output.fullPath(), # Output file path
		period = period,
		database = attributes["_database"],
		protocol = attributes["protocol"],
		subject = attributes["subject"],
		format = format,
		mode = True, # The database mode
		temporal_binning = self.temporal_binning,
		spatial_binning = self.spatial_binning,
		context = context) # BrainVISA context
