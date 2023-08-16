.. _tutorial_ares_basic_outputs:

Tutorial: checking ARES outputs in python
=========================================

We first import numpy (to handle arrays), h5py (to read hdf5 files) and
matplotlib.pyplot (to plot density slices):

.. code:: ipython3

    import numpy as np
    import h5py as h5
    import matplotlib.pyplot as plt
    %matplotlib inline

We then load the hdf5 file with h5py:

.. code:: ipython3

    fdir="./" # directory to the ARES outputs
    isamp=0 # sample number
    fname_mcmc="mcmc_"+str(isamp)+".h5"
    hf=h5.File(fname_mcmc)

We can then list the datasets in the hdf5 file:

.. code:: ipython3

    list(hf.keys())




.. code:: text

    ['scalars']



.. code:: ipython3

    list(hf['scalars'].keys())




.. code:: text

    ['catalog_foreground_coefficient_0',
     'galaxy_bias_0',
     'galaxy_nmean_0',
     'powerspectrum',
     's_field',
     'spectrum_c_eval_counter']



The density contrast is stored as ‘scalars/s_field’:

.. code:: ipython3

    density=np.array(hf['scalars/s_field'])

We now plot a slice through the box:

.. code:: ipython3

    plt.imshow(density[16,:,:])

.. image:: /user/postprocessing/ARES_basic_outputs_files/ares_basic_outputs_12_1.png


The “restart” files contain a lot of useful information.

.. code:: ipython3

    fname_restart=fdir+"restart.h5_0"
    hf2=h5.File(fname_restart)
    list(hf2.keys())




.. code:: text

    ['galaxy_catalog_0', 'galaxy_kecorrection_0', 'random_generator', 'scalars']



.. code:: ipython3

    list(hf2['scalars'].keys())




.. code:: text

    ['ARES_version',
     'K_MAX',
     'K_MIN',
     'L0',
     'L1',
     'L2',
     'MCMC_STEP',
     'N0',
     'N1',
     'N2',
     'N2_HC',
     'N2real',
     'NCAT',
     'NFOREGROUNDS',
     'NUM_MODES',
     'adjust_mode_multiplier',
     'ares_heat',
     'bias_sampler_blocked',
     'catalog_foreground_coefficient_0',
     'catalog_foreground_maps_0',
     'corner0',
     'corner1',
     'corner2',
     'cosmology',
     'data_field',
     'fourierLocalSize',
     'fourierLocalSize1',
     'galaxy_bias_0',
     'galaxy_bias_ref_0',
     'galaxy_data_0',
     'galaxy_nmean_0',
     'galaxy_schechter_0',
     'galaxy_sel_window_0',
     'galaxy_selection_info_0',
     'galaxy_selection_type_0',
     'galaxy_synthetic_sel_window_0',
     'growth_factor',
     'k_keys',
     'k_modes',
     'k_nmodes',
     'key_counts',
     'localN0',
     'localN1',
     'messenger_field',
     'messenger_mask',
     'messenger_signal_blocked',
     'messenger_tau',
     'power_sampler_a_blocked',
     'power_sampler_b_blocked',
     'power_sampler_c_blocked',
     'powerspectrum',
     'projection_model',
     's_field',
     'sampler_b_accepted',
     'sampler_b_tried',
     'spectrum_c_eval_counter',
     'spectrum_c_init_sigma',
     'startN0',
     'startN1',
     'total_foreground_blocked',
     'x_field']



There we have in particular cosmological parameters:

.. code:: ipython3

    cosmo=np.array(hf2['scalars/cosmology'])
    print("h="+str(cosmo['h'][0])+", omega_m="+str(cosmo['omega_m'][0]))


.. code:: text

    h=0.6711, omega_m=0.3175


We also have the k modes to plot the power spectrum in our mcmc files:

.. code:: ipython3

    k_modes=np.array(hf2['scalars/k_modes'])

The power spectrum is stored in the mcmc files as
‘scalars/powerspectrum’:

.. code:: ipython3

    powerspectrum=np.array(hf['scalars/powerspectrum'])

We can now make a plot.

.. code:: ipython3

    plt.xlabel("$k$ [$h$/Mpc]")
    plt.ylabel("$P(k)$ [$(\mathrm{Mpc}/h)^3$]")
    plt.title("Power spectrum of the Oth sample")
    plt.loglog(k_modes,powerspectrum)

.. image:: /user/postprocessing/ARES_basic_outputs_files/ares_basic_outputs_23_1.png


Finally we close the hdf5 files.

.. code:: ipython3

    hf.close()
    hf2.close()
