"""
====================
HMI plotting example
====================
In this example it is going to be demonstrated how to download and plot data 
from HMI. For this example we will use the LOS_magnetic_field but any other HMI
product can be similarly be accessed just by changing the Physical Observables
(PHYSOBS) keyword on the search. 

Useful links:
The list with HMI keys for PHYSOBS_.
.. _PHYSOBS: https://sdac.virtualsolar.org/cgi/show_details?keyword=PHYSOBS

Finding and downloading data using fido_.
.. _fido: https://docs.sunpy.org/en/stable/guide/acquiring_data/fido.html#downloading-data

Jsoc and VSO attributes for searches and filtering searches_.
.. _searches: https://docs.sunpy.org/en/stable/code_ref/net.html#
"""
###############################################################################
#Importing the required modules.
import matplotlib.pyplot as plt
import sunpy.map
from sunpy.net import Fido, attrs as a
import astropy.units as u

###############################################################################
# Downloading data with fido
# For this example we will specify time range, sample, instrument and the 
# Observation type. If you want however to further refine your seach you can 
# check other attributes that can be used in a Fido search_. 
# .. _search: https://docs.sunpy.org/en/stable/code_ref/net.html#module-sunpy.net.vso.attrs
# We will set a time range from 2015/11/04 12:00:00' to '2015/11/04 13:00:00 for
# HMI LOS magnetic field where our images will be spaced every 720 seconds.
result = Fido.search(a.Time('2015/11/04 12:00:00', '2015/11/04 13:00:00'),
                     a.Instrument('hmi'),
                     a.Sample(720*u.s),
                     a.vso.Physobs('LOS_magnetic_field'))

# checking what results we obtained from our search
print(result)

# Once we are happy with the results obtained from the search we can use them to
# download the data with Fido.fetch . Each file will be stored in the directory
# defined by the path and they will be named with the filename {file} obtained
# in our results.
downloaded_files = Fido.fetch(result, path = '/APath/{file}.fits')

# The downloaded_files variables returns a list with the path for each file 
# that was downloaded as we can see by printing the variable.
print(downloaded_files)

###############################################################################
# Now we are going to create a sunpy.Map object out of one of our results
hmi_map = sunpy.map.Map(downloaded_files[0])

###############################################################################
# Once we have the map object plotting it is quite simple.
# First we define a figure object and an axes for it.
fig, ax = plt.subplots()

# Now we plot our map on the axes we created
hmi_map.plot(axes = ax)

# Finally we can see our map
plt.show()
