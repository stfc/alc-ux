.. _cloud_deployment_guide:

Deployment on ADA Cloud Workspace 
=================================

This guide details how to use AiiDAlab and the AiiDAlab ALC application on a cloud based 
remote workstation using the UKRI's `ADA <https://ada.stfc.ac.uk/>`_ service as an example. 
The information provided here can be easily generalised to any remote/cloud based workstation 
that utilises `Apptainer <https://apptainer.org/docs/user/main/index.html>`_ contained 
applications. 

Setup ADA Workspace
-------------------

Run AiiDAlab
------------

ADA uses Apptainer for container deployment which can in turn pull and run the docker 
image's provided with the AiiDAlab ALC app. Since these images were created to be used 
with docker a few key settings must be passed to ensure correct behaviour within the 
container. First are the ``--compat`` and ``--cleanenv`` parameters which prevent 
mounting of any local system filespaces or environment variables which could interfere 
with the container. This provides a more docker like approach to running containers, 
however, it is still required that the home directory be mounted to the container so 
that work will persist between instances of AiiDAlab. This is achieved by mounting the 
users home directory to the container's home directory which exists at ``/home/jovyan``
and then setting the home parameter to this directory. The full commands are shown below. 

To run a basic AiiDAlab instance running on python 3.10, with no installed additional 
applications besides the core AiiDAlab home interface run the following command from a 
terminal instance on the virtual workspace, 

.. code:: bash 

    apptainer run --compat --cleanenv --bind ${HOME}:/home/jovyan --home /home/jovyan docker://ghcr.io/stfc/alc-ux/base:py310

To run an AiiDAlab instance which contains the AiiDAlab ALC application and some additional
required python libraries, instead run, 

.. code:: bash 

    apptainer run --compat --cleanenv --bind ${HOME}:/home/jovyan --home /home/jovyan docker://ghcr.io/stfc/alc-ux/full:latest 

In addition to these supplied images, any of the official 
`AiiDAlab docker images <https://github.com/aiidalab/aiidalab-docker-stack>`_  can be 
used in the same manner, however, at present these are limited to python 3.9 which limits 
support with certain core AiiDA plugin's provided by the ALC. 

Data Persistence Within the Workspace
-------------------------------------

If these images have been run ensuring correct mounting of the user's home directory, 
then all data produced and managed by AiiDA/AiiDAlab will persist between instances 
of the AiiDAlab container. The first time the container is run, all required data 
directories for AiiDA will be produced in the user's home directory. This includes 
the ``.aiida`` directory containing the profile information for AiiDA and the 
``.postgresql`` directory which contains the database information. Whilst these 
exist the container will read any profile or database information from them 
instead of initialising new instances on start up. Additionally any files/folders 
generated from within the container or AiiDAlab application will persist as long 
as they exist within the mounted home space. 

Data Persistence Outside the Workspace 
--------------------------------------

It is recommended to use AiiDA's data base exporting tools to save the generated database with all 
results and provenance relations. This can then be imported into another instance of AiiDA to view 
or use any of the data nodes within the database. 