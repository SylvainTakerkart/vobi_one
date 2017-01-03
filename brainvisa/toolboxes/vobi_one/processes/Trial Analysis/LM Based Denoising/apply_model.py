# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Flavien Garcia <flavien.garcia@free.fr>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Denoising of input signal using the Linear Model

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
name=_t_('Apply Linear Model') # Process name in the GUI
category = _t_('LM Based Denoising') # Category name in the GUI
userLevel=0 # Always visible

signature=Signature(
    "format", apply( Choice,[('<auto>',None)] + map( lambda x: (x,getFormat(x)), list_formats ) ), # Saving format of images. It can be NIFTI-1 Image ('.nii') or gzip compressed NIFTI-1 Image ('.nii.gz')
    "glm", ReadDiskItem( 'OI GLM Design Matrix' , 'Text file' ), # The path of the Linear Model
    "data", ReadDiskItem( 'OI Raw Imported Data' , list_formats ), # The path of the external file, containing the raw NIFTI image
    "denoised", WriteDiskItem( 'OI GLM Denoised' , list_formats ), # The path where to save the denoised image
    "betas", WriteDiskItem( 'OI GLM Beta map',list_formats  ), # The path where to save betas
    "residuals", WriteDiskItem( 'OI GLM Residuals',list_formats  ), # The path where to save residual noise
    'ROI', Choice(('Rectangular ROI (from coordinates)','corners')\
                 ,('Binary mask (from image)','mask') ), # Way to average images. It can be with corners (top left-hand and bottom right-hand) or with a mask (binary matrix)
    'corner0', String(), # The position of the top left-hand corner of the mask (x,y)
    'corner1', String(), # The position of the bottom right-hand corner of the mask (x,y)
    "data_graph",WriteDiskItem( 'OI GLM Data Graph','PNG image'), # The data graph path
)
        
def initData( self, inp ):
    """Data autocompletion
    
    Parameters
    ----------
    inp : BrainVISA parameter type
            The parameter whose changes will be tracked to autocomplete the others
    """
    value={} # Value dictionary initialization
    if self.glm is not None:
         # Key value autocompletion
        value=self.glm.hierarchyAttributes()
        if 'secondlevel_analysis' in value: # If the user has selected the GLM session file
            value['firstlevel_analysis']=value['secondlevel_analysis'] # Gets trial analysis value
            del value['secondlevel_analysis'] # Delete the session analysis value
            try:
                del value['experience_number'] # Delete the experiment number value
                del value['trial_number'] # Delete the trial number value
            except:
                None

    return value

def initDenoised( self,inp ):
    """Denoised autocompletion
    
    Parameters
    ----------
    inp : BrainVISA parameter type
            The parameter whose changes will be tracked to autocomplete the others
    """
    value={} # Value dictionary initialization
    if self.data is not None:
         # Key value autocompletion
        value=self.data.hierarchyAttributes()

    if self.glm is not None:
         # Key value autocompletion
        if 'secondlevel_analysis' in self.glm.hierarchyAttributes(): # If the user has selected the GLM session file
            analysis_value=self.glm.hierarchyAttributes()['secondlevel_analysis']
        elif 'firstlevel_analysis' in self.glm.hierarchyAttributes(): # If the user has selected the GLM trial file
            analysis_value=self.glm.hierarchyAttributes()['firstlevel_analysis']          
        value['firstlevel_analysis']=analysis_value   # Gets trial analysis value 
          
    if self.format is not None:
        result = WriteDiskItem( 'OI GLM Denoised', self.format ).findValue( value )
    else:
        result = WriteDiskItem( 'OI GLM Denoised', 'NIFTI-1 image' ).findValue( value ) # Check list_formats in oiformats.py

    if result is not None:
        return result # While opening process, result is not created
    else:
        return value

def initResiduals( self,inp ):
    """Residuals autocompletion
    
    Parameters
    ----------
    inp : BrainVISA parameter type
            The parameter whose changes will be tracked to autocomplete the others
    """
    value={} # Value dictionary initialization
    if self.data is not None:
         # Key value autocompletion
        value=self.data.hierarchyAttributes()

    if self.glm is not None:
         # Key value autocompletion
        if 'secondlevel_analysis' in self.glm.hierarchyAttributes(): # If the user has selected the GLM session file
            analysis_value=self.glm.hierarchyAttributes()['secondlevel_analysis']
        elif 'firstlevel_analysis' in self.glm.hierarchyAttributes(): # If the user has selected the GLM trial file
            analysis_value=self.glm.hierarchyAttributes()['firstlevel_analysis']          
        value['firstlevel_analysis']=analysis_value   # Gets trial analysis value  

    if self.format is not None:
        result = WriteDiskItem( 'OI GLM Residuals', self.format ).findValue( value )
    else:
        result = WriteDiskItem( 'OI GLM Residuals', 'NIFTI-1 image' ).findValue( value ) # Check list_formats in oiformats.py

    if result is not None:
        return result # While opening process, result is not created
    else:
        return value

def initBeta( self,inp ):
    """Betas autocompletion
    
    Parameters
    ----------
    inp : BrainVISA parameter type
            The parameter whose changes will be tracked to autocomplete the others
    """
    value={} # Value dictionary initialization
    if self.data is not None:
        # Key value autocompletion
        value=self.data.hierarchyAttributes()

    if self.glm is not None:
         # Key value autocompletion
        if 'secondlevel_analysis' in self.glm.hierarchyAttributes(): # If the user has selected the GLM session file
            analysis_value=self.glm.hierarchyAttributes()['secondlevel_analysis']
        elif 'firstlevel_analysis' in self.glm.hierarchyAttributes(): # If the user has selected the GLM trial file
            analysis_value=self.glm.hierarchyAttributes()['firstlevel_analysis']          
        value['firstlevel_analysis']=analysis_value   # Gets trial analysis value 

    if self.format is not None:
        result = WriteDiskItem( 'OI GLM Beta map', self.format ).findValue( value )
    else:
        result = WriteDiskItem( 'OI GLM Beta map', 'NIFTI-1 image' ).findValue( value ) # Check list_formats in oiformats.py

    if result is not None:
        return result # While opening process, result is not created
    else:
        return value
        
def changeROI( self,inp ):
    """Signature change and parameters initialization

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    paramSignature=[] # New signature initialization
    for k,v in self.signature.items(): # For each item
        paramSignature.append(k) # Add the key
        paramSignature.append(v) # Add the value
        
    if inp=='mask': # If user wants to average with a binary mask
        try:
            i=paramSignature.index('corner0') # Find the index of the top left-hand corner input
            del paramSignature[i:i+4] # Delete the two corners input
            paramSignature.insert(i,'input_mask') # Add binary mask input
            paramSignature.insert(i+1,ReadDiskItem( 'OI Mask' , ['NIFTI-1 image','gz compressed NIFTI-1 image'])) # Insert mask type       
            signature=Signature(*paramSignature) # List to Signature
            self.changeSignature(signature) # Apply new signature
            self.addLink('data_graph','input_mask',self.initDataGraph) # Change on data_graph if change on input_mask 
        except:
            None

    else: # If user wants to average over a rectangular ROI
        try:
            i=paramSignature.index('input_mask')# Find the index of the binary mask input
            self.input_mask=None
            del paramSignature[i:i+2] # Delete the binary mask input
            paramSignature.insert(i,'corner0') # Add top left-hand corner input
            paramSignature.insert(i+1,String()) # Insert corner type
            paramSignature.insert(i+2,'corner1') # Add bottom right-hand corner input
            paramSignature.insert(i+3,String()) # Insert corner type
            signature=Signature(*paramSignature) # List to Signature
            self.changeSignature(signature) # Apply new signature
            self.corner0='(,)'
            self.corner1='(,)'
            self.addLink('data_graph','corner0',self.initDataGraph) # Change on data_graph if change on corner0
            self.addLink('data_graph','corner1',self.initDataGraph) # Change on data_graph if change on corner1
        except:
            None
            
def initDataGraph( self,inp ):
    """Figure file path autocompletion

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    # Variables initialization
    data_graph=None # Figure path initialization
    result=None # Value founded initialization
    filename=''
    
    if self.format == 'gz compressed NIFTI-1 image':
        format='.nii.gz'
    else:
        format='.nii'
        
    if self.denoised is not None:
        data_graph=self.denoised.hierarchyAttributes()
        filename=os.path.split(self.data.fullPath())[1][:-len(str(format))] # Filename variable initialization
    
    region=''
    if self.ROI=='mask' and self.input_mask is not None:
        region+='_over_'+os.path.basename(self.input_mask.fullPath())[:-len(str(format))]
    else:
        try:
            corner0=eval(self.corner0)
            corner1=eval(self.corner1)
            region+='_over_'+str(corner0[0])+'_'+str(corner0[1])+'_'+str(corner1[0])+'_'+str(corner1[1])
        except:
            None
    
    filename+=region
        
    # Path location
    if data_graph is not None:
        data_graph['filename_variable']=filename
        
    result=WriteDiskItem( 'OI GLM Data Graph', 'PNG image' ).findValue( data_graph )
    if result is not None:
        return result # While opening process, result is not created
    else:
        return data_graph
        
def initialization( self ):
    """Parameters values initialization
    """
    # Optional parameters
    self.setOptional('format') # Format of images
    self.corner0='(,)'
    self.corner1='(,)'   
    
    # Visibility
    self.signature["data"].browseUserLevel = 2 # Browse only visible for expert user
    self.signature["glm"].browseUserLevel = 2 # Browse only visible for expert user
    self.signature["betas"].browseUserLevel = 2 # Browse only visible for expert user
    self.signature["residuals"].browseUserLevel = 2 # Browse only visible for expert user
    self.signature["denoised"].browseUserLevel = 2 # Browse only visible for expert user
    self.signature["data_graph"].browseUserLevel = 2 # Browse only visible for expert user
    
    # Changes links
    self.addLink( 'data','glm', self.initData ) # Change of data if change on glm

    self.addLink( 'denoised','data',self.initDenoised ) # Change of denoised if change on data
    self.addLink( 'denoised','format',self.initDenoised ) # Change of denoised if change on format

    self.addLink( 'residuals','data',self.initResiduals ) # Change of residuals if change on data
    self.addLink( 'residuals','format',self.initResiduals ) # Change of residuals if change on format

    self.addLink( 'betas','data',self.initBeta ) # Change of betas if change on data
    self.addLink( 'betas','format',self.initBeta ) # Change of betas if change on format
    
    self.addLink( None,'ROI',self.changeROI) # Chane on signature if change on ROI
    self.addLink( 'data_graph','glm',self.initDataGraph)
    self.addLink( 'data_graph','data',self.initDataGraph)
    self.addLink( 'data_graph','ROI',self.initDataGraph) # Change of corners if change on visualization
    self.addLink('data_graph','corner0',self.initDataGraph) # Change on data_graph if change on corner0
    self.addLink('data_graph','corner1',self.initDataGraph) # Change on data_graph if change on corner1

def execution( self , context ):
    """The execution process
    
    Parameters
    ----------
    context : BrainVISA context
    """
    import oidata.oitrial_processes as oitrial_processes

    # Analysis recuperation
    if 'secondlevel_analysis' in self.glm.hierarchyAttributes(): # If the user has selected the GLM session file
        analysis_value=self.glm.hierarchyAttributes()['secondlevel_analysis']
    elif 'firstlevel_analysis' in self.glm.hierarchyAttributes(): # If the user has selected the GLM trial file
        analysis_value=self.glm.hierarchyAttributes()['firstlevel_analysis']
    analysis = 'glm_based' + analysis_value
    
    # Format recuperation
    if self.format == 'gz compressed NIFTI-1 image':
        format='.nii.gz'
    else:
        format='.nii'
    
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
    
    # Mask recuperation
    try:
        mask=str(self.input_mask)
    except:
        mask=None

    # Denoising of input signal using the Linear Model
    oitrial_processes.estimate_model_process(
        self.data.fullPath().encode('utf8'), # Data file path
        glm=self.glm.fullPath().encode('utf8'), # GLM file path
        betas=self.betas.fullPath().encode('utf8'), # Betas file path
        residuals=self.residuals.fullPath().encode('utf8'), # Residuals file path
        denoised=self.denoised.fullPath().encode('utf8'), # Denoised file path
        analysis=analysis,
        format=format,
        mode=True, # The database mode
        corner0=corner0,corner1=corner1,
        mask=mask,
        data_graph=self.data_graph.fullPath().encode('utf8'),
        context=context # BrainVISA context
        )