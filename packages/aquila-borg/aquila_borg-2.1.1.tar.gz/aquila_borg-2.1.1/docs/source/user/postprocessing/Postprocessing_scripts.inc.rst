Postprocessing scripts
======================

ARES Plotting library
---------------------

There is one repository that concentrate plotting routines and ready to
use program to postprocess ARES MCMC chains. It is located at
https://bitbucket.org/bayesian_lss_team/ares_visualization/. Please
enrich it at the same time as this page.

show_log_likelihood.py
~~~~~~~~~~~~~~~~~~~~~~

To be run in the directory containing the MCMC chain. Compute the power
spectrum of initial conditions, binned correctly, for each sample and
store it into a NPZ file. The output can be used by plot_power.py

plot_power.py
~~~~~~~~~~~~~

Contrast field in scatter plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python3

   import numpy as np

   dset_test=np.ones((32,32,32))

   def contrast2cic(dset):
      Nbox=dset.shape[0]
      cic=np.zeros((Nbox,Nbox,Nbox))
      min_dset=min(dset.flatten())

      for m in range(Nbox):
         for k in range(Nbox):
             for j in range(Nbox):
               d=dset[m,k,j]
                 cic[m][k][j]=int(np.floor((1+d)/(1+min_dset)))
      return cic

   cic=contrast2cic(dset_test)

Acceptance rate
~~~~~~~~~~~~~~~

.. code:: python3

   import matplotlib.pyplot as plt
   import h5py

   acceptance=[]
   accept=0

   for m in range(latest_mcmc()):
      f1=h5py.File('mcmc_'+str(m)+'.h5','r')
      accept=accept+np.array(f1['scalars/hades_accept_count'][0])
      acceptance.append(accept/(m+1))

   plt.plot(acceptance)
   plt.show()

Create gifs
~~~~~~~~~~~

.. code:: python3

   import imageio
   images = []
   filenames=[]

   for m in range(64,88):
      filenames.append('galaxy_catalogue_0x - slice '+str(m)+'.png')

   for filename in filenames:
      images.append(imageio.imread(filename))

   imageio.mimsave('datax.gif', images)

Scatter plot from galaxy counts in restart.h5
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python3

   import h5py
   import pyplot.matplotlib as plt

   f=h5py.File('restart.h5_0','r')
   data1=np.array(f['scalars/galaxy_data_0'])

   xgrid=[]
   ygrid=[]
   zgrid=[]

   for m in range(Nbox):
      for k in range(Nbox):
         for j in range(Nbox):
            if data1[m,k,j]!=0:
               xgrid.append(m)
               ygrid.append(k)
               zgrid.append(j)

   fig = plt.figure()
   ax = Axes3D(fig)
   ax.view_init(0, 80)
   ax.scatter(xgrid, ygrid, zgrid,s=1.5,alpha=0.2,c='black')
   plt.show()

Plot data on mask
~~~~~~~~~~~~~~~~~

.. code:: python3

   import numpy as np
   import healpy

   # Import your ra and dec from the data
   # Then projscatter wants a specific transform
   # wrt what BORG outputs

   ra=np.ones(10) 
   dec=np.ones(10)

   corr_dec=-(np.pi/2.0)*np.ones(len(ra))
   decmask=corr_dec+dec
   corr_ra=np.pi*np.ones(len(ra))
   ramask=ra+corr_ra

   map='WISExSCOSmask.fits.gz'
   mask = hp.read_map(map)
   hp.mollview(mask,title='WISE mock')
   hp.projscatter(decmask,ramask,s=0.2)

Non-plotting scripts
--------------------

Download files from remote server (with authentication):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python3

   from requests.auth import HTTPBasicAuth
   import requests

   def download_from_URL(o):
       URL='https://mysite.com/dir1/dir2/'+'filename_'+str(o)+'.h5'
       r = requests.get(URL, auth=HTTPBasicAuth('login', 'password'),allow_redirects=True)
       open('downloaded_file_'+str(o)+'.h5', 'wb').write(r.content)
       return None

   for o in range(10000):
       download_from_URL(o)

This works for horizon with the login and password provided in the
corresponding page.

Get latest mcmc_%d.h5 file from a BORG run
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python3

   import os

   def latest_mcmc():
      strings=[]
      for root, dirs, files in os.walk("."):
         for file in files:
            if file.startswith("mcmc_"):
               string=str(os.path.join(root, file))[7:]
               string=string.replace('.h5','')
               strings.append(int(string))
   return max(strings)

But beware: we want the file before the latest one to not destroy the writing process in the restart files.

Template generator
------------------

Jens Jasche has started a
specific repository that gather python algorithms to post-process the
BORG density field to create predictive maps for other effects on the
cosmic sky. The effects that has been implemented are the following:

-  CMB lensing
-  Integrated Sachs-Wolfe effect
-  Shapiro Time-delay

The repository is available on bitbucket `here <https://bitbucket.org/jjasche/lss_template_generator/>`__.
