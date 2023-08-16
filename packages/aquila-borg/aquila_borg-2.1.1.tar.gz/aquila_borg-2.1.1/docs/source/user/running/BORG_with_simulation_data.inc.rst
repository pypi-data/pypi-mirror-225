Running BORG with simulation data
=================================

Pre-run test
------------

Gradient test
~~~~~~~~~~~~~

-  Run ``<ARES_REPO_DIR>/build.sh`` with ``~~debug``
-  Execute ``<BUILD_DIR>/libLSS/tests/test_gradient_<bias_model>``
-  Grab ``dump.h5``.
-  Plot analytical and numerical gradient (by finite difference), can
   use the script in ``<ARES_REPO_DIR>/scripts/check_gradients.py``
-  Example:

.. image:: /user/running/BORG_with_simulation_data_files/Gradient_test_for_2nd_order_bias.png


Setup and tuning
----------------

ARES configuration file and input files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ARES configuration file:

   -  Documentation: :ref:`here<configuration_file>`
   -  Set SIMULATION = True in ARES configuration file,
      ``<FILENAME>.ini``.
   -  Set corner0, corner1, corner2 = 0.
   -  See, for example, `ARES configuration file for BORG runs using
      SIMULATION
      data <https://datashare.mpcdf.mpg.de/s/wzOJo6XwGDN1bbD>`__

-  Halo catalog:

   -  ASCII format: 5 columns (ID, :math:`M_h`, :math:`R_h`, spin, x, y,
      z, :math:`v_x`, :math:`v_y`, :math:`v_z`). See, for example,
      `Python scripts to convert AHF output to ASCII catalog for
      BORG <https://datashare.mpcdf.mpg.de/s/p0AZJhQEsxFl9M6>`__.
   -  HDF5 format: similar to above. See, for example, `Python scripts
      to convert AHF output to HDF5 catalog for
      BORG <https://datashare.mpcdf.mpg.de/s/lEwZDKQGWOsSiYo>`__.

-  Trivial HEALPix mask where all pixels are set to 1 (choose approriate
   NSIDE for your BORG grid resolution).

-  Flat selection function in ASCII format. See, for example, `Flat
   selection function
   file <https://datashare.mpcdf.mpg.de/s/cdBlmHf0PPjuWXx>`__.

HMC performance tuning
~~~~~~~~~~~~~~~~~~~~~~

-  Grab ``<OUTPUT_DIR>/hmc_performance.txt``.
-  Plot :math:`\Delta H` and :math:`|\Delta H|`.
-  Tune ``max_epsilon`` and ``max_timestep`` in the ``.ini`` file
   accordingly.

-  An example of bad HMC performance. The horizontal dashed line denotes
   :math:`|\Delta H|=0.5`. Red dots denote negative :math:`\Delta H`:
   
.. image:: /user/running/BORG_with_simulation_data_files/Bad_HMC.png

-  An example of good HMC performance:

.. image:: /user/running/BORG_with_simulation_data_files/Good_HMC.png

After-run checks
----------------

Convergence check
~~~~~~~~~~~~~~~~~

-  Grab all ``<OUTPUT_DIR>/mcmc_<mcmc_identifier>.h5``.

-  Plot :math:`P_{mm, \mathrm{ini}}^s(k)` vs.
   :math:`P_{mm, \mathrm{ini}}^{\mathrm{theory}}(k)`.

   .. figure:: /user/running/BORG_with_simulation_data_files/Pk_convergence.png
      :alt: Pk convergence

      BORG_with_simulation_data_files/Pk_convergence.png

Correlation check
~~~~~~~~~~~~~~~~~

-  Compute noise residual in each BORG :math:`s`-th sample as
   :math:`\vec{\delta}_{\mathrm{res}}^s=\vec{\delta}_{m,\mathrm{ini}}^s-\left\langle\vec{\delta}_{m,\mathrm{ini}}\right\rangle_{s'}`.
-  Plot
   :math:`r_{\mathrm{residual}}(\Delta s=s'-s)\equiv\frac{\mathrm{Cov}\left(\vec{\delta}_{\mathrm{res}}^s,\,\vec{\delta}_{\mathrm{res}}^{s'}\right)}{\sigma_s \sigma_{s'}}`.

   .. figure:: /user/running/BORG_with_simulation_data_files/Residual_correlation_length.png
      :alt: Residual correlation length

      BORG_with_simulation_data_files/Residual_correlation_length.png
