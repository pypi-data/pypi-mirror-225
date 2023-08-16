Radial selection format
=======================

The file format for radial selection is the following:

-  First line is : ``rmin dr numPoints``

   -  ``rmin`` is the minimal distance of the completeness (the first point
      in the following)
   -  ``dr`` is the space between two samples
   -  ``numPoints`` is the number of points

-  Comment line start with ``#``
-  All following lines are completeness

For example, the following would create a completeness equal to one
between :math:`100 \, \mathrm{Mpc} \, h^{-1}` and :math:`4000 \, \mathrm{Mpc} \, h^{-1}`:

.. code:: text

    # some comment
    100 800 5
    1
    1
    1
    1
    1
