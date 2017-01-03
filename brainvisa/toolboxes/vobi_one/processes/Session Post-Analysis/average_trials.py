# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Flavien Garcia <flavien.garcia@free.fr>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Averages a list of images using the condition file created using cond_file process

# Imports
from neuroProcesses import * # Provides a hierarchy to get object's path
import os

# Header
name = _t_('Average Trials')
category = _t_('Session Post-Analysis')
userLevel=0 # Always visible

# The parameters
signature=Signature(
    'format', Choice(('<auto>','.nii'),('NIfTI-1 image','.nii'),('gz compressed NIfTI-1 image','.nii.gz') ), # Saving format of images. It can be NIfTI-1 Image ('.nii') or gzip compressed NIfTI-1 Image ('.nii.gz')
    'conditions_file', ReadDiskItem( 'Trials+conditions list' , 'Text file' ), # The condition file path
    'analysis_type', Choice( ('Choose an analysis type',None)), # Analysis name : Raw, Glm-based or Blank-based
    'analysis_name', Choice(('Choose an analysis name',None)), # The name of the analysis
    'conditions_list', String(), # A tuple of list of condition which has to be averaged. Exemple : ([5,2],[4,]) The files which have for condtions 5 and 2 will be averaged together, the files which have for condition 4 will be averaged together.
    'blank_based_suffix', Choice(('No file available',None)), # The suffix of images' filename. Gives the processing algorithmes applied on this image. It can be : '_f0d' for frame0 division, '_f0s' for frame0 substraction, '_d' for linear detrend, '_bks' for blank substraction or  '_bkd' for blank division.
    'average_file',WriteDiskItem( 'OI 2D+t Mean Image' , ['NIfTI-1 image','gz compressed NIfTI-1 image']),
    )
    
def initAnalysisType( self,inp ):
    """Analysis type choice autocompletion

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    paramSignature=[] # New signature initialization
    for k,v in self.signature.items(): # For each item
        paramSignature.append(k) # Add the key
        paramSignature.append(v) # Add the value
        
    if self.conditions_file is not None:
        source=os.path.join(os.path.split(os.path.split(self.conditions_file.fullPath())[0])[0],'oisession_analysis')
        directory_list=os.listdir(source)
        
        type_list=[('Choose an analysis type',None)]
        for directory in directory_list:
            if directory[0:9]=='glm_based':
                try:
                    type_list.index(('Linear Model','glm_based'))
                except:
                    type_list.append(('Linear Model','glm_based'))
            elif directory[0:11]=='blank_based':
                try:
                    type_list.index(('Blank Subtraction (+ Detrending)','blank_based'))
                except:
                    type_list.append(('Blank Subtraction (+ Detrending)','blank_based'))                
            if directory[0:3]=='raw':
                try:
                    type_list.index(('Raw','raw'))
                except:
                    type_list.append(('Raw','raw'))

        try:
            i=paramSignature.index('analysis_type')
            paramSignature[i+1]=Choice()
            paramSignature[i+1].setChoices(*type_list)
            i=paramSignature.index('analysis_name')
            paramSignature[i+1]=Choice(('Choose an analysis name',None))
            signature=Signature(*paramSignature) # List to Signature
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
    self.conditions_list='[,]' # Condition list initialization
    paramSignature=[] # New signature initialization
    for k,v in self.signature.items(): # For each item
        paramSignature.append(k) # Add the key
        paramSignature.append(v) # Add the value
          
    if self.analysis_type is not None:
        source=os.path.join(os.path.split(os.path.split(self.conditions_file.fullPath())[0])[0],'oisession_analysis')
        directory_list=os.listdir(source)
        name_list=[('Choose an analysis name',None)]
        if self.analysis_type=='raw':
            try:
                i=paramSignature.index('analysis_name')
                del paramSignature[i:i+2]
                signature=Signature(*paramSignature) # List to Signature
                self.changeSignature(signature) # Apply new signature
            except:
                None     
        elif self.analysis_type=='blank_based':
            for directory in directory_list:
                if directory[0:11]=='blank_based' and directory[-5:]!='.minf':
                    try:
                        name_list.index((str(directory[11:]),str(directory[11:])))
                    except:
                        name_list.append((str(directory[11:]),str(directory[11:])))
           
            try:
                i=paramSignature.index('analysis_name')
                self.analysis_name=None
                del paramSignature[i+1]
                paramSignature.insert(i+1,Choice())
                paramSignature[i+1].setChoices(*name_list)
                signature=Signature(*paramSignature) # List to Signature
                self.changeSignature(signature) # Apply new signature
            except:
                i=paramSignature.index('analysis_type')
                self.analysis_name=None
                paramSignature.insert(i+2,'analysis_name')
                paramSignature.insert(i+3,Choice())
                paramSignature[i+3].setChoices(*name_list)
                signature=Signature(*paramSignature) # List to Signature
                self.changeSignature(signature) # Apply new signature
                self.addLink(None,'analysis_name',self.initBlankBasedSuffix) # Change on blank_based_suffix if change on analysis_name
                self.addLink('average_file','analysis_name',self.initAverageFile) # Change on average_file if change on analysis_name
            try: # Test if blank based suffix input exists
                i=paramSignature.index('blank_based_suffix')
            except:
                i=paramSignature.index('conditions_list')
                self.blank_based_suffix=None
                paramSignature.insert(i+2,'blank_based_suffix')
                paramSignature.insert(i+3,Choice())
                paramSignature[i+3].setChoices(('Choose a suffix for files',None))
                signature=Signature(*paramSignature) # List to Signature
                self.changeSignature(signature) # Apply new signature
                self.addLink('average_file','blank_based_suffix',self.initAverageFile) # Change on average_file if change on blank-based suffix
                
            
        elif self.analysis_type=='glm_based':
            for directory in directory_list:  
                if directory[0:9]=='glm_based' and directory[-5:]!='.minf':
                    try:
                        name_list.index((str(directory[9:]),str(directory[9:])))
                    except:
                        name_list.append((str(directory[9:]),str(directory[9:]))) 
            
            try:
                i=paramSignature.index('analysis_name')
                paramSignature[i+1]=Choice()
                paramSignature[i+1].setChoices(*name_list)
                signature=Signature(*paramSignature) # List to Signature
                self.changeSignature(signature) # Apply new signature
                
            except:
                i=paramSignature.index('analysis_type')
                self.analysis_name=None
                choice=Choice()
                choice.setChoices(*name_list)
                paramSignature.insert(i+2,'analysis_name')
                paramSignature.insert(i+3,choice)
                signature=Signature(*paramSignature) # List to Signature
                self.changeSignature(signature) # Apply new signature
                self.addLink(None,'analysis_name',self.initBlankBasedSuffix) # Change on blank_based_suffix if change on analysis_name
                self.addLink('average_file','analysis_name',self.initAverageFile) # Change on average_file if change on analysis_name
                
                
        elif self.analysis_type==None:
            paramSignature=['format', Choice(('<auto>','.nii'),('NIfTI-1 image','.nii'),('gz compressed NIfTI-1 image','.nii.gz') ), # Saving format of images. It can be NIfTI-1 Image ('.nii') or gzip compressed NIfTI-1 Image ('.nii.gz')
                            'conditions_file', ReadDiskItem( 'Trials+conditions list' , 'Text file' ), # The condition file path
                            'analysis_type', self.signature['analysis_type'], # Analysis name : Raw, Glm-based or Blank-based
                            'analysis_name', Choice(('Choose an analysis name',None)), # The name of the analysis
                            'conditions_list', String(), # A tuple of list of condition which has to be averaged. Exemple : ([5,2],[4,]) The files which have for condtions 5 and 2 will be averaged together, the files which have for condition 4 will be averaged together.
                            'blank_based_suffix', Choice(('No file available',None)), # The suffix of images' filename. Gives the processing algorithmes applied on this image. It can be : '_f0d' for frame0 division, '_f0s' for frame0 substraction, '_d' for linear detrend, '_bks' for blank substraction or  '_bkd' for blank division.
                            'average_file',WriteDiskItem( 'OI 2D+t Mean Image' , ['NIfTI-1 image','gz compressed NIfTI-1 image']),
                            ]
            signature=Signature(*paramSignature)
            self.changeSignature(signature) 
            self.addLink(None,'analysis_name',self.initBlankBasedSuffix) # Change on blank_based_suffix if change on analysis_name
            self.addLink('average_file','analysis_name',self.initAverageFile) # Change on average_file if change on analysis_name
            self.initialization()
    else:
        try:
            i=paramSignature.index('analysis_name')
            self.analysis_name=None
            paramSignature[i+1]=Choice(('Choose an analysis name',None))
            signature=Signature(*paramSignature)
            self.changeSignature(signature)
        except:
            None
        try:
            i=paramSignature.index('blank_based_suffix')
            self.blank_based_suffix=None
            paramSignature[i+1]=Choice(('No file available',None))
            signature=Signature(*paramSignature)
            self.changeSignature(signature)
        except:
            None
            
            
def initBlankBasedSuffix(self,inp ):
    """Blank based suffix choice autocompletion

    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    paramSignature=[] # New signature initialization
    for k,v in self.signature.items(): # For each item
        paramSignature.append(k) # Add the key
        paramSignature.append(v) # Add the value
       
    if self.analysis_type in ['raw','glm_based']:
        try:
            i=paramSignature.index('blank_based_suffix')
            self.blank_based_suffix=None
            del paramSignature[i:i+2]
            signature=Signature(*paramSignature) # List to Signature
            self.changeSignature(signature) # Apply new signature 
        except:
            None
            
    elif self.analysis_type=='blank_based' and self.conditions_list!='[,]':
        if self.analysis_name is not None:
            blank_based_suffix_list=[('Choose a suffix for files',None)]
            exp_list=os.listdir(os.path.split(self.conditions_file.fullPath())[0])
            file_number=0
            suffix_counter={'_f0d':0,'_f0d':0,'_f0s':0,'_f0d_bkd':0,'_f0s_bks':0,'_f0d_bks':0,'_f0s_bkd':0,'_f0d_bks_d':0,'_f0d_bkd_d':0,'_f0s_bkd_d':0,'_f0s_bks_d':0}
            for exp in exp_list:
                trial_list=[]
                if exp[0:3]=='exp':
                    trial_list=os.listdir(os.path.join(os.path.split(self.conditions_file.fullPath())[0],exp))
                for trial in trial_list:
                    source=os.path.join(os.path.split(self.conditions_file.fullPath())[0],exp,trial,'blank_based'+self.analysis_name)
                    file_list=os.listdir(source)
                    if eval(file_list[0][19:22]) in eval(self.conditions_list):
                        file_number+=1
                    
                    for f in file_list:
                        for sp in suffix_counter.keys():
                            if f[-len(sp+self.format):-len(self.format)]==sp and eval(f[19:22]) in eval(self.conditions_list):
                                suffix_counter[sp]+=1
            if file_number==0:
                blank_based_suffix_list=[('No file available with theses conditions',None)]
            else:                    
                for sp in suffix_counter.keys():
                    if suffix_counter[sp]==file_number:
                        blank_based_suffix_list.append((sp,sp))
            try:
                i=paramSignature.index('blank_based_suffix')
                paramSignature[i+1]=Choice()
                paramSignature[i+1].setChoices(*blank_based_suffix_list)
                signature=Signature(*paramSignature) # List to Signature
                self.changeSignature(signature) # Apply new signature 
            except:
                i=paramSignature.index('conditions_list')
                self.blank_based_suffix=None
                paramSignature.insert(i+2,'blank_based_suffix')
                paramSignature.insert(i+3,Choice())
                paramSignature[i+3].setChoices(*blank_based_suffix_list)
                signature=Signature(*paramSignature) # List to Signature
                self.changeSignature(signature) # Apply new signature
                self.addLink('average_file','blank_based_suffix',self.initAverageFile) # Change on average_file if change on blank-based suffix
        else:
            i=paramSignature.index('blank_based_suffix')
            self.blank_based_suffix=None
            paramSignature[i+1]=Choice(('Choose a suffix for files',None))
            signature=Signature(*paramSignature) # List to Signature
            self.changeSignature(signature) # Apply new signature      

def initAverageFile( self,inp ):
    """Average file path in output autocompletion
    
    Parameters
    ----------
    inp : BrainVISA parameter type
        The parameter whose changes will be tracked to autocomplete the others
    """
    average_file=None
    result=None
    if self.conditions_file is not None:
        # Format recovery
        if self.format!='.nii.gz':
            format='NIfTI-1 image'
        else:
            format='gz compressed NIfTI-1 image'
            
        average_file=self.conditions_file.hierarchyAttributes()
        
        
        # Conditions list recovery
        cdt=''
        if self.conditions_list!='[,]': # If user has modified the condtions list
            try:
                eval_cdt_list=sorted(eval(self.conditions_list))
                for c in range(len(eval_cdt_list)-1): # For each group
                    cdt+='c'
                    cdt+=str(eval_cdt_list[c]).zfill(3)+'_'
                cdt+='c'+str(eval_cdt_list[len(eval_cdt_list)-1]).zfill(3) # Last condition
            except:
                None
        
        # Blank based suffix recovery
        suffix=''
        if self.blank_based_suffix is not None:
            suffix=self.blank_based_suffix
        average_file['filename_variable']=cdt+suffix
        
        if self.analysis_name is not None:
            average_file['secondlevel_analysis']=self.analysis_name
            
        if self.analysis_type is not None:
            if self.analysis_type == 'glm_based':
                result=WriteDiskItem( 'OI 2D+t GLM Denoised Mean' , format ).findValue( average_file )
            if self.analysis_type == 'blank_based':
                result=WriteDiskItem( 'OI 2D+t BkSD Mean' , format ).findValue( average_file )        
            if self.analysis_type == 'raw':
                result=WriteDiskItem( 'OI 2D+t Blank Mean' , format ).findValue( average_file )   
    
    if result is not None:
        return result # While opening process, result is not created
    else:
        return None
        
def initialization( self ):
    """Parameters values initialization
    """
    self.signature['conditions_file'].browseUserLevel=2 # Browse only visible for expert user
    self.signature['average_file'].browseUserLevel=2 # Browse only visible for expert user

    # Links  
    self.addLink(None,'conditions_file',self.initAnalysisType) # Change on analysis_type if change on conditions_file

    self.addLink(None,'conditions_file',self.initAnalysisName) # Change on analysis_name if change on conditions_file
    self.addLink(None,'analysis_type',self.initAnalysisName) # Change on analysis_name if change on analysis_type

    self.addLink(None,'conditions_file',self.initBlankBasedSuffix) # Change on blank_based_suffix if change on conditions_file
    self.addLink(None,'analysis_type',self.initBlankBasedSuffix) # Change on blank_based_suffix if change on analysis_type
    self.addLink(None,'analysis_name',self.initBlankBasedSuffix) # Change on blank_based_suffix if change on analysis_name 
    self.addLink(None,'conditions_list',self.initBlankBasedSuffix) # Change on blank_based_suffix if change on conditions_list
    
    self.addLink('average_file','format',self.initAverageFile) # Change on average_file if change on format    
    self.addLink('average_file','conditions_file',self.initAverageFile) # Change on average_file if change on conditions_file
    self.addLink('average_file','analysis_type',self.initAverageFile) # Change on average_file if change on analysis_type   
    self.addLink('average_file','analysis_name',self.initAverageFile) # Change on average_file if change on analysis_name
    self.addLink('average_file','conditions_list',self.initAverageFile) # Change on average_file if change on conditions_file   
    self.addLink('average_file','blank_based_suffix',self.initAverageFile) # Change on average_file if change on blank-based suffix
    self.conditions_list='[,]' # Condition list initialization
        
def execution( self, context ):
    """The execution process
    
    Parameters
    ----------
    context : BrainVISA context
    """
    import oidata.oisession_postprocesses as oisession_postprocesses

    attributes=self.average_file.hierarchyAttributes() # Attributes recuperation
    
    # Analysis name recovery
    try:
        if self.analysis_type=='raw':
            analysis_name=self.analysis_type
        else:
            analysis_name=self.analysis_type+self.analysis_name
    except:
        analysis_name=None
        
    # Conditions list recovery
    try:
        eval_cdt_list=sorted(eval(self.conditions_list)) # Str to int list
    except SyntaxError:
        raise SyntaxError('Conditions list is not properly completed')
            
    # Blank based suffix recuperation
    try:
        if self.analysis_type=='blank_based':
            blank_based_suffix=self.blank_based_suffix
        else:
            blank_based_suffix=''
    except:
        blank_based_suffix=''
        
    # Averages a list of images using the condition file created using cond_file process
    oisession_postprocesses.average_trials_process(
        attributes['_database'],
        attributes['protocol'],
        attributes['subject'],
        'session_'+attributes['session_date'],
        analysis_name,
        (eval_cdt_list),
        mode=True,
        format=self.format,
        blank_based_suffix=blank_based_suffix,
        context=context, # BrainVISA context
        )
