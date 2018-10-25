# -*- coding: utf-8 -*-
"""
=========================================
Composite map
=========================================
In this example we make a composite map out
of images provided by AIA and HMI.

"""
#importing the relevant packages
import sunpy.map
import sunpy.data.sample
#from astropy.wcs import WCS
#from astropy.io import fits
#from wcsaxes import datasets

#import numpy as np

import matplotlib.pyplot as plt

###########
    
def layers():
    '''
    This functions takes two different arrays
    and overplot them being the second a contourplot.
    '''
    
    #opening the AIA sample image
    #header data unit!
    aia = sunpy.map.Map(sunpy.data.sample.AIA_171_IMAGE)
    #taking the aia wcs (world coordinate system)
    #aia_wcs = aia.wcs
    aia.draw_limb()
    
    hmi = sunpy.map.Map(sunpy.data.sample.HMI_LOS_IMAGE)
    
    #creating the figure object
    fig = plt.figure()
    #adding an axe to it, an empty figure basically
    #with AIA projection
    ax = fig.add_axes([1,1,1,1])#, projection = aia.wcs)
    #configuring the axis limits
    #ax.set_xlim(-0.5, aia.data.shape[1] - 0.5)
    #ax.set_ylim(-0.5, aia.data.shape[0] - 0.5)
    
    #showing the AIA image
    ax.imshow(aia.data, **aia.plot_settings)
    
    #defining the contourlevels of hmi
    ax.contour(hmi.data, transform = ax.get_transform(aia.wcs),
               levels = [-500,500], colors = 'white', alpha = 0.75)
    
    #show fig
    plt.show(fig)
    
    return(fig)


if __name__ == '__main__':
    '''
    testing zone
    '''
    print('lol')    
    fig = layers()
    