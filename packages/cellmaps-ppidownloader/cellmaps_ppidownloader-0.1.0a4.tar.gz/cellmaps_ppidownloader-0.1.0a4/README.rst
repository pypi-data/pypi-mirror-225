================================
Cell Maps for AI PPI Downloader
================================


.. image:: https://img.shields.io/pypi/v/cellmaps_ppidownloader.svg
        :target: https://pypi.python.org/pypi/cellmaps_ppidownloader

.. image:: https://app.travis-ci.com/idekerlab/cellmaps_ppidownloader.svg?branch=main
    :target: https://app.travis-ci.com/idekerlab/cellmaps_ppidownloader

.. image:: https://readthedocs.org/projects/cellmaps-ppidownloader/badge/?version=latest
        :target: https://cellmaps-ppidownloader.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

Downloads Affinity-Purification mass spectrometry (AP-MS) data as a Protein-Protein Interaction
network used in the pipeline for `Cell Maps for AI (CM4AI) <https://cm4ai.org>`__


* Free software: MIT license
* Documentation: https://cellmaps-ppidownloader.readthedocs.io.

Dependencies
------------

* TODO add

Compatibility
-------------

* Python 3.8+

Installation
------------

.. code-block::

   git clone https://github.com/idekerlab/cellmaps_ppidownloader
   cd cellmaps_ppidownloader
   make dist
   pip install dist/cellmaps_ppidownloader*whl


Run **make** command with no arguments to see other build/deploy options including creation of Docker image 

.. code-block::

   make

Output:

.. code-block::

   clean                remove all build, test, coverage and Python artifacts
   clean-build          remove build artifacts
   clean-pyc            remove Python file artifacts
   clean-test           remove test and coverage artifacts
   lint                 check style with flake8
   test                 run tests quickly with the default Python
   test-all             run tests on every Python version with tox
   coverage             check code coverage quickly with the default Python
   docs                 generate Sphinx HTML documentation, including API docs
   servedocs            compile the docs watching for changes
   testrelease          package and upload a TEST release
   release              package and upload a release
   dist                 builds source and wheel package
   install              install the package to the active Python's site-packages
   dockerbuild          build docker image and store in local repository
   dockerpush           push image to dockerhub




Needed files
------------

**TODO:** Add description of needed files


Usage
-----

For information invoke :code:`cellmaps_ppidownloadercmd.py -h`

**Example usage**

**TODO:** Add information about example usage

.. code-block::

   cellmaps_ppidownloadercmd.py # TODO Add other needed arguments here


Via Docker
~~~~~~~~~~~~~~~~~~~~~~

**Example usage**

**TODO:** Add information about example usage


.. code-block::

   docker run -v `pwd`:`pwd` -w `pwd` idekerlab/cellmaps_ppidownloader:0.1.0 cellmaps_ppidownloadercmd.py # TODO Add other needed arguments here


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _NDEx: http://www.ndexbio.org
