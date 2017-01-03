# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 14:14:28 2013

@author: takerkart
"""

import numpy as np
import pylab as pl



def compute_response(time, alpha):
    response = np.zeros(time.shape)
    
    # delay before the response starts: stays at zero
    c1=np.nonzero(time>alpha[a,0])
    
    # first part of the negative dip; amplitude is -beta = -alpha[,6]
    c2=np.nonzero(time>(alpha[a,0]+alpha[a,1]))
    response[c1[0][0]:c2[0][0]] = alpha[a,6] * (np.cos(np.pi*((time[c1[0][0]:c2[0][0]]-alpha[a,0])/alpha[a,1])) - 1 ) / 2
    
    # rise from negative dip to plateau; amplitude of plateau is +1
    c3=np.nonzero(time>(alpha[a,0]+alpha[a,1]+alpha[a,2]))
    response[c2[0][0]:c3[0][0]] = (1 - alpha[a,6]) / 2 - (1 + alpha[a,6]) * np.cos(np.pi*((time[c2[0][0]:c3[0][0]]-alpha[a,0]-alpha[a,1])/alpha[a,2])) / 2
    
    # plateau
    c4=np.nonzero(time>(alpha[a,0]+alpha[a,1]+alpha[a,2]+alpha[a,3]))
    response[c3[0][0]:c4[0][0]]=1.
    
    # decrease from plateau to second negative dip: amplitude of dip is -gamma = -alpha[,7]
    c5=np.nonzero(time>(alpha[a,0]+alpha[a,1]+alpha[a,2]+alpha[a,3]+alpha[a,4]))
    response[c4[0][0]:c5[0][0]] = (1 - alpha[a,7]) / 2 + (1 + alpha[a,7]) * np.cos(np.pi*((time[c4[0][0]:c5[0][0]]-alpha[a,0]-alpha[a,1]-alpha[a,2]-alpha[a,3])/alpha[a,4])) / 2
    
    # rise from second negative dip to rest activity (zero!)
    c6=np.nonzero(time>(alpha[a,0]+alpha[a,1]+alpha[a,2]+alpha[a,3]+alpha[a,4]+alpha[a,5]))
    response[c5[0][0]:c6[0][0]] = - alpha[a,7] * (1 + np.cos(np.pi*((time[c5[0][0]:c6[0][0]]-alpha[a,0]-alpha[a,1]-alpha[a,2]-alpha[a,3]-alpha[a,4])/alpha[a,5])) ) / 2
    
    return response

time = np.arange(0,1,0.01)

alpha = np.zeros([1,8])
a = 0;

pl.figure()

alpha[a,:] = [0.1,0.1,0.2,0.2,0.2,0.15,0.5,0.2]
response = compute_response(time,alpha)
pl.plot(response)

pl.tick_params(\
   axis='x',          # changes apply to the x-axis
   which='both',      # both major and minor ticks are affected
   bottom='off',      # ticks along the bottom edge are off
   top='off',         # ticks along the top edge are off
   labelbottom='off') # labels along the bottom edge are off
    
pl.xlabel('time')

pl.ylim(response.min()-0.3,response.max()+0.1)
ticks = np.arange(-0.5,1.1,0.25)
pl.yticks(ticks, ticks)

pl.figure()

alpha[a,:] = [0.1,0,0.2,0.3,0.3,0,0,0]
response = compute_response(time,alpha)
pl.plot(response)

alpha[a,:] = [0.1,0.1,0.2,0.2,0.2,0.15,0.7,0.2]
response = compute_response(time,alpha)
pl.plot(1.3 * response)

alpha[a,:] = [0.05,0.2,0.2,0,0.2,0.,1.4,0]
response = compute_response(time,alpha)
pl.plot(response)

alpha[a,:] = [0,0.3,0.3,0,0.2,0,0.8,0]
response = compute_response(time,alpha)
pl.plot(-response)

pl.tick_params(\
   axis='x',          # changes apply to the x-axis
   which='both',      # both major and minor ticks are affected
   bottom='off',      # ticks along the bottom edge are off
   top='off',         # ticks along the top edge are off
   labelbottom='off') # labels along the bottom edge are off
    
pl.xlabel('time')


