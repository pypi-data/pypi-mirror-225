How to create a config file from python
=======================================

This page is about running the ``gen_subcat_conf.py`` script under
``scripts/ini_generator`` in ares. For an explanation of the config-file itself, see :ref:`here<configuration_file>`.

Config-file for 2M++ and SDSS(MGS)
----------------------------------

The folder containing the scripts and the ini files below is located in ``$SOURCE/scripts/ini_generator``. Steps to generate the config-file are the following:

-  Manipulate ``header.ini`` for your needs
-  (If needed) alter template files (``template_sdss_main.py``,
   ``template_2mpp_main.py`` and ``template_2mpp_second.py``) for the cutting and adjusting of data
-  To create ini file, run this command:

.. code:: bash

    python gen_subcat_conf.py  --output NAME_OF_OUTPUT_FILE.ini --configs template_sdss_main.py:template_2mpp_main.py:template_2mpp_second.py  --header header.ini
