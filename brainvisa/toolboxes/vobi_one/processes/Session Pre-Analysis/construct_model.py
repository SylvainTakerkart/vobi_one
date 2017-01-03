# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Creates the matrix of regressors. Saves the linear model in a txt file and the parameters in a Numpy Dump File.

# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path
# In toolbox Vobi One
try:
    import manip_char
except ImportError:
    raise ValidationError(_t_('Impossible to import manip_char')) # Raises an exception
    
# Header    
name = _t_('Construct Model') # Process name in the GUI
category = _t_('Session Pre-Analysis') # Category name in the GUI
userLevel=0 # Always visible

# The parameters
signature = Signature(
    'parameters',ReadDiskItem( 'OI GLM Parameters', 'Numpy Dump file' ), # In case of the parameters are loaded from an existing file. It is the path of this file
    'sampling_frequency', Float(), # The sampling frequency
    'trial_duration', Float(), # The trial duration
    'tau', Float(), # The time constant of dye bleaching
    'frequencies', String(), # The frequencies of environmental and physiological noises (a list)
    'fourier_orders', String(), # The fourier orders of environmental and physiological noises (a list, must have the same lenght as point 3)
    'L', Integer(), # The number of regressors kept to create the Linear Model
    'alpha_min', String(), # The time-range parameters (minima)
    'alpha_max', String(), # The time-range parameters (maxima, must have the same lenght as point 6)
    'output', WriteDiskItem( 'OI GLM Design Matrix', 'Text file' ), # The path where is saved the model definition
    'parameters_file', WriteDiskItem( 'OI GLM Parameters', 'Numpy Dump file' ), # The path where are saved the parameters
)

def initParam( self, inp ):
    """Parameters autocompletion

    Parameters
    ----------
    inp : BrainVISA parameter type
         The parameter whose changes will be tracked to autocomplete the others
    """
    import pickle

    if self.parameters is not None:
        f=open(self.parameters.fullPath().encode("utf8"),'r') # Opening parameters_file
        param=pickle.load(f) # Parameters recuperation
        f.close() # Closing parameters_file*

        # Parameters initializing
        self.trial_duration=param[1]
        self.tau=param[2]
        self.frequencies=param[3]
        self.fourier_orders=param[4]    
        self.L=param[5]
        self.alpha_min=param[6]
        self.alpha_max=param[7]
        return param[0]

def initParametersFile( self, inp ):
    """Parameters_file autocompletion

    Parameters
    ----------
    inp : BrainVISA parameter type
         The parameter whose changes will be tracked to autocomplete the others
    """
    values={} # Value dictionary initialization

    if self.output is not None:
        # Key value autocompletion
        values=self.output.hierarchyAttributes()

    values['filename_variable' ] = 'param' # Key value autocompletion
    return values

def initOutput( self, inp ):
    """Output autocompletion

    Parameters
    ----------
    inp : BrainVISA parameter type
         The parameter whose changes will be tracked to autocomplete the others
    """
    values={} # Value dictionary initialization

    if self.parameters_file is not None:
         # Key value autocompletion
        values=self.parameters_file.hierarchyAttributes()

    values['filename_variable' ] = 'glm' # Key value autocompletion
    return values

def initialization( self ):
    """Parameters values initialization
    """
    # Optional parameters
    self.setOptional( 'parameters' )

    self.signature["parameters_file"].browseUserLevel = 2 # Browse only visible for expert user
    self.signature["output"].browseUserLevel = 2 # Browse only visible for expert user

    # Links
    self.addLink( "sampling_frequency", "parameters", self.initParam ) # Change of sampling_frequency if change on parameters

    self.addLink( "output","parameters_file", self.initOutput ) # Change of output if change on parameters_file
    self.addLink( "parameters_file", "output", self.initParametersFile ) # Change of parameters_file if change on output
   
    # Parameters initialization
    self.frequencies='( , , , , )'
    self.fourier_orders='( , , , , )'
    self.alpha_min='( , , , , , , , )'
    self.alpha_max='( , , , , , , , )'
   
def execution( self, context ):
    """The execution process

    Parameters
    ----------
    context : BrainVISA context
    """
    import oidata.oisession_preprocesses as oisession_preprocesses
          
    # Lists completion evaluation and correction
    self.frequencies=manip_char.standardize(self.frequencies)
    self.fourier_orders=manip_char.standardize(self.fourier_orders)
    self.alpha_min=manip_char.standardize(self.alpha_min)
    self.alpha_max=manip_char.standardize(self.alpha_max)

    try:
        if len(eval(self.frequencies)) is not len(eval(self.fourier_orders)):
            context.error(_t_('frequencies and fourier_orders must have the same length')) # Verification of frequencies and fourier orders length
            return

        if len(eval(self.alpha_max))!=8 or len(eval(self.alpha_min))!=8:
            context.error(_t_('Alpha must contain 8 values')) # Verification of alpha_min and alpha_max length
            return
    except:
        context.error(_t_('At least one of the vector parameters has not the expected form')) # Verification of lists completion
        return

    

    attributes = self.output.hierarchyAttributes() # Attributes recuperation
    analysis = 'glm_based' + attributes["secondlevel_analysis"] # Analysis recuperation

# Creation of the matrix of regressors. Saves the linear model in a txt file and the parameters in a Numpy Dump File.
    oisession_preprocesses.construct_model_process(
        database=attributes["_database"],
        protocol=attributes["protocol"],
        subject=attributes["subject"],
        session='session_'+attributes["session_date"],
        param=(self.sampling_frequency,
         self.trial_duration,
         self.tau,
         self.frequencies,
         self.fourier_orders,
         self.L,
         self.alpha_min,
         self.alpha_max),
        pathX=self.output.fullPath(),
        pathParam=self.parameters_file.fullPath(),
        analysis=analysis,
        mode=True, # The database mode
        context=context ) # BrainVISA context
