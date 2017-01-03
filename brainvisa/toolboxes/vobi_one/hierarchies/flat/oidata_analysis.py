# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

include( 'base' ) # BrainVISA base
include( 'oitrials_analysis' ) # Trial-level directories
include( 'oisession_analysis' ) # Session-level directories

# oi-brainvisa-tbx hierarchy
hierarchy=(
    SetWeakAttr( 'database', '%f' ),
    SetContent(
        '*', SetType('Database Cache file'), # the database directory contains files of type "Database Cache file"
        '{protocol}', # The protocol directory
        SetContent(
            '{subject}',SetType('Subject'), # The subject drectory
            SetContent(
                'session_{session_date}',SetFileNameStrongAttribute( '20' ), # The session directory
                SetContent( 
                    'oitrials_analysis', # Trial-level directories
                    SetContent( *oitrials_analysis ),
                    'oisession_analysis', # Session-level directories
                    SetContent( *oisession_analysis ),
                    ),
		'*',SetType('OI Analysis Data Graph'),
                ),
            ),
        ),
    )
