.. _user_guide_introduction:

Getting Started
---------------

AiiDA
~~~~~

`AiiDA <https://www.aiida.net/>`_  is a workflow management framework facilitating automation, sharing and reproduction of complex worflows across 
all areas of modern scientific computing. It is built around the `ADES model <https://arxiv.org/abs/1504.01163>`_\: 
Automation, Data, Environment and Sharing. It enables computational processing via a plugin interface either locally, 
or via connection to a high performance compute (HPC) facility and then provides data management strategies including 
full data provenance to improve reproducability. A more detailed guide on the core concepts of AiiDA can be found 
`here <https://aiida.readthedocs.io/projects/aiida-core/en/stable/intro/index.html>`_\. 

AiiDAlab 
~~~~~~~~

`AiiDAlab <https://www.aiidalab.net/>`_ is a flexible UI interface for the AiiDA
computational workflow managment system. It provides a logical step by step approach to setting up and running 
research software packages leveraging AiiDA's workflow provenance and data management capabilities.
It is implemented as an interactive jupyter notebook environment leveraging the graphical capabilities of 
IPython widgets. AiiDAlab is designed to be modular and extensible via a plugin system allowing users to 
install and develop custom applications to carry out specific workflows relating to their research.  

ALC AiiDAlab App
~~~~~~~~~~~~~~~~

The ALC AiiDAlab app is an example framework for developing AiiDAlab applications for ALC supported software 
packages. It provides an example application structure, based around submitting ChemShell workdlows via AiiDA.
This application can be used as a starting point for developing new AiiDAlab applications for other software 
projects. 