# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@univ-amu.fr>
# License: BSD Style.

# Trial-level directories
oitrials_analysis = (
    'conditions',SetType( 'Trials+conditions list' ), # Conditions file : contains informations about datas
    'physio_params',SetType( 'Physiological parameters' ), #Physiological parameters file : contains informations about datas
    'exp{experience_number}', # The experience directory
    SetContent(
        'trial{trial_number}', # The trial directory
        SetContent(
            'raw', # Directory containing raw datas
            SetContent(
                '*' , SetType('OI Raw Imported Data'), # RAW image
                ),
            'glm_based{firstlevel_analysis}',SetType('Firstlevel GLM Directory'), # GLM-based directory
            SetContent(
                '*_denoised', SetType( 'OI GLM Denoised' ), # Denoised image using the Linear Model
                '*_residuals', SetType( 'OI GLM Residuals'), # Residual noise
                '*_betas', SetType( 'OI GLM Beta map' ), # Betas
                'glm', SetType( 'OI GLM Design Matrix' ), # Linear Model
                'glm_physio', SetType('OI GLM+physio param Design Matrix' ), # Linear Model+physio params
                'param', SetType( 'OI GLM Parameters' ), # Parameters
		'*', SetType( 'OI GLM Data Graph' ),# PNG Image
                ),
            'blank_based{firstlevel_analysis}',SetType('Firstlevel Blank Directory'), # Blank-based directory
            SetContent(
                '*', SetType( 'OI BkSD' ), # Denoised image using the BkSD method
                ),
            ),
        ),
    )
