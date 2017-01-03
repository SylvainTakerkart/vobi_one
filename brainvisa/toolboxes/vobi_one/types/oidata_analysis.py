# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

include( 'builtin' )
include( 'registration' )

Format( 'Numpy Dump file', "f|*.npz" ) # Numpy file format
Format( 'BLK Camera file', 'f|*.BLK' ) # BLK acquisition file format
Format( 'RSD Camera file', 'f|*.rsd' ) # RSD acquisition file format

FileType( 'OI 2D+t Image', '4D Volume') # Generic 2D + time file type
FileType( 'OI 2D Map', '4D Volume' ) # Map file type (2D)

FileType( 'OI Raw Imported Data', 'OI 2D+t Image' ) # RAW image file type
FileType( 'OI GLM Denoised', 'OI 2D+t Image' ) # GLM denoised image file type
FileType( 'OI GLM Residuals', 'OI 2D+t Image' ) # GLM residuals image file type

FileType( 'OI BKSD','OI 2D+t Image' ) # BkSD denoised image file type 

FileType( 'OI 2D+t Mean Image', 'OI 2D+t Image' ) # Averaged image file type
FileType( 'OI 2D+t GLM Denoised Mean', 'OI 2D+t Mean Image' ) # GLM denoised averaged image file type
FileType( 'OI 2D+t BkSD Mean', 'OI 2D+t Mean Image') # BkSD denoised averaged image file type 
FileType( 'OI 2D+t Blank Mean', 'OI 2D+t Mean Image') # RAW image averaged file type

FileType( 'OI GLM Beta map', 'OI 2D Map' ) # Betas file type
FileType( 'OI Mask', 'OI 2D Map' ) # Region of Interest Mask file type

FileType( 'OI Data', 'Any Type' ) # Optical Imaging Datas

FileType( 'OI GLM Data', 'OI Data' ) # Linear Model datas file type
FileType( 'OI BLK Camera File', 'OI Data' ) # BLK acquisition file type
FileType( 'OI RSD Camera File', 'OI Data' ) # RSD acquisition file type
FileType( 'OI Time Series', 'OI Data' ) # Region averaged data file type
FileType ('OI Data Graph', 'OI Data' ) # Figure file type


FileType( 'OI GLM Time Series', 'OI Time Series' )  # GLM denoised region averaged image file type
FileType( 'OI BkSD Time Series', 'OI Time Series' ) # BkSD denoised region averaged image file type 
FileType( 'OI Blank Time Series', 'OI Time Series' ) # RAW image region averaged file type

FileType ('OI GLM Data Graph', 'OI Data Graph' ) # Figure file type
FileType ('OI BkSD Data Graph', 'OI Data Graph' ) # Figure file type
FileType ('OI Blank Data Graph', 'OI Data Graph' ) # Figure file type
FileType ('OI Analysis Data Graph', 'OI Data Graph' ) # Figure file type

FileType( 'OI GLM Design Matrix', 'OI GLM Data' ) # Linear Model file type
FileType( 'OI GLM+physio param Design Matrix', 'OI GLM Data' ) # Linear Model file including regressors from this trial's physiological parameters
FileType( 'OI GLM Parameters', 'OI GLM Data' ) # Parameters file type

FileType( 'Trials+conditions list', 'Text file' ) # Condition list file type
FileType( 'Unimported physiological parameters', 'Text file' ) # Unimported physiological parameters file type
FileType( 'Physiological parameters', 'Text file' ) # Physiological parameters file type

HierarchyDirectoryType( 'OI Directory' ) # oi-brainvisa-tbx directories
FileType( 'Firstlevel Analysis','OI Directory') # Trial-level analysis directory
FileType( 'Firstlevel GLM Directory', 'Firstlevel Analysis') # GLM-based trial-level analysis directory
FileType( 'Firstlevel Blank Directory', 'Firstlevel Analysis') # BkSD-based trial-level analysis directory

FileType( 'Secondlevel Analysis','OI Directory') # Session-level analysis directory
FileType( 'Secondlevel GLM Directory', 'Secondlevel Analysis') # GLM-based session-level analysis directory
FileType( 'Secondlevel Blank Directory', 'Secondlevel Analysis') # BkSD-based session-level analysis directory
