Getting Started
===============

Welcome to the ALC AiiDAlab app's developer guide. 


Running The Test Suite 
----------------------

There is a testing framework in place which uses `pytest <https://docs.pytest.org/en/stable/>`_. To run the test suite locally, run:

.. code:: bash 

    cd tests 
    pytest 


Building The Documentation
--------------------------

The documentation for the ALC's AiiDAlab app is written using `sphinx <https://www.sphinx-doc.org/en/master/>`_ 
and is contained within the ``/docs/`` folder. It can be built via, 

.. code:: bash 

    cd docs 
    make html 

Alongside the user and developer documentation an API reference is provided via the sphinx-autodoc extension.
This can be automatically updated to include new modules using the command line tool provided with sphinx-autodoc, 

.. code:: bash 

    sphinx-apidoc -o ./docs/source/api_docs/ ./src/aiidalab_alc/

or any new modules can be added manually. All docstrings are to be written in `numpy style <https://numpydoc.readthedocs.io/en/latest/format.html>`_ for consistency. 


Coding Style 
------------


Contributing 
------------