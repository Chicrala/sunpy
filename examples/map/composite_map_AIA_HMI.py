# -*- coding: utf-8 -*-
"""
=========================================
Composite map
=========================================
In this example we make a composite map out
of images provided by AIA and HMI.
"""

##############################################################################
# Start by importing the necessary modules.

import matplotlib.pyplot as plt

import sunpy.map
import sunpy.data.sample

#this should be gone when the HMI data is added
#to the examples folder
from sunpy.net import Fido, attrs as a
from sunpy.net import jsoc

##############################################################################

#downloading the "missing" data
#the AIA data timestamp we need to
#match is 20110607 063302
def download(tstart = '2011/06/07 06:32:45', tend = '2011/06/07 06:33:15'):
    '''
    This function will download the
    data using fido and return
    the data.

    This way only the final result 
    will stay on the main function
    namespace until this bit get
    deleted.

    The default values for tstart
    and tend are the closest to
    match the AIA 171 file on the 
    examples folder.
    '''

    #using Fido search to look for results
    res = Fido.search(a.jsoc.Time(tstart, tend),
                      #specifying the data series
                      #which, in this case, is the
                      #hmi Line-Of-sight B
                      a.jsoc.Series('hmi.M_45s'),
                      #adding my email to be notified
                      #this is mandatory and the email
                      #must be registered with JSOC
                      a.jsoc.Notify('andrechicrala@gmail.com'), #<<change later

                      #setting the harpnumber as primekey
                      #for this search
                      #a.jsoc.PrimeKey('HARPNUM', str(harpnum)),

                      #specifying which segments will be
                      #queried. We want the magnetogram.
                      #a.jsoc.Segment('magnetogram'))
                     )

    #downloading the data
    downloaded_files = Fido.fetch(res,
                                  path='/Users/andrechicrala/Downloads/testfido/{file}.fits')  
    
    return()

##############################################################################
# Sunpy sample data contains a number of suitable maps, for this example we
# will use both AIA 171 and HMI magnetogram
aia_map = sunpy.map.Map(sunpy.data.sample.AIA_171_IMAGE)

#using the data I downloaded
hmi_map = sunpy.map.Map('/Users/andrechicrala/Downloads/testfido/hmi.m_45s.20110607_063300_TAI.2.magnetogram.fits')

#creating the composite map object
comp_map = sunpy.map.Map(aia_map, hmi_map, composite = True)

#drawing the countours over the hmi_map
#note that the hmi_map have index = 1
#according to our definition of comp_map
comp_map.set_levels(index = 1, levels = [-1000,-500,-250,250,500,1000])

#having a look at the map
comp_map.peek()

#It is also possible to set up the
#alpha-channel value for a layer in 
#the CompositeMap.
comp_map.set_alpha(index = 1, alpha = 0.5)

#having another look at the map
comp_map.peek()

##############################################################################
