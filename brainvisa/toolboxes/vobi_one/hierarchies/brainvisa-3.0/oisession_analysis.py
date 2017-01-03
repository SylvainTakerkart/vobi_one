# Author: Philippe Katz <philippe.katz@gmail.com>,
#	  Flavien Garcia <flavien.garcia@free.fr>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Session-level directories
oisession_analysis = (
    'glm_based{secondlevel_analysis}',SetType('Secondlevel GLM Directory'), # GLM-based directory
    SetContent(
        's{session_date}_glm_based{secondlevel_analysis}_denoised_*_mean', SetType( 'OI 2D+t GLM Denoised Mean' ), # Averaged image denoised using the Linear Model
        'glm', SetType( 'OI GLM Design Matrix' ), # Linear Model
        'param', SetType( 'OI GLM Parameters' ), # Parameters
        '*', SetType( 'OI GLM Time Series' ), # Region averaged data
	'*', SetType ( 'OI GLM Data Graph' ), # PNG figure
        ),
    'blank_based{secondlevel_analysis}',SetType('Secondlevel Blank Directory'), # Blank-based directory
    SetContent(
        's{session_date}_blank_based{secondlevel_analysis}_bksd_*_mean', SetType( 'OI 2D+t BkSD Mean' ), # Averaged image denoised using the BkSD method
        '*', SetType( 'OI BkSD Time Series' ), # Region averaged data
	'*', SetType ( 'OI BkSD Data Graph' ), # PNG figure
        ),
    'raw', # Averaged raw directory
    SetContent(
        's{session_date}_raw_*_mean', SetType( 'OI 2D+t Blank Mean' ), # Averaged raw image
        '*', SetType( 'OI Blank Time Series' ), # Region averaged data
	'*', SetType ( 'OI Blank Data Graph' ), # PNG figure
        ),
    'mask', # Mask directory
    SetContent(
        'mask_*', SetType( 'OI Mask' ), # Region Of Interest Mask
        ),
    )
