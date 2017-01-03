# Author: Flavien Garcia <flavien.garcia@free.fr>
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Calculates means responses of only one analyse showing all trials in background too.


# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path

try:
    import numpy as np # Needed to use matrix and list
except ImportError:
    raise ValidationError(_t_('Impossible to import numpy')) # Raises an exception

# Header
name = _t_('Visualization of Trials Variability') # Process name in the GUI
category = _t_('Session Post-Analysis') # Category name in the GUI
userLevel=0 # Always visible

# The parameters
signature=Signature(
    'format', Choice(('<auto>','.nii')\
                    ,('NIFTI-1 image','.nii')\
                    ,('gz compressed NIFTI-1 image','.nii.gz') ), # Saving format of images. It can be NIFTI-1 Image ('.nii') or gzip compressed NIFTI-1 Image ('.nii.gz')
    'conditions_file', ReadDiskItem( 'Trials+conditions list' , 'Text file' ), # The condition file path
    'model', Choice(('Linear Model (GLM)','GLM')\
                   ,('Blank Subtraction (BkS)','BkS')\
                   ,('Blank Subtraction + Detrending (BkSD)','BkSD')), # Model choice
    'analysis_name', Choice(('Choose an analysis name',None)), # The name of the analysis
    'conditions_list', String(), # A tuple of list of condition which has to be averaged. Exemple : [5,2],[4] The files which have for condtions 5 and 2 will be averaged together.
    'ROI', Choice(('Rectangular ROI (from coordinates)','corners')\
                 ,('Binary mask (from image)','mask') ), # Way to average images. It can be with corners (Top left-hand and bottom right-hand) or with a mask (binary matrix)
    'corner0', String(), # The position of the top left-hand corner of the mask (x,y)
    'corner1', String(), # The position of the left-bottom corner of the mask (x,y)
    'input_mask', ReadDiskItem( 'OI Mask' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ), # The path of an existing mask
    'data_graph', WriteDiskItem( 'OI GLM Data Graph','PNG image' ), # The data_graph file path
    )

def initSignature( self,inp ):
    """Signature change and ROI parameters initialization

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    if self.model == 'GLM' and self.ROI == 'corners':        
        self.analysis_name=None
        self.input_mask=None
        # New signature
        paramSignature = ['format', Choice(('<auto>','.nii')\
                                          ,('NIFTI-1 image','.nii')\
                                          ,('gz compressed NIFTI-1 image','.nii.gz') ),
                          'conditions_file', ReadDiskItem( 'Trials+conditions list' , 'Text file' ),
                          'model', Choice(('Linear Model (GLM)','GLM')\
                                         ,('Blank Subtraction (BkS)','BkS'),('Blank Subtraction + Detrending (BkSD)','BkSD')),
                          'analysis_name', self.signature['analysis_name'], # The name of the analysis
                          'conditions_list', String(),
                          'ROI', Choice(('Rectangular ROI (from coordinates)','corners')\
                                       ,('Binary mask (from image)','mask') ),
                          'corner0', String(),
                          'corner1', String(),
                          'data_graph', WriteDiskItem( 'OI GLM Data Graph','PNG image' ),
                          ]
                          
    elif self.model == 'GLM' and self.ROI == 'mask': # If user wants to average with a binary mask 
        self.corner0='(,)'
        self.corner1='(,)'        
        self.analysis_name=None
        # New signature
        paramSignature = ['format', Choice(('<auto>','.nii')\
                                          ,('NIFTI-1 image','.nii')\
                                          ,('gz compressed NIFTI-1 image','.nii.gz') ),
                          'conditions_file', ReadDiskItem( 'Trials+conditions list' , 'Text file' ),
                          'model', Choice(('Linear Model (GLM)','GLM')\
                                         ,('Blank Subtraction (BkS)','BkS'),('Blank Subtraction + Detrending (BkSD)','BkSD')),
                          'analysis_name', self.signature['analysis_name'], # The name of the analysis
                          'conditions_list', String(),
                          'ROI', Choice(('Rectangular ROI (from coordinates)','corners')\
                                       ,('Binary mask (from image)','mask') ),
                          'input_mask', ReadDiskItem( 'OI Mask' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                          'data_graph', WriteDiskItem( 'OI GLM Data Graph','PNG image' ),
                          ]


    elif self.model != 'GLM' and self.ROI == 'corners':
        self.input_mask=None
        self.analysis_name=None
        # New signature
        paramSignature = ['format', Choice(('<auto>','.nii')\
                                          ,('NIFTI-1 image','.nii')\
                                          ,('gz compressed NIFTI-1 image','.nii.gz') ),
                          'conditions_file', ReadDiskItem( 'Trials+conditions list' , 'Text file' ),
                          'model', Choice(('Linear Model (GLM)','GLM')\
                                         ,('Blank Subtraction (BkS)','BkS'),('Blank Subtraction + Detrending (BkSD)','BkSD')),
                          'analysis_name', self.signature['analysis_name'], # The name of the analysis
                          'conditions_list', String(),
                          'ROI', Choice(('Rectangular ROI (from coordinates)','corners')\
                                       ,('Binary mask (from image)','mask') ),
                          'corner0', String(),
                          'corner1', String(),
                          'data_graph', WriteDiskItem( 'OI BkSD Data Graph','PNG image' ),
                          ]
                          
    else:  
        self.corner0='(,)'
        self.corner1='(,)'
        self.analysis_name=None
        # New signature
        paramSignature = ['format', Choice(('<auto>','.nii')\
                                          ,('NIFTI-1 image','.nii')\
                                          ,('gz compressed NIFTI-1 image','.nii.gz') ),
                          'conditions_file', ReadDiskItem( 'Trials+conditions list' , 'Text file' ),
                          'model', Choice(('Linear Model (GLM)','GLM')\
                                         ,('Blank Subtraction (BkS)','BkS'),('Blank Subtraction + Detrending (BkSD)','BkSD')),
                          'analysis_name', self.signature['analysis_name'], # The name of the analysis
                          'conditions_list', String(),
                          'ROI', Choice(('Rectangular ROI (from coordinates)','corners')\
                                       ,('Binary mask (from image)','mask') ),
                          'input_mask', ReadDiskItem( 'OI Mask' , ['NIFTI-1 image','gz compressed NIFTI-1 image'] ),
                          'data_graph', WriteDiskItem( 'OI BkSD Data Graph','PNG image' ),
                          ]
                          
    signature=Signature(*paramSignature) # List to Signature
    self.changeSignature( signature ) # Change of signature
    # Permissions
    self.signature['conditions_file'].browseUserLevel=2 # Browse only visible for expert user
    self.signature['data_graph'].browseUserLevel=2 # Browse only visible for expert user    
    # Links
    self.addLink('data_graph','input_mask',self.initDataGraph) # Change on data_graph if change on input_mask
    self.addLink('data_graph','corner0',self.initDataGraph) # Change on data_graph if change on corner0
    self.addLink('data_graph','corner1',self.initDataGraph) # Change on data_graph if change on corner1

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
          
    if self.conditions_file is not None and self.model is not None:
        source=os.path.join(os.path.split(os.path.split(self.conditions_file.fullPath())[0])[0],'oisession_analysis')
        directory_list=os.listdir(source)
        name_list=[('Choose an analysis name',None)]
        if self.model=='GLM':
            for directory in directory_list:  
                if directory[0:9]=='glm_based' and directory[-5:]!='.minf':
                    try:
                        name_list.index((str(directory[9:]),str(directory[9:])))
                    except:
                        name_list.append((str(directory[9:]),str(directory[9:])))
        else:
            for directory in directory_list:
                if directory[0:11]=='blank_based' and directory[-5:]!='.minf':
                    try:
                        name_list.index((str(directory[11:]),str(directory[11:])))
                    except:
                        name_list.append((str(directory[11:]),str(directory[11:])))
                        
        i=paramSignature.index('analysis_name')
        prec=str(getattr(self,'analysis_name'))
        self.analysis_name=None
        paramSignature[i+1]=Choice()
        paramSignature[i+1].setChoices(*name_list)
        signature=Signature(*paramSignature) # List to Signature
        self.changeSignature(signature) # Apply new signature
        self.addLink('data_graph','analysis_name',self.initDataGraph) # Change on data_graph if change on analysis_name
        if (prec,prec) in name_list:
            setattr(self,'analysis_name',prec)    
            
def initDataGraph( self,inp ):
    """Figure file path autocompetion

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    # Variables initialization
    data_graph=None # Hierarchy attributes of the data_graph file path
    result=None # Result of data_graph fiel search
    filename='' # Filename variable
    
    # Parameters recovery
    if self.conditions_file is not None: # If user has selected a session
                            
        # Conditions list recovery
        cdt=''
        if self.conditions_list not in ['[,]','[[,],]']: # If user has modified the condtions list
            try:
                eval_cdt_list=eval(self.conditions_list) # Str to int list
                if len(eval_cdt_list)==1 and type(eval_cdt_list[0])==int: # If there is only one group
                    eval_cdt_list=[eval_cdt_list]
                for g in range(len(eval_cdt_list)): # For each group
                    cdt+='_c'
                    if type(eval_cdt_list[g])==int: # If group contains only one condition
                        eval_cdt_list[g]=[eval_cdt_list[g]]
                    for c in range(len(eval_cdt_list[g])-1): # For each condition
                        cdt+=str(eval_cdt_list[g][c])+'+c'
                    cdt+=str(eval_cdt_list[g][len(eval_cdt_list[g])-1]) # Last condition
            except:
                None
        # ROI recovery
        roi='' # String describing ROI
        if self.ROI == 'corners': # If user wants the image averaging using rectangular ROI 
            if self.corner0 != '(,)' and self.corner1 != '(,)': # If user has modified the two corners
                roi+='_'+str(eval(self.corner0)[0])\
                    +'_'+str(eval(self.corner0)[1])\
                    +'_'+str(eval(self.corner1)[0])\
                    +'_'+str(eval(self.corner1)[1]) # Add ROI text
        if self.ROI == 'mask': # If user wants the image averaging using binary mask
            if self.input_mask != None: # If user has selected an existing mask
                roi='_'+os.path.split(self.input_mask.fullPath())[1][5:-len(self.format)]
        
        # Model recovery
        model=self.model
            
        # Filename creation
        filename=model+cdt+roi
        
        # Path location
        data_graph=self.conditions_file.hierarchyAttributes()  
        data_graph['filename_variable']=filename
        try:
            if self.analysis_name is not None:
                data_graph['secondlevel_analysis']=self.analysis_name
        except:
            None
        if model=='GLM':
            result=WriteDiskItem( 'OI GLM Data Graph', 'PNG image' ).findValue( data_graph )
        else:
            result=WriteDiskItem( 'OI BkSD Data Graph', 'PNG image' ).findValue( data_graph )
            
    if result is not None: # If a data graph was found
        return result # Return this file
    else:
        return data_graph
        
def initialization( self ):
    """Parameters values initialization
    """
    self.signature['conditions_file'].browseUserLevel=2 # Browse only visible for expert user
    self.signature['data_graph'].browseUserLevel=2 # Browse only visible for expert user
    self.setOptional( 'corner0' ) # User may choose to average over all the image 
    self.setOptional( 'corner1' ) # User may choose to average over all the image 
    self.conditions_list='[,]' # Conditions list initialization
    self.corner0='(,)' # Top left-hand corner initialization
    self.corner1='(,)' # Bottom right-hand corner initialization

    self.addLink(None,'conditions_file',self.initAnalysisName) # Change on signature if change on conditons_file
    self.addLink(None,'model',self.initAnalysisName) # Change on signature if change on model
    
    self.addLink('data_graph','conditions_file',self.initDataGraph) # Change on data_graph if change on conditions_file
    self.addLink('data_graph','analysis_name',self.initDataGraph) # Change on data_graph if change on analysis_name
    self.addLink('data_graph','conditions_list',self.initDataGraph) # Change on data_graph if change on conditions_list
    self.addLink('data_graph','ROI',self.initDataGraph) # Change on data_graph if change on ROI   
    self.addLink('data_graph','corner0',self.initDataGraph) # Change on data_graph if change on corner0   
    self.addLink('data_graph','corner1',self.initDataGraph) # Change on data_graph if change on corner1
    self.addLink('data_graph','input_mask',self.initDataGraph) # Change on data_graph if change on input_mask
    self.addLink('data_graph','model',self.initDataGraph) # Change on data_graph if change on model
    self.addLink(None,'ROI',self.initSignature) # Change on signature if change on ROI
    self.addLink(None,'model',self.initSignature) # Change on signature if change on model  
    
def execution( self, context ):
    """The execution process
    
    Parameters
    ----------
    context : BrainVISA context
    """
    import oidata.oisession_postprocesses as oisession_postprocesses

    attributes=self.conditions_file.hierarchyAttributes()

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

    # ROI recovery
    roi=[]
    if path_mask is not None:
        roi.append(path_mask)
    elif corner0 is not None and corner1 is not None:
        roi.append((corner0,corner1))
    else:
        roi.append((None,None))
        
    # Blank based suffix and model recovery
    blank_based_suffix=''
    model='glm_based'
    if self.model=='BkS':
        model='blank_based'
        blank_based_suffix='_f0d_bks'
    if self.model=='BkSD':
        model='blank_based'
        blank_based_suffix='_f0d_bks_d'
           
    oisession_postprocesses.visualization_of_trials_variability_process(
        attributes['_database'],
        attributes['protocol'],
        attributes['subject'],
        'session_'+attributes['session_date'],
        model+str(self.analysis_name),
        eval_cdt_list,
        blank_based_suffix,
        roi=roi,
        format=self.format,
        data_graph=self.data_graph.fullPath().encode('utf8'),
        context=context,
        )  
