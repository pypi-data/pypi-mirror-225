dm_sheet
========

This is a module for ARES/HADES/BORG.
It adds the algorithms **dm_sheet** to compute cosmological fields from
the dark matter phase-space sheet (in particular, density and velocity
fields from tetrahedra formalism).

``borg_forward`` supports the use of dm_sheet when it is available.

Setup
-----

To use this module, clone `the repository <https://bitbucket.org/bayesian_lss_team/dm_sheet/>`_ in $ARES_ROOT/extra/ (where $ARES_ROOT
represents the root source directory of ARES on your computer).

For example, you can do:

.. code:: bash

   cd $ARES_SOURCE/extra
   git clone git@bitbucket.org:/bayesian_lss_team/dm_sheet.git dm_sheet

and :ref:`rebuild <building>`.

Use
---

To use dm_sheet in ``borg_forward``, use the flag ``--dmsheet``. New
fields are then added to the :ref:`output files<outputs>`.

Contributors
------------

The main authors of this module are:

-  Florent Leclercq
-  Guilhem Lavaux

To add more features, please contact these people, or submit pull
requests.

Additional contributions from:

- James Prideaux-Ghee

References
----------

- T. Abel, O. Hahn, R. Kaehler (2012), Tracing the Dark Matter Sheet in Phase Space, arXiv:1111.3944
- O. Hahn, R. Angulo, T. Abel (2015), The Properties of Cosmic Velocity Fields, arXiv:1404.2280
- F. Leclercq, J. Jasche, G. Lavaux, B. Wandelt, W. Percival (2017), The phase-space structure of nearby dark matter as constrained by the SDSS, arXiv:1601.00093
