Getting Started
===============


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

This project adheres to the `pep8 <https://peps.python.org/pep-0008/>`_ style guide for python coding alongside numpy style docstring formatting. This should be checked before any code updates. A pre-commit configuration using the ruff linter tool is provided for convenience. 


Contributing 
------------

Contributing Workflow 
~~~~~~~~~~~~~~~~~~~~~

This document outlies the best practices for contributing to the ALC-ux project. These must be 
followed for any contributions to be accepted. In brief the contribution process should be as 
follows:

- Follow the branch, fix, merge model, from your own fork or fork/branch model. 
- Create an issue for all work (bug, feature etc.)
- Pull requests will not be accepted without review. 
- Any new feature must include appropriate testing. 

Using git for development 
~~~~~~~~~~~~~~~~~~~~~~~~~

The core *upstream* repository is hosted on GitHub which contributors will create forks, from 
using the GitHub web UI, to carry out any development work. This maintains a clean core repository.
Once a fork has been created the branch, fix, merge workflow should be followed.

**Step 1: Branch**


Create a new branch for the issue with an appropriate name (e.g. issueXYZ). This can either 
be carried out through the web UI, then cloned using, 

.. code:: bash 

    git clone -b issueXYZ --single-branch git@github.com:username/alc-ux.git 


Alternatively, use the CLI directly to create and checkout the new branch, 

.. code:: bash

    # clone the repository  
    git clone git@github.com:username/alc-ux.git 
    # create and checkout a new branch 
    git checkout -b issueXYZ 
    # create a remote tracking branch 
    git push -u origin issueXYZ 


**Step 2: Fix**


Here you will fix the issue commit all changes to the new remote tracking branch within 
your fork, ensuring all style guidelines are followed and changes are appropriately 
documented. 

**Step 3: Merge**


Via the web UI, create a pull request from your development branch into the upstream 
repository. Include any relevant labels or milestones and assign a reviewer. Once the 
request has been created, tests will be run and the review process will begin, which may 
include discussions using the comment system on the pull request. If changes need to be 
made you may make more commits onto your development branch which will be added to the 
pull request automatically. Once all is OK with the commit then the reviewer will set 
the request to be merged once all tests have passed. 

If your branch has become out of sync with the *upstream* repository then conflicts 
may arise. If they cannot be resolved automatically by git you will need to resolve them 
by hand as detailed in the GitHub documentation. 

It is best practice that when you submit the pull request you squash your commits into 
a single commit that will be applied to the *upstream* repository. This is enabled by 
default and should not be switched off. 

**Cleaning stale branches**


Deleting branches from the web interface will get rid of the remotes and
not of your local copies. The local branches left behind are called
stale branches. To get rid of them

.. code:: bash

    git remote prune origin


To delete a local branch

.. code:: bash

    git branch -d localBranch


if unmerged commits exists but you still want to delete use

.. code:: bash

    git branch -D localBranch
