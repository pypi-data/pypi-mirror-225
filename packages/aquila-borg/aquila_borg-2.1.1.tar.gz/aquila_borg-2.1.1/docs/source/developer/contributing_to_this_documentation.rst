Contributing to this documentation
==================================

The present documentation for *ARES*-*HADES*-*BORG* is a joint endeavour from many members of the `Aquila Consortium <https://aquila-consortium.org/>`_.

The purpose of this page is to describe some technical aspects that are specific to our documentation. Useful general links are provided in the :ref:`last section <useful_resources_documentation>`.


Source files, Sphinx, and Read the Docs
---------------------------------------

Source files and online edition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Source files of the present documentation are located in the `public ARES repository on Bitbucket <https://bitbucket.org/bayesian_lss_team/ares/>`_, in a subdirectory called ``docs/``. Their extension is ``.rst``.

The easiest way to contribute to the documentation is to directly edit source files online with Bitbucket, by navigating to them in the git repository and using the button `edit` in the top right-hand corner. Alternatively, clicking on the link `Edit on Bitbucket` on Read the Docs will take to the same page. Editing online with Bitbucket will automatically create a pull request to the branch that is shown in the top left-hand corner of the editor.

Sphinx and Read the Docs
~~~~~~~~~~~~~~~~~~~~~~~~

The present documentation is based on **Sphinx**, a powerful documentation generator using python. The source format is **reStructuredText** (RST). It is hosted by **Read the Docs** (https://readthedocs.org), which provides some convenient features:

- the documentation is built every time a commit is pushed to the |a| repository,
- documentation for several versions is maintained (the current version is visible in green at the bottom of left bar in Read the Docs pages),
- automatic code generation can be generated (in the future).


Off-line edition and creation of a pull request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To build the documentation locally, go to ``docs/`` and type

.. code:: bash

    make html
    
You will need a python environment with Sphinx; see for example `this page on how to get started with Sphinx <https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html>`_. Output HTML pages are generated in ``docs/_build/html``.

You can edit or add any file in ``docs/source/`` locally. Once you have finished preparing your edits of the documentation, please make sure to solve any Sphinx warning. 

You can then commit your changes to a new branch (named for instance ``yourname/doc``) and create a pull request as usual (see :ref:`development_with_git`). Please make sure to create a pull request to the correct branch, corresponding to the version of the code that you are documenting.

Once your pull request is merged, the documentation will be automatically built on Read the Docs.


Contributing new pages
----------------------

reStructuredText files
~~~~~~~~~~~~~~~~~~~~~~

The easiest way to contribute a new page is to directly write a reStructuredText document and place it somewhere in ``docs/source``. Give it a ``.rst`` extension and add it somewhere in the table of contents in ``docs/source/index.rst`` or in sub-files such as  ``docs/source/user/extras.rst``.

To include figures, add the image (jpg, png, etc.) in a subdirectory of ``docs/source``. As all images are ultimately included in the |a| repository, please be carefull with image sizes.

reStructuredText syntax
^^^^^^^^^^^^^^^^^^^^^^^

A RestructuredText primer is available `here <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_.

The order of headings used throughout the |a| documentation is the following:
    
.. code:: text

    ######### part
    ********* chapter
    ========= sections
    --------- subsections
    ~~~~~~~~~ subsubsections
    ^^^^^^^^^
    '''''''''

Included reStructuredText files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Extension**. If you write a page that is included in another page (using the RST directive ``.. include::``), make sure that its extension is ``.inc.rst``, not simply ``.rst`` (otherwise Sphinx will generate an undesired HTML page and may throw warnings).
- **Figures**. If there are figures in your "included" pages, use the "absolute" path (in the Sphinx sense, i.e. relative to ``docs/source/``) instead of the relative path, otherwise Sphinx will throw warnings and may not properly display your figures on Read the Docs (even if they are properly displayed on your local machine). For instance, in ``docs/source/user/postprocessing/ARES_basic_outputs.inc.rst``, one shall use

.. code:: rst

    .. image:: /user/postprocessing/ARES_basic_outputs_files/ares_basic_outputs_12_1.png

instead of

.. code:: rst

    .. image:: ARES_basic_outputs_files/ares_basic_outputs_12_1.png

Markdown pages
~~~~~~~~~~~~~~

If you have a page in Markdown format (for example, created in the **Aquila CodiMD**) that you wish to include in the documentation, you shall convert it to reStructuredText format. There exists automatic tools to do so, for instance `CloudConvert <https://cloudconvert.com/md-to-rst>`_ (online) or `M2R <https://github.com/miyakogi/m2r>`_ (on Github). It is always preferable to check the reStructuredText output. 

Jupyter notebooks
~~~~~~~~~~~~~~~~~

- **Conversion to RST**. If you have Jupyter/IPython notebooks that you wish to include in the documentation, Jupyter offers a `command <https://nbconvert.readthedocs.io>`_ to convert to reStructuredText:

    .. code:: bash

        jupyter nbconvert --to RST your_notebook.ipynb

    The output will be named ``your_notebook.rst`` and any image will be placed in ``your_notebook_files/*.png``. These files can be directly included in ``docs/source/`` after minimal editing.

- **nbsphinx**. Alternatively, you can use the nbsphinx extension for Sphinx (https://nbsphinx.readthedocs.io/) which allows you to directly add the names of ``*.ipynb`` files to the `toctree`, but offers less flexibility.



.. _useful_resources_documentation:

Useful resources
----------------

- `Read the Docs documentation <https://docs.readthedocs.io/en/stable/index.html>`__
- `Installing Sphinx <https://www.sphinx-doc.org/en/master/usage/installation.html>`__
- `Getting Started with Sphinx <https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html>`__
- `reStructuredText Primer <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`__
- Markdown conversion: `CloudConvert <https://cloudconvert.com/md-to-rst>`__, `M2R <https://github.com/miyakogi/m2r>`__
- `Jupyter nbconvert <https://nbconvert.readthedocs.io>`_, `nbsphinx <https://nbsphinx.readthedocs.io/>`__
