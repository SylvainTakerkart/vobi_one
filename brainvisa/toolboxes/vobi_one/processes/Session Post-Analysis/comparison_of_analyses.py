# Author: Flavien Garcia <flavien.garcia@free.fr>
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Compares the mean response of several analyses over the same region.
# Each analyse include its model (GLM, BkS or BkSD), its conditions file and 
# its conditions list.
# Possibility to average over a rectangular ROI or a binary mask.


# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path

try:
    import numpy as np # Needed to use matrix and list
except ImportError:
    raise ValidationError(_t_('Impossible to import numpy')) # Raises an exception

# Header
name = _t_('Comparison of Analyses') # Process name in the GUI
category = _t_('Session Post-Analysis') # Category name in the GUI
userLevel=0 # Always visible

# The parameters
signature=Signature(
    'format', Choice(('<auto>','.nii')\
                    ,('NIFTI-1 image','.nii')\
                    ,('gz compressed NIFTI-1 image','.nii.gz')), # Saving format of images. It can be NIFTI-1 Image ('.nii') or gzip compressed NIFTI-1 Image ('.nii.gz')
    'ROI', Choice(('Rectangular ROI (from coordinates)','corners')\
                            ,('Binary mask (from image)','mask') ), # Way to average images. It can be with corners (top left-hand and bottom right-hand) or with a mask (binary matrix)
    'corner0', String(), # The position of the top left-hand corner of the mask (x,y)
    'corner1', String(), # The position of the bottom right-hand corner of the mask (x,y)
    'model_1', Choice(('Change to add a new analysis','auto_1')\
                     ,('Linear Model (GLM)','GLM_1')\
                     ,('Blank Subtraction (BkS)','BkS_1')\
                     ,('Blank Subtraction + Detrending (BkSD)','BkSD_1')), # Model choice
    'data_graph', WriteDiskItem( 'OI Analysis Data Graph','PNG image' ), # The data graph path
    ) 

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
            
def changeAnalysis( self,inp ):
    """Signature change and parameters initialization

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    # Recovery of available analysis
    index_analysis=[] # List of condition file'index initialization
    for k in range(1,len(self.signature.keys())+1): # For each signature's key
        if self.signature.keys()[k-1][:-1]=='model_': # If key is a condition file with a digit index
            index_analysis.append(int(self.signature.keys()[k-1][-1])) # Add index of this condition file
        if self.signature.keys()[k-1][:-2]=='model_': # If key is a condition file with a number index
            index_analysis.append(int(self.signature.keys()[k-1][-2:])) # Add index of this condition file
            
    paramSignature=[] # New signature initialization
    for k,v in self.signature.items(): # For each item
        paramSignature.append(k) # Add the key
        paramSignature.append(v) # Add the value
       
    # Apply changes       
    for a in index_analysis: # For each available analysis
        
        if inp in ['GLM_'+str(a),'BkS_'+str(a),'BkSD_'+str(a)]: # If model selected
            try: # Test if this analysis already exists
                i=paramSignature.index('conditions_file_'+str(a)) # Find index of conditions file input
                signature=Signature(*paramSignature) # New signature recovery
                self.changeSignature(signature) # Apply new signature
            except: # If not, it is created
                i=paramSignature.index('model_'+str(a)) # Find index of model choice input
                paramSignature[i+1]=Choice(('Delete this analysis','auto_'+str(a))\
                                          ,('Linear Model (GLM)','GLM_'+str(a))\
                                          ,('Blank Subtraction (BkS)','BkS_'+str(a))\
                                          ,('Blank Subtraction + Detrending (BkSD)','BkSD_'+str(a))) # Change models choices to can delete it
                paramSignature.insert(i+2,'conditions_file_'+str(a)) # Add conditions file input
                paramSignature.insert(i+3,ReadDiskItem( 'Trials+conditions list' , 'Text file' )) # Insert conditions file type
                paramSignature.insert(i+4,'analysis_name_'+str(a)) # Analysis name input
                paramSignature.insert(i+5,Choice(('Choose an analysis name',None))) # The name of the analysis
                paramSignature.insert(i+6,'conditions_list_'+str(a)) # Add conditions list input
                paramSignature.insert(i+7,String()) # Add conditions list type
                paramSignature.insert(i+8,'model_'+str(a+1)) # Add model choice input
                paramSignature.insert(i+9,Choice(('Change to add a new analysis','auto_'+str(a+1))\
                                                ,('Linear Model (GLM)','GLM_'+str(a+1))\
                                                ,('Blank Subtraction (BkS)','BkS_'+str(a+1))\
                                                ,('Blank Subtraction + Detrending (BkSD)','BkSD_'+str(a+1)))) # Insert model choice type
                signature=Signature(*paramSignature) # New signature recovery
                self.changeSignature(signature) # Apply new signature
                
                # Links
                self.addLink(None,'model_'+str(a+1),self.changeAnalysis) # Change on signature if change on next model               
                self.addLink(None,'model_'+str(a),self.initAnalysisName)
                self.addLink(None,'conditions_file_'+str(a),self.initAnalysisName) # Change on next analysis_name if change on next conditions_file
                self.addLink('data_graph','model_'+str(a+1),self.initDataGraph) # Change on data_graph if change on next model
                self.addLink('data_graph','conditions_file_'+str(a),self.initDataGraph) # Change on data_graph if change on current conditions_file        
                self.addLink('data_graph','analysis_name_'+str(a),self.initDataGraph) # Change on data_graph if change on current analysis_name 
                self.addLink('data_graph','conditions_list_'+str(a),self.initDataGraph) # Change on data_graph if change on current conditions_list                
                self.signature['model_'+str(a+1)].mandatory=0
                setattr(self,'conditions_list_'+str(a),'[,]')
                
        elif inp=='auto_'+str(a) and len(index_analysis)>1: # If user wants to delete an analysis and if it is not the only one
            try: # Test if model already exists and delete it
                i=paramSignature.index('model_'+str(a))
                del paramSignature[i:i+8]
                signature=Signature(*paramSignature) # New signature recovery
                self.changeSignature(signature) # Apply new signature                
            except:
                None
                
def initAnalysisName( self,inp ):
    """Analysis name choice autocompletion

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    # Recovery of available analysis
    index_analysis=[] # List of condition file'index initialization
    for k in range(1,len(self.signature.keys())+1): # For each signature's key
        if self.signature.keys()[k-1][:-1]=='model_': # If key is a condition file with a digit index
            index_analysis.append(int(self.signature.keys()[k-1][-1])) # Add index of this condition file
        if self.signature.keys()[k-1][:-2]=='model_': # If key is a condition file with a number index
            index_analysis.append(int(self.signature.keys()[k-1][-2:])) # Add index of this condition file
            
    paramSignature=[] # New signature initialization
    for k,v in self.signature.items(): # For each item
        paramSignature.append(k) # Add the key
        paramSignature.append(v) # Add the value

    # Apply changes       
    for a in index_analysis: # For each available analysis
        if getattr(self,'model_'+str(a)) is not None:
            if getattr(self,'conditions_file_'+str(a)) is not None and getattr(self,'model_'+str(a)) is not None:
                source=os.path.join(os.path.split(os.path.split(str(getattr(self,'conditions_file_'+str(a))))[0])[0],'oisession_analysis')
                directory_list=os.listdir(source)
                name_list=[('Choose an analysis name',None)]
                if str(getattr(self,'model_'+str(a)))=='GLM_'+str(a):
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
                        
                i=paramSignature.index('analysis_name_'+str(a))
                prec=str(getattr(self,'analysis_name_'+str(a)))
                setattr(self,'analysis_name_'+str(a),None)
                paramSignature[i+1]=Choice()
                paramSignature[i+1].setChoices(*name_list)
                signature=Signature(*paramSignature) # List to Signature
                self.changeSignature(signature) # Apply new signature
                self.addLink('data_graph','analysis_name_'+str(a),self.initDataGraph) # Change on data_graph if change on analysis_name               
                if (prec,prec) in name_list:
                    setattr(self,'analysis_name_'+str(a),prec)
                    
def initDataGraph( self,inp ):
    """Figure file path autocompetion

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    # Variables initialization
    data_graph=None # Figure path initialization
    result=None # Value founded initialization
    filename='' # Filename variable initialization
    
    # Region recovery
    region=''
    if self.ROI=='mask' and self.input_mask is not None:
        region+='Over_'+os.path.basename(str(self.input_mask)[:-len(self.format)])+'_'
    else:
        try:
            corner0=eval(self.corner0)
            corner1=eval(self.corner1)
            region+='Over_'+str(corner0[0])+'_'+str(corner0[1])+'_'+str(corner1[0])+'_'+str(corner1[1])+'_'
        except:
            None
    
    filename+=region        
    # Recovery of available analysis
    index_analysis=[] # List of condition file'index initialization
    for k in range(1,len(self.signature.keys())+1): # For each signature's key
        if self.signature.keys()[k-1][:-1]=='conditions_file_': # If key is a condition file with a digit index
            index_analysis.append(int(self.signature.keys()[k-1][-1])) # Add index of this condition file
        if self.signature.keys()[k-1][:-2]=='conditions_file_': # If key is a condition file with a number index
            index_analysis.append(int(self.signature.keys()[k-1][-2:])) # Add index of this condition file
           
    # Filename construction
    for a in index_analysis:
        if a!=index_analysis[0]:
            filename+='_and_'
        # Model recovery
        model=''
        model_selected=str(getattr(self,'model_'+str(a)))
        if model_selected!='auto_'+str(a):
            if model_selected[-2]=='_':
                model+='on_'+model_selected[:-2]
            else:
                model+='on_'+model_selected[:-3]
        filename+=model
        
        try:
            if getattr(self,'conditions_file_'+str(a)) is not None: # If session is selected
                data_graph={}
                # Hierarchy recovery
                cut=os.path.split(os.path.split(str(getattr(self,'conditions_file_'+str(a))))[0])[0]
                data_graph['session_date']=os.path.split(cut)[1][-6:]
                cut2=os.path.split(cut)[0]
                data_graph['subject']=os.path.split(cut2)[1]
                cut=os.path.split(cut2)[0]
                data_graph['protocol']=os.path.split(cut)[1]
                data_graph['_database']=os.path.split(cut)[0]
                filename+='_session_'+data_graph['session_date']
                if getattr(self,'analysis_name_'+str(a)) is not None:
                    filename+='_analysis'+str(getattr(self,'analysis_name_'+str(a)))
                data_graph['_ontology']=self.conditions_file_1['_ontology']
        except:
            None
                      
        # Conditions list recovery
        cdt=''
        if getattr(self,'conditions_list_'+str(a))!='[,]':
            try:
                eval_cdt_list=eval(str(getattr(self,'conditions_list_'+str(a)))) # Str to int
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
 
        # Filename completion
        filename+=cdt
        
    # Path location
    if data_graph is not None:
        data_graph['filename_variable']=filename
        
    result=WriteDiskItem( 'OI Analysis Data Graph', 'PNG image' ).findValue( data_graph )
    if result is not None:
        return result # While opening process, result is not created
    else:
        return data_graph
    
def initialization( self ):
    """Parameters values initialization
    """
    # Parameters initialization
    self.signature['data_graph'].browseUserLevel=2 # Browse only visible for expert user
    self.conditions_list_1='[,]' # Condition list initialization
    self.corner0='(,)'
    self.corner1='(,)'   
    
    # Links
    self.addLink(None,'ROI',self.changeROI) # Change on signature if change on ROI
    
    self.addLink('data_graph','ROI',self.initDataGraph) # Change on data_graph if change on ROI
    self.addLink('data_graph','corner0',self.initDataGraph) # Change on data_graph if change on ROI 
    self.addLink('data_graph','corner1',self.initDataGraph) # Change on data_graph if change on ROI 
    self.addLink(None,'model_1',self.changeAnalysis) # Change on signature if change on model
    self.addLink('data_graph','model_1',self.initDataGraph) # Change on data_graph if change on model  
    
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
    
    # Mask recovery
    try:
        path_mask=self.input_mask.fullPath().encode('utf8')
    except:
        path_mask=None

    # Analysis informations recovery
    index_analysis=[] # List of condition file'index initialization
    for k in range(1,len(self.signature.keys())+1): # For each signature's key
        if self.signature.keys()[k-1][:-1]=='conditions_file_': # If key is a condition file with a digit index
            index_analysis.append(int(self.signature.keys()[k-1][-1])) # Add index of this condition file
        if self.signature.keys()[k-1][:-2]=='conditions_file_': # If key is a condition file with a number index
            index_analysis.append(int(self.signature.keys()[k-1][-2:])) # Add index of this condition file
    
    attributes_list=[]
    for a in index_analysis:
        attributes={}
        model=str(getattr(self,'model_'+str(a)))
        if model[:3]=='GLM':
            model='glm_based'
            blank_based_suffix=''
        elif model[:4]=='BkSD':
            model='blank_based'
            blank_based_suffix='_f0d_bks_d'
        else:
            model='blank_based'
            blank_based_suffix='_f0d_bks'
        # Hierarchy recovery
        path_cond=str(getattr(self,'conditions_file_'+str(a)))
        cut=os.path.split(os.path.split(path_cond)[0])[0]
        attributes['session_date']=os.path.split(cut)[1][-6:]
        cut2=os.path.split(cut)[0]
        attributes['subject']=os.path.split(cut2)[1]
        cut=os.path.split(cut2)[0]
        attributes['protocol']=os.path.split(cut)[1]
        attributes['_database']=os.path.split(cut)[0]       
        attributes['analysis_name']=model+str(getattr(self,'analysis_name_'+str(a)))
        attributes['blank_based_suffix']=blank_based_suffix
        # Conditions list recovery
        try:
            attributes['conditions_list']=sorted(eval(str(getattr(self,'conditions_list_'+str(a)))))
        except SyntaxError:
            raise SyntaxError('Conditions list of the analysis number'+str(a)+'is not properly completed')
        attributes_list.append(attributes)
    
    if type(attributes_list[0])!=dict:
        attributes_list=[attributes_list]
    
    oisession_postprocesses.comparison_of_analyses_process(
        attributes_list,    
        corner0=corner0,
        corner1=corner1,
        path_mask=path_mask,
        format=self.format,
        data_graph=self.data_graph.fullPath().encode('utf8'),
        context=context,
        )   
