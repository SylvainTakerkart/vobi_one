# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Flavien garcia <flavien.garcia@free.fr>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Averages a region of interest from an averaged image created using average_trial process

# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path

# Header
name = _t_('Average Region')
category = _t_('Session Post-Analysis')
userLevel=0 # Always visible

# The parameters
signature=Signature(
    "input", ReadDiskItem( 'OI 2D+t Image' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The path of the image to average
    "ROI", Choice(('Rectangular ROI (from coordinates)','corners')\
                 ,('Binary mask (from image)','mask') ), # Way to average images. It can be with corners (Top left-hand and bottom right-hand) or with a mask (binary matrix)
    "corner0", String(), # The position of the top left-hand corner of the mask (x,y)
    "corner1", String(), # The position of the left-bottom corner of the mask (x,y)
    "input_mask", ReadDiskItem( 'OI Mask' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The path of an existing mask
    "output_mask", WriteDiskItem( 'OI Mask' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The path of the created mask
    "output", WriteDiskItem( 'OI Time Series', 'Text File' ), # 
    )

def initSignature( self,inp ):
    """Signature change and parameters initialization

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    if self.ROI == 'corners': # If user wants to average over a rectangular ROI
        self.input_mask=None
        # New signature
        paramSignature=["input", ReadDiskItem( 'OI 2D+t Image' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The path of the image to average
                        "ROI", Choice(('Rectangular ROI (from coordinates)','corners')\
                                     ,('Binary mask (from image)','mask') ), # Way to average images. It can be with corners (Top left-hand and bottom right-hand) or with a mask (binary matrix)
                        "corner0", String(), # The position of the top left-hand corner of the mask (x,y)
                        "corner1", String(), # The position of the left-bottom corner of the mask (x,y)
                        "output_mask", WriteDiskItem( 'OI Mask' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The path of the created mask
                        "output", WriteDiskItem( 'OI Time Series', 'Text File' ),
                        ]

        signature=Signature( *paramSignature )

        signature['input'].browseUserLevel=2 # Browse only visible for expert user
        signature['output_mask'].browseUserLevel=2 # Browse only visible for expert user
        signature['output'].browseUserLevel=2 # Browse only visible for expert user

        self.changeSignature( signature ) # Change of signature

        self.addLink( 'output_mask','corner0', self.initOutputMask ) # Change of output_mask if change on corner0
        self.addLink( 'output_mask','corner1', self.initOutputMask ) # Change of output_mask if change on corner1        
        self.addLink( 'output','corner0', self.initOutput ) # Change of output if change on corner0
        self.addLink( 'output','corner1', self.initOutput ) # Change of output if change on corner1
    else: # If user wants to average with a binary mask
        self.corner0='(,)'
        self.corner1='(,)'
        # New signature
        paramSignature=["input", ReadDiskItem( 'OI 2D+t Image' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                        "ROI", Choice(('Rectangular ROI (from coordinates)','corners')\
                                     ,('Binary mask (from image)','mask') ), # Way to average images. It can be with corners (Top left-hand and bottom right-hand) or with a mask (binary matrix)
                        "input_mask", ReadDiskItem( 'OI Mask' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                        "output", WriteDiskItem( 'OI Time Series', 'Text File' ),
                        ]

        signature=Signature( *paramSignature )

        signature['input'].browseUserLevel=2 # Browse only visible for expert user
        signature['input_mask'].browseUserLevel=2 # Browse only visible for expert user
        signature['output'].browseUserLevel=2 # Browse only visible for expert user
        
        self.changeSignature( signature ) # Change of signature
        self.addLink( 'output','input_mask', self.initOutput ) # Change of output if change on input_mask
        
def initOutputMask( self, inp ):
    """Output Mask autocompletion
    
    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    value={} # Value dictionary initialization
    if self.input is not None and self.corner0!='(,)' and self.corner1 != '(,)':
        # Key value autocompletion
        value=self.input.hierarchyAttributes()
        try:
            value['filename_variable']=str(eval(self.corner0)[0])+'_'+str(eval(self.corner0)[1])+'_'+str(eval(self.corner1)[0])+'_'+str(eval(self.corner1)[1])
        except:
            None
    return value

def initOutput( self, inp ):
    """Output autocompletion
    
    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    value=None # Value dictionary initialization
    result=None

    if self.input is not None:
        # Key value autocompletion
        value=self.input.hierarchyAttributes()
        if 'secondlevel_analysis' not in value.keys() and 'firstlevel_analysis' in value.keys():
            value['secondlevel_analysis']=value['firstlevel_analysis']
        value['filename_variable']=None
        if self.ROI=='corners' and self.corner0!='(,)' and self.corner1 != '(,)':
            try:
                value['filename_variable']=os.path.split(self.input.fullPath())[1][:-4]+'_mask_'+str(eval(self.corner0)[0])+'_'+str(eval(self.corner0)[1])+'_'+str(eval(self.corner1)[0])+'_'+str(eval(self.corner1)[1])
            except:
                None
        elif self.ROI=='mask' and self.input_mask is not None:
            # Key value autocompletion
            value['filename_variable']=os.path.split(self.input.fullPath())[1][:-4]+'_mask_'+self.input_mask.hierarchyAttributes()['filename_variable']

        if (os.path.split(os.path.split(self.input.fullPath())[0])[1])[0:9]=='glm_based':
            result=WriteDiskItem( 'OI GLM Time Series' , 'Text file' ).findValue( value )
        elif (os.path.split(os.path.split(self.input.fullPath())[0])[1])[0:11]=='blank_based':
            result=WriteDiskItem( 'OI BKSD Time Series' , 'Text file' ).findValue( value )
        elif (os.path.split(os.path.split(self.input.fullPath())[0])[1])=='raw':
            result=WriteDiskItem( 'OI Blank Time Series', 'Text file').findValue( value )

    if result is not None:
        return result # While opening process, result is not created
    else:
        return value

def initialization( self ):
    """Parameters values initialization
    """

    self.corner0='(,)' # corner0 initialization
    self.corner1='(,)' # corner1 initialization

    # Optional parameters
    self.setOptional('input_mask')
    self.setOptional('corner0')
    self.setOptional('corner1')
    self.setOptional('output_mask')

    self.signature['input'].browseUserLevel=2 # Browse only visible for expert user
    self.signature['input_mask'].browseUserLevel=2 # Browse only visible for expert user
    self.signature['output_mask'].browseUserLevel=2 # Browse only visible for expert user
    self.signature['output'].browseUserLevel=2 # Browse only visible for expert user

    self.addLink(None,'ROI',self.initSignature) # Change on signature if change on ROI
    self.addLink('output','ROI',self.initOutput) 
    self.addLink('output_mask','input', self.initOutputMask) # Change of output_mask if change on input

    self.addLink('output','input', self.initOutput) # Change of output if change on input

def execution( self, context ):
    """The execution process
    
    Parameters
    ----------
    context : BrainVISA context
    """
    import oidata.oisession_postprocesses as oisession_postprocesses

    # Top left-hand corner recovery
    if self.corner0 != '(,)': # If top left-hand corner was modified
        try:
            c0=eval(self.corner0) # Values recovery
        except SyntaxError:
            raise SyntaxError('Top left-hand corner is not properly completed')
        try:
            if len(c0)==2:
                corner0=c0
            else:
                raise SyntaxError('Top left-hand corner is not properly completed')        
        except TypeError:
            raise TypeError('Top left-hand corner is not properly completed')
    else: # If it was not modified
        corner0=None 
    
    # Bottom right-hand corner recovery
    if self.corner1 != '(,)': # If bottom right-hand corner was modified
        try:
            c1=eval(self.corner1) # Values recovery
        except SyntaxError:
            raise SyntaxError('Bottom right-hand corner is not properly completed')
        try:
            if len(c1)==2:
                corner1=c1
            else:
                raise SyntaxError('Top left-hand corner is not properly completed')        
        except TypeError:
            raise TypeError('Bottom right-hand corner is not properly completed')
    else: # If it was not modified
        corner1=None

    # Input_mask's path recuperation
    if self.input_mask is not None:
        input_mask=self.input_mask.fullPath()
    else:
        input_mask=None

    attributes=self.input.hierarchyAttributes() # Attributes recuperation
    format=os.path.splitext(os.path.splitext(self.output.fullPath())[0])[1]+os.path.splitext(self.output.fullPath())[1] # Formet recuperation

    # Averages a region of interest from an averaged image created using average_trial process
    oisession_postprocesses.average_region_process(
        database=attributes['_database'],
        protocol=attributes['protocol'],
        subject=attributes['subject'],
        session='session_'+attributes['session_date'],
        analysis=os.path.split(os.path.split(self.input.fullPath())[0])[1], # Analysis name
        filename=os.path.basename(self.input.fullPath()),
        corner0=corner0,
        corner1=corner1,
        path_mask=input_mask,
        format=format,
        mode=True, # The database mode
        context=context # BrainVISA context
        )
