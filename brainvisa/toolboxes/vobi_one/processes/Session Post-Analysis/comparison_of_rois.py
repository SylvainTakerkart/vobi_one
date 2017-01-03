# Author: Flavien Garcia <flavien.garcia@free.fr>
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Compares the mean response of one analyse over different regions.
# Each analyse include its way of average (Rectangular ROI or binary mask)
# Possibility to select the model (GLM, BkS or BkSD), the conditions file and 
# the conditions list.

# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path

try:
    import numpy as np # Needed to use matrix and list
except ImportError:
    raise ValidationError(_t_('Impossible to import numpy')) # Raises an exception

# Header
name = _t_('Comparison of ROIs') # Process name in the GUI
category = _t_('Session Post-Analysis') # Category name in the GUI
userLevel=0 # Always visible

# The parameters
signature=Signature(
    'format', Choice(('<auto>','.nii')\
                    ,('NIFTI-1 image','.nii')\
                    ,('gz compressed NIFTI-1 image','.nii.gz')), # Saving format of images. It can be NIFTI-1 Image ('.nii') or gzip compressed NIFTI-1 Image ('.nii.gz')
    'conditions_file', ReadDiskItem( 'Trials+conditions list' , 'Text file' ), # The condition file path
    'model', Choice(('Linear Model (GLM)','GLM')\
                   ,('Blank Subtraction (BkS)','BkS')\
                   ,('Blank Subtraction + Detrending (BkSD)','BkSD')), # Model choice
    'analysis_name', Choice(('Choose an analysis name',None)), # The name of the analysis
    'conditions_list', String(), # A tuple of list of condition which has to be averaged. Exemple : ([5,2]) The files which have for conditions 5 and 2 will be averaged together.
    'ROI_1', Choice(('Change to add new region','auto_1')\
                   ,('Rectangular ROI (from coordinates)','corners_1')\
                   ,('Binary mask (from image)','mask_1') ), # Way to average images. It can be with corners (top left-hand and bottom right-hand) or with a mask (binary matrix)                               
    'data_graph', WriteDiskItem( 'OI BkSD Data Graph','PNG image' ), # The data graph path
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
        paramSignature[i+1]=Choice()
        paramSignature[i+1].setChoices(*name_list)
        signature=Signature(*paramSignature) # List to Signature
        self.changeSignature(signature) # Apply new signature
        self.addLink('data_graph','analysis_name',self.initDataGraph) # Change on data_graph if change on analysis_name
        if (prec,prec) in name_list:
            setattr(self,'analysis_name',prec)
            
def changeROI( self ,inp):
    """Signature change and parameters initialization

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    # Recovery of available regions
    index_regions=[] # List of regions'index initialization
    for k in range(1,len(self.signature.keys())+1): # For each signature's key
        if self.signature.keys()[k-1][:-1]=='ROI_': # If key is a region with a digit index
            index_regions.append(int(self.signature.keys()[k-1][-1])) # Add index of this region
        if self.signature.keys()[k-1][:-2]=='ROI_': # If key is a region with a number index
            index_regions.append(int(self.signature.keys()[k-1][-2:])) # Add index of this region
    paramSignature=[] # New signature initialization
    for k,v in self.signature.items(): # For each item
        paramSignature.append(k) # Add the key
        paramSignature.append(v) # Add the value          
    # Apply changes       
    for r in index_regions: # For each available region
        
        if inp in ['mask_'+str(r),'corners_'+str(r)]:
            
            if inp=='mask_'+str(r): # If current region has changed in a binary mask
                    
                try: # Test if current region was a rectangular ROI before change
                    i=paramSignature.index('corner0_'+str(r)) # Search the top left-hand corner
                    del paramSignature[i:i+4] # Delete the two corners
                except:
                    None
                try: # Add mask to current region
                    i=paramSignature.index('ROI_'+str(r)) # Search current region
                    paramSignature[i+1]=Choice(('Delete region','auto_'+str(r))\
                                              ,('Rectangular ROI (from coordinates)','corners_'+str(r))\
                                              ,('Binary mask (from image)','mask_'+str(r))) # Change choice by default
                    paramSignature.insert(i+2,'input_mask_'+str(r)) # Insert mask key
                    paramSignature.insert(i+3,ReadDiskItem( 'OI Mask' , ['NIFTI-1 image','gz compressed NIFTI-1 image'])) # Insert mask type
                except:
                    None
                try: # Test if next region already exists
                    paramSignature.index('ROI_'+str(r+1)) # Search next region
                    signature=Signature(*paramSignature) # New signature recovery
                    self.changeSignature(signature) # Apply new signature                   
                    self.addLink('data_graph','input_mask_'+str(r),self.initDataGraph)
                except: # If not, a region is added
                    i=paramSignature.index('ROI_'+str(r)) # Search current region
                    paramSignature.insert(i+4,'ROI_'+str(r+1)) # Insert next region key
                    paramSignature.insert(i+5,Choice(('Change to add new region','auto_'+str(r+1))\
                                                    ,('Rectangular ROI (from coordinates)','corners_'+str(r+1))\
                                                    ,('Binary mask (from image)','mask_'+str(r+1)))) # Insert next region type     
                    signature=Signature(*paramSignature) # New signature recovery
                    self.changeSignature(signature) # Apply new signature
                    # Permissions
                    self.signature['input_mask_'+str(r)].browseUserLevel=2 # Browse only visible for expert user
                    # Links
                    self.addLink(None,'ROI_'+str(r+1),self.changeROI)
                    self.addLink('data_graph','ROI_'+str(r+1),self.initDataGraph) # Change on data_graph if change on ROI                                        
                    self.addLink('data_graph','input_mask_'+str(r),self.initDataGraph)
                    self.signature['ROI_'+str(r)].mandatory=False # Current region can be optional
                    self.signature['ROI_'+str(r+1)].mandatory=0 # Current region can be optional               
                       
            if inp=='corners_'+str(r): # If current region has changed in a rectangular ROI
                try: # Test if current region was a binary mask before change
                    i=paramSignature.index('input_mask_'+str(r)) # Search mask
                    setattr(self,'input_mask_'+str(r),None)
                    del paramSignature[i:i+2] # Delete mask
                except:
                    None
                try: # Add corners to current region
                    i=paramSignature.index('ROI_'+str(r)) # Search current region
                    paramSignature[i+1]=Choice(('Delete region','auto_'+str(r))\
                                              ,('Rectangular ROI (from coordinates)','corners_'+str(r))\
                                              ,('Binary mask (from image)','mask_'+str(r))) # Change choice by default
                    paramSignature.insert(i+2,'corner0_'+str(r)) # Insert top left-hand corner input
                    paramSignature.insert(i+3,String()) # Insert corner type
                    paramSignature.insert(i+4,'corner1_'+str(r)) # Insert bottom right-hand corner input
                    paramSignature.insert(i+5,String()) # Insert corner type
                except:
                    None
                try: # Test if next region already exists
                    paramSignature.index('ROI_'+str(r+1)) # Search next region
                    signature=Signature(*paramSignature) # New signature recovery
                    self.changeSignature(signature) # Apply new signature
                    setattr(self,'corner0_'+str(r),'(,)') # First corner initialization
                    setattr(self,'corner1_'+str(r),'(,)') # Second corner initialization
                    self.addLink('data_graph','corner0_'+str(r),self.initDataGraph)
                    self.addLink('data_graph','corner1_'+str(r),self.initDataGraph)
                except: # If not, a region is added
                    i=paramSignature.index('ROI_'+str(r)) # Search current region
                    paramSignature.insert(i+6,'ROI_'+str(r+1)) # Insert next region key
                    paramSignature.insert(i+7,Choice(('Change to add new region','auto_'+str(r+1))\
                                                    ,('Rectangular ROI (from coordinates)','corners_'+str(r+1))\
                                                    ,('Binary mask (from image)','mask_'+str(r+1)))) # Insert next region type                                  
                    signature=Signature(*paramSignature) # New signature recovery
                    self.changeSignature(signature) # Apply new signature
                    setattr(self,'corner0_'+str(r),'(,)') # First corner initialization
                    setattr(self,'corner1_'+str(r),'(,)') # Second corner initialization
                    self.addLink(None,'ROI_'+str(r+1),self.changeROI)
                    self.addLink('data_graph','corner0_'+str(r),self.initDataGraph)
                    self.addLink('data_graph','corner1_'+str(r),self.initDataGraph)
                    self.addLink('data_graph','ROI_'+str(r+1),self.initDataGraph) # Change on data_graph if change on ROI                                        
                    self.signature['ROI_'+str(r+1)].mandatory=0 # Current region can be optional 
                    
        if inp=='auto_'+str(r) and len(index_regions)>1: # If current region must be deleted
            try: # Test if current region was a rectangular ROI before change
                i=paramSignature.index('corner0_'+str(r))
                del paramSignature[i-2:i+4]
            except:
                None
            try: # Test if current region was a binary mask before change
                i=paramSignature.index('input_mask_'+str(r))
                del paramSignature[i-2:i+2]
            except:
                None
            signature=Signature(*paramSignature) # New signature recovery
            self.changeSignature(signature) # Apply new signature
            if len(index_regions)==2:
                self.signature['ROI_'+str(index_regions[-1])].mandatory=True     
                    
def initDataGraph( self,inp ):
    """Signature change and parameters initialization

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    # Variables initialization
    data_graph=None # Figure path initialization
    result=None # Value founded initialization
    filename='' # Filename variable initialization
    
    # Filename construction
    if self.conditions_file is not None: # If session is selected
        
        # Hierarchy recovery
        data_graph=self.conditions_file.hierarchyAttributes()
                              
        # Conditions list recovery
        cdt=''
        if self.conditions_list!='[,]':
            try:
                eval_cdt_list=eval(self.conditions_list) # Str to int
                if len(eval_cdt_list)==1 and type(eval_cdt_list[0])==int:
                    eval_cdt_list=[eval_cdt_list]
                for g in range(len(eval_cdt_list)): # For each group
                    cdt+='_c'
                    if type(eval_cdt_list[g])==int:
                        eval_cdt_list[g]=[eval_cdt_list[g]]
                    for c in range(len(eval_cdt_list[g])-1):
                        cdt+=str(eval_cdt_list[g][c])+'+'
                    cdt+=str(eval_cdt_list[g][len(eval_cdt_list[g])-1])
            except:
                None
                
        # Region recovery
        region='_over'
        index_regions=[]
        for k in range(1,len(self.signature.keys())+1):
            if self.signature.keys()[k-1][:-1]=='ROI_':
                index_regions.append(int(self.signature.keys()[k-1][-1]))
            if self.signature.keys()[k-1][:-2]=='ROI_':
                index_regions.append(int(self.signature.keys()[k-1][-2:]))
        for i in index_regions:          
            try:
                if str(getattr(self,'ROI_'+str(i)))[:4]=='mask' and getattr(self,'input_mask_'+str(i)) is not None:
                    if i!=index_regions[0]:
                        region+='_and'
                    region+='_'+os.path.basename(str(getattr(self,'input_mask_'+str(i)))[:-len(self.format)])
                if str(getattr(self,'ROI_'+str(i)))[:7]=='corners':
                    corner0=eval(getattr(self,'corner0_'+str(i)))
                    corner1=eval(getattr(self,'corner1_'+str(i)))
                    if i!=index_regions[0]:
                        region+='_and'
                    region+='_'+str(corner0[0])+'_'+str(corner0[1])+'_'+str(corner1[0])+'_'+str(corner1[1])
            except:
                None
                
        # Model recovery
        model=self.model
            
        # Filename creation
        filename=model+cdt+region
        
        # Path location
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
    if result is not None:
        return result # While opening process, result is not created
    else:
        return data_graph

def initModel( self,inp ):
    """Signature change and parameters initialization

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    paramSignature=[]
    for k,v in self.signature.items():
        paramSignature.append(k)
        paramSignature.append(v) 
    if self.model=='GLM':
        paramSignature[-1]=WriteDiskItem( 'OI GLM Data Graph', 'PNG image' )
    else:
        paramSignature[-1]=WriteDiskItem( 'OI BkSD Data Graph', 'PNG image' )
    signature=Signature(*paramSignature) # New signature recovery
    self.changeSignature(signature) # Apply new signature
    # Permissions
    self.signature['data_graph'].browseUserLevel=2 # Browse only visible for expert user

def initialization( self ):
    """Parameters values initialization
    """
    # Permissions
    self.signature['conditions_file'].browseUserLevel=2 # Browse only visible for expert user
    self.signature['data_graph'].browseUserLevel=2 # Browse only visible for expert user
    
    # Parameters initialization
    self.conditions_list='[,]' # Condition list initialization
    
    # Links
    self.addLink(None,'model',self.initModel)
    
    self.addLink(None,'conditions_file',self.initAnalysisName) # Change on signature if change on conditons_file
    self.addLink(None,'model',self.initAnalysisName) # Change on signature if change on model
    self.addLink(None,'ROI_1',self.changeROI) # Change on signature if change on ROI_1
    
    self.addLink('data_graph','conditions_file',self.initDataGraph) # Change on data_graph if change on conditions_file
    self.addLink('data_graph','analysis_name',self.initDataGraph) # Change on data_graph if change on analysis_name
    self.addLink('data_graph','model',self.initDataGraph) # Change on data_graph if change on model    
    self.addLink('data_graph','conditions_list',self.initDataGraph) # Change on data_graph if change on conditions_list
    self.addLink('data_graph','ROI_1',self.initDataGraph) # Change on data_graph if change on ROI   
    
    # First region value can be None initially
    setattr(self,'ROI_1',None)
    
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

    # ROIs recovery
    rois_list=[]
    for k in range(len(self.signature.keys())):
        if self.signature.keys()[k][:-1]=='corner0_' or self.signature.keys()[k][:-2]=='corner0_':
            # Top left-hand corner recovery
            try:
                c0=eval(str(getattr(self,self.signature.keys()[k])))
            except SyntaxError:
                raise SyntaxError('Top left-hand corner is not properly completed')
            try:
                if len(c0)==2:
                    corner0=c0
                else:
                    raise SyntaxError('Top left-hand corner is not properly completed')        
            except TypeError:
                raise TypeError('Top left-hand corner is not properly completed') 
            # Bottom right-hand corner recovery    
            try:
                c1=eval(str(getattr(self,self.signature.keys()[k+1])))
            except SyntaxError:
                raise SyntaxError('Bottom right-hand corner is not properly completed')
            try:
                if len(c1)==2:
                    corner1=c1
                else:
                    raise SyntaxError('Bottom right-hand corner is not properly completed')        
            except TypeError:
                raise TypeError('Bottom right-hand corner is not properly completed')
            rois_list.append((corner0,corner1))
        if self.signature.keys()[k][:-1]=='input_mask_' or self.signature.keys()[k][:-2]=='input_mask_':
            rois_list.append(str(getattr(self,self.signature.keys()[k])))
    
    # Blank based suffix and model recovery
    blank_based_suffix=''
    model='glm_based'
    if self.model=='BkS':
        model='blank_based'
        blank_based_suffix='_f0d_bks'
    if self.model=='BkSD':
        model='blank_based'
        blank_based_suffix='_f0d_bks_d'
    
    oisession_postprocesses.comparison_of_rois_process(
        attributes['_database'],
        attributes['protocol'],
        attributes['subject'],
        'session_'+attributes['session_date'],
        model+str(self.analysis_name),
        eval_cdt_list,
        blank_based_suffix,      
        rois_list,
        format=self.format,
        data_graph=self.data_graph.fullPath().encode('utf8'),
        context=context,
        )      