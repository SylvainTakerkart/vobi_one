# Author: Flavien Garcia <flavien.garcia@free.fr>
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Apply a Durbin-Watson test on residuals to verify their independancy

# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path

try:
    import numpy as np # Needed to use matrix and list
except ImportError:
    raise ValidationError(_t_('Impossible to import numpy')) # Raises an exception

# Header    
name = _t_('Durbin-Watson Test') # Process name in the GUI
category = _t_('Session Post-Analysis') # Category name in the GUI
userLevel=0 # Always visible

# The parameters
signature=Signature(
    'format', Choice(('<auto>','.nii'),('NIFTI-1 image','.nii'),('gz compressed NIFTI-1 image','.nii.gz') ), # Saving format of images. It can be NIFTI-1 Image ('.nii') or gzip compressed NIFTI-1 Image ('.nii.gz')
    'conditions_file', ReadDiskItem( 'Trials+conditions list' , 'Text file' ), # The condition file path
    'analysis_name', Choice(('Choose an analysis name',None)), # The name of the analysis
    'conditions_list', String(), # A tuple of list of condition which has to be averaged. Exemple : [5,2] The files which have for condtions 5 and 2 will be averaged together.
    'ROI', Choice(('Rectangular ROI (from coordinates)','corners'),('Binary mask (from image)','mask') ), # Way to average images. It can be with corners (left-top and right-bottom) or with a mask (binary matrix)
    'corner0', String(), # The position of the left-head corner of the mask (x,y)
    'corner1', String(), # The position of the left-bottom corner of the mask (x,y)
    'input_mask', ReadDiskItem( 'OI Mask' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The path of an existing mask
    'data_graph', WriteDiskItem( 'OI GLM Data Graph','PNG image' ), # The data graph path
    )

def initAnalysisName( self,inp ):
    """Analysis name choice autocompletion

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    self.conditions_list='[,]' # Condition list initialization
    paramSignature=[] # New signature initialization
    for k,v in self.signature.items(): # For each item
        paramSignature.append(k) # Add the key
        paramSignature.append(v) # Add the value
          
    if self.conditions_file is not None:
        source=os.path.join(os.path.split(os.path.split(self.conditions_file.fullPath())[0])[0],'oisession_analysis')
        directory_list=os.listdir(source)
        name_list=[('Choose an analysis name',None)]
        for directory in directory_list:  
            if directory[0:9]=='glm_based' and directory[-5:]!='.minf':
                try:
                    name_list.index((str(directory[9:]),str(directory[9:])))
                except:
                    name_list.append((str(directory[9:]),str(directory[9:]))) 
            
        i=paramSignature.index('analysis_name')
        paramSignature[i+1]=Choice()
        paramSignature[i+1].setChoices(*name_list)
        signature=Signature(*paramSignature) # List to Signature
        self.changeSignature(signature) # Apply new signature
            
def initROI( self,inp ):
    """Signature change and parameters initialization

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    if self.ROI == 'corners': 
        self.input_mask=None
        # New signature
        paramSignature = ['format', Choice(('<auto>','.nii'),('NIFTI-1 image','.nii'),('gz compressed NIFTI-1 image','.nii.gz') ),
                          'conditions_file', ReadDiskItem( 'Trials+conditions list' , 'Text file' ),
                          'analysis_name', self.signature['analysis_name'], # The name of the analysis
                          'conditions_list', String(),
                          'ROI', Choice(('Rectangular ROI (from coordinates)','corners'),('Binary mask (from image)','mask') ),
                          'corner0', String(),
                          'corner1', String(),
                          'data_graph', WriteDiskItem( 'OI GLM Data Graph','PNG image'),
                          ]

        signature=Signature(*paramSignature)

        self.changeSignature( signature ) # Change of signature 
        self.addLink('data_graph','corner0',self.initDataGraph) # Change on data_graph if change on corner0   
        self.addLink('data_graph','corner1',self.initDataGraph) # Change on data_graph if change on corner1    
    
    if self.ROI == 'mask':
        self.corner0='(,)' # Left-head corner initialization
        self.corner1='(,)' # Right-bottom corner initialization
        # New signature
        paramSignature = ['format', Choice(('<auto>','.nii'),('NIFTI-1 image','.nii'),('gz compressed NIFTI-1 image','.nii.gz') ),
                          'conditions_file', ReadDiskItem( 'Trials+conditions list' , 'Text file' ),
                          'analysis_name', self.signature['analysis_name'], # The name of the analysis
                          'conditions_list', String(),
                          'ROI', Choice(('Rectangular ROI (from coordinates)','corners'),('Binary mask (from image)','mask') ),
                          'input_mask', ReadDiskItem( 'OI Mask' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                          'data_graph', WriteDiskItem( 'OI GLM Data Graph','PNG image' ),
                          ]

        signature=Signature(*paramSignature)

        self.changeSignature( signature ) # Change of signature 
        self.addLink('data_graph','input_mask',self.initDataGraph) # Change on data_graph if change on input_mask
    
    # Permissions
    self.signature['conditions_file'].browseUserLevel=2 # Browse only visible for expert user
    self.signature['data_graph'].browseUserLevel=2 # Browse only visible for expert user
    
def initDataGraph( self,inp ):
    """Signature change and parameters initialization

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    data_graph=None
    result=None
    filename=''
    if self.conditions_file is not None:
                                     
        # Conditions list recuperation
        cdt=''
        if self.conditions_list != '[,]':
            try:
                eval_conditions_list=eval(self.conditions_list) # Str to int
                for c in range(len(eval_conditions_list)): # For each condition
                    cdt+='_c'+str(eval_conditions_list[c])
            except:
                None
            
        # Region recuperation
        region=''
        if self.ROI == 'corners':
            if self.corner0 != '(,)' and self.corner1 != '(,)':
                region+='_'+str(eval(self.corner0)[0])+'_'+str(eval(self.corner0)[1])+'_'+str(eval(self.corner1)[0])+'_'+str(eval(self.corner1)[1])
        if self.ROI == 'mask':
            if self.input_mask != None:
                region='_'+os.path.split(self.input_mask.fullPath())[1][5:-len(self.format)]
        
        # Filename creation
        filename='durbin_watson_test'+cdt+region
        
        # Path location
        data_graph=self.conditions_file.hierarchyAttributes()
        data_graph['filename_variable']=filename
        try:
            if self.analysis_name is not None:
                data_graph['secondlevel_analysis']=self.analysis_name
        except:
            None
        result=WriteDiskItem( 'OI Data Graph', 'PNG image' ).findValue( data_graph )
        
    if result is not None:
        return result # While opening process, result is not created
    else:
        return data_graph
        
def initialization( self ):
    """Parameters values initialization
    """
    self.signature['conditions_file'].browseUserLevel=2 # Browse only visible for expert user
    self.signature['data_graph'].browseUserLevel=2 # Browse only visible for expert user
    self.setOptional( 'corner0' )
    self.setOptional( 'corner1' )
    self.conditions_list='[,]' # Condition list initialization
    self.corner0='(,)' # Left-head corner initialization
    self.corner1='(,)' # Right-bottom corner initialization
 
    # Links 
    self.addLink(None,'conditions_file',self.initAnalysisName) # Change on signature if change on conditions_file
        
    self.addLink(None,'ROI',self.initROI) # Change on signature if change on ROI
    
    self.addLink('data_graph','conditions_file',self.initDataGraph) # Change on data_graph if change on conditions_file
    self.addLink('data_graph','analysis_name',self.initDataGraph) # Change on data_graph if change on analysis_name
    self.addLink('data_graph','conditions_list',self.initDataGraph) # Change on data_graph if change on conditions_list
    self.addLink('data_graph','ROI',self.initDataGraph) # Change on data_graph if change on ROI   
    self.addLink('data_graph','corner0',self.initDataGraph) # Change on data_graph if change on corner0   
    self.addLink('data_graph','corner1',self.initDataGraph) # Change on data_graph if change on corner1
    self.addLink('data_graph','input_mask',self.initDataGraph) # Change on data_graph if change on input_mask
       
def execution( self, context ):
    """The execution process
    
    Parameters
    ----------
    context : BrainVISA context
    """
    import oidata.oisession_postprocesses as oisession_postprocesses

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
           
    oisession_postprocesses.durbin_watson_test_process(
        attributes['_database'],
        attributes['protocol'],
        attributes['subject'],
        'session_'+attributes['session_date'],
        'glm_based'+str(self.analysis_name),
        eval_cdt_list,
        corner0=corner0,
        corner1=corner1,
        path_mask=path_mask,
        format=self.format,
        data_graph=self.data_graph.fullPath().encode('utf8'),
        context=context,
        )      
