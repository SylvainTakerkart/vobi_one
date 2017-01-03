# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

userLevel = 3 # Never visible

def standardize(instring):
	"""Standardization of input text

	Parameters
	----------
	instring : string
	    Input text

	Returns
	-------
	outstring : string
	    Output text
	"""
	outstring=instring.decode("utf-8") # Utf-8 decoding

	outstring=outstring.strip() # Spaces before and after text destruction
	outstring=outstring.replace(";",",") # Remplacement of ';' by ','
	outstring=outstring.replace(" ,",",") # Remplacement of ' ,' by ','
	outstring=outstring.replace(", ",",") # Remplacement of ', ' by ','
	outstring=outstring.replace(" ",",") # Remplacement of ' ' by ','

	return outstring.encode("utf-8") # Utf-8 encoding
