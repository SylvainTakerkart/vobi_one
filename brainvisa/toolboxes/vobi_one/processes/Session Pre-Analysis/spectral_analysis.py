# Author: Flavien Garcia <flavien.garcia@free.fr>
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Spectral analysis with visualization. Allow to detect frequencies of spikes by
# calculating the spectrum of each blank file and meaning all this spectrums.

# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path

try:
    import numpy as np # Needed to use matrix and list
except ImportError:
    raise ValidationError(_t_('Impossible to import numpy')) # Raises an exception

# Header
name = _t_('Spectral Analysis') # Process name in the GUI
category = _t_('Session Pre-Analysis') # Category name in the GUI
userLevel=0 # Always visible

# The parameters
signature=Signature(
    'format', Choice(('<auto>','.nii')\
                    ,('NIFTI-1 image','.nii')\
                    ,('gz compressed NIFTI-1 image','.nii.gz')), # Saving format of images. It can be NIFTI-1 Image ('.nii') or gzip compressed NIFTI-1 Image ('.nii.gz')
    'conditions_file', ReadDiskItem( 'Trials+conditions list' , 'Text file' ), # The condition file path
    'conditions_list', String(), # A list of condition which has to be averaged. Exemple : ([0,15]) The files which have for condtions 0 and 15 will be averaged together.
    'ROI', Choice(('Rectangular ROI (from coordinates)','corners')\
                 ,('Binary mask (from image)','mask') ), # Way to average images over a region of interest. It can be with corners (top left-hand and bottom right-hand) or with a mask (binary matrix)
    'corner0', String(), # The position of the top left-hand corner of the mask (x,y)
    'corner1', String(), # The position of the bottom right-hand corner of the mask (x,y)
    'input_mask', ReadDiskItem( 'OI Mask',['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The path of an existing mask
    'data_graph', WriteDiskItem( 'OI Blank Data Graph','PNG image' ), # The data graph path
    )
    
def changeROI(self,inp):
    """Signature change and ROI parameters initialization

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    if self.ROI == 'corners': # If user wants the image averaging using rectangular ROI 
        # New signature
        self.input_mask=None
        paramSignature = ['format', Choice(('<auto>','.nii')\
                                          ,('NIFTI-1 image','.nii')\
                                          ,('gz compressed NIFTI-1 image','.nii.gz') ),
                          'conditions_file', ReadDiskItem( 'Trials+conditions list' , 'Text file' ),
                          'conditions_list', String(),
                          'ROI', Choice(('Rectangular ROI (from coordinates)','corners')\
                                       ,('Binary mask (from image)','mask') ),
                          'corner0', String(),
                          'corner1', String(),
                          'data_graph', WriteDiskItem( 'OI Blank Data Graph','PNG image' ),
                          ]

        signature=Signature(*paramSignature) # List to Signature
        self.changeSignature( signature ) # Change of signature 

        self.addLink('data_graph','corner0',self.initDataGraph) # Change on data_graph if change on corner0   
        self.addLink('data_graph','corner1',self.initDataGraph) # Change on data_graph if change on corner1
        
    if self.ROI == 'mask': # If user wants the image averaging using binary mask
        # New signature
        self.corner0='(,)'
        self.corner1='(,)'
        paramSignature = ['format', Choice(('<auto>','.nii')\
                                          ,('NIFTI-1 image','.nii')\
                                          ,('gz compressed NIFTI-1 image','.nii.gz') ),
                          'conditions_file', ReadDiskItem( 'Trials+conditions list' , 'Text file' ),
                          'conditions_list', String(),
                          'ROI', Choice(('Rectangular ROI (from coordinates)','corners')\
                                       ,('Binary mask (from image)','mask') ),
                          'input_mask', ReadDiskItem( 'OI Mask' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                          'data_graph', WriteDiskItem( 'OI Blank Data Graph','PNG image' ),
                          ]

        signature=Signature(*paramSignature) # List to Signature
        self.changeSignature( signature ) # Change of signature
        
        self.addLink('data_graph','input_mask',self.initDataGraph) # Change on data_graph if change on input_mask 
        
    # Permissions
    self.signature['conditions_file'].browseUserLevel=2 # Browse only visible for expert user
    self.signature['data_graph'].browseUserLevel=2 # Browse only visible for expert user
    
def initDataGraph( self,inp ):
    """Data graph path autocompetion

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    # Variables initialization
    data_graph=None # Hierarchy attributes of the data graph path
    result=None # Result of data_graph fiel search
    filename='' # Filename variable
    
    # Parameters recovery
    if self.conditions_file is not None: # If user has selected a session
                                     
        # Conditions list recovery
        cdt='' # String describing conditions
        if self.conditions_list != '[,]': # If user has modified conditions list
            eval_cdt_list=eval(self.conditions_list) # Str to int list
            for c in range(len(eval_cdt_list)): # For each condition
                cdt+='_c'+str(eval_cdt_list[c]) # Add condition text
            
        # ROI recovery
        roi='' # String describing ROI
        if self.ROI == 'corners': # If user wants the image averaging using rectangular ROI 
            if self.corner0 != '(,)' and self.corner1 != '(,)': # If user has modified the two corners
                try:
                    roi+='_'+str(eval(self.corner0)[0])\
                        +'_'+str(eval(self.corner0)[1])\
                        +'_'+str(eval(self.corner1)[0])\
                        +'_'+str(eval(self.corner1)[1]) # Add ROI text
                except:
                    None
        if self.ROI == 'mask': # If user wants the image averaging using binary mask
            if self.input_mask != None: # If user has selected an existing mask
                roi='_mask_'+os.path.split(self.input_mask.fullPath())[1][5:-len(self.format)]
        
        # Filename creation
        filename='spectral_analysis'+cdt+roi
        
        # Path location
        data_graph=self.conditions_file.hierarchyAttributes()
        data_graph['filename_variable']=filename
        result=WriteDiskItem( 'OI Blank Data Graph', 'PNG image' ).findValue( data_graph )
        
    if result is not None: # If a data graph was found
        return result # Return this file
    else:
        return data_graph
        
def initialization( self ):
    """Parameters values initialization
    """
    # Permissions
    self.signature['conditions_file'].browseUserLevel=2 # Browse only visible for expert user
    self.signature['data_graph'].browseUserLevel=2 # Browse only visible for expert user
    
    self.setOptional( 'corner0' ) # User may choose to average over all the image 
    self.setOptional( 'corner1' ) # User may choose to average over all the image 
    self.conditions_list='[,]' # Condition list initialization
    self.corner0='(,)' # Top left-hand corner initialization
    self.corner1='(,)' # Bottom right-hand corner initialization
    
    # Links
    self.addLink('data_graph','conditions_file',self.initDataGraph) # Change on data_graph if change on conditions_file
    self.addLink('data_graph','conditions_list',self.initDataGraph) # Change on data_graph if change on conditions_list
    self.addLink('data_graph','ROI',self.initDataGraph) # Change on data_graph if change on ROI   
    self.addLink('data_graph','corner0',self.initDataGraph) # Change on data_graph if change on corner0   
    self.addLink('data_graph','corner1',self.initDataGraph) # Change on data_graph if change on corner1
    self.addLink('data_graph','input_mask',self.initDataGraph) # Change on data_graph if change on input_mask
    self.addLink(None,'ROI',self.changeROI) # Change on signature if change on ROI
       
def execution( self, context ):
    """The execution process
    
    Parameters
    ----------
    context : BrainVISA context
    """
    import oidata.oisession_preprocesses as oisession_preprocesses
    
    # Hierarchy attributes recovery
    attributes=self.conditions_file.hierarchyAttributes() # Attributes recuperation

    # Conditions list recovery
    try:
        eval_cdt_list=sorted(eval(self.conditions_list)) # Str to int
        if len(eval_cdt_list)>1 and type(eval_cdt_list[0])!=int:
            raise SyntaxError('Conditions list not properly completed')
    except SyntaxError:
        raise SyntaxError('Conditions list is not properly completed')
    
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
    
    # Mask recovery
    try:
        path_mask=self.input_mask.fullPath().encode('utf8')
    except:
        path_mask=None

    # Lauching the process 
    oisession_preprocesses.spectral_analysis_process(
        attributes['_database'],
        attributes['protocol'],
        attributes['subject'],
        'session_'+attributes['session_date'],
        'raw',
        eval_cdt_list,
        corner0=corner0,
        corner1=corner1,
        path_mask=path_mask,
        format=self.format,
        data_graph=self.data_graph.fullPath().encode('utf8'),
        context=context,
        )                                   