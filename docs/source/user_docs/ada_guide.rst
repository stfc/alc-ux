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

The following section is specific to the ADA cloud computing platform. 

To be able to use ADA it is required to setup an 
`STFC facilities user account <https://users.facilities.rl.ac.uk/auth//?service=https://ada.stfc.ac.uk/&redirecturl=https://ada.stfc.ac.uk/auth/DEV>`_ 
using your UKRI credentials. Once created you will be able to access `ADA <https://ada.stfc.ac.uk/>`_
and create and manage workspaces. It will also provide access to online tools to enable data transfer 
to and from ADA workspaces via a user home directory, which will be mounted into any workspace you 
create. There are also tools for mounting external data shares into your running workspaces. 
It is currently recommended to use create a developer workspace 
as the functionality for AiiDAlab on ADA is still a work in progress. Once created you can use the 
start script provided or manually configure and run AiiDAlab within the workspace as described below.

Any questions regarding the creation of an ADA user account or workspace management can be directed to 
the ADA support team at supportanalysis@stfc.ac.uk. 


Run AiiDAlab
------------

Startup Script 
~~~~~~~~~~~~~~

A `startup <https://github.com/stfc/alc-ux/tree/main/scripts>`_ script is provided which will handle 
initialising the container and the user workspace within the container. Once this has run a web address 
will be provided which can be opened within a browser and will display the AiiDAlab application home page. 
This script comes pre-installed on many instances of ADA workspaces, if it is not present in your groups
default workspace configuration and you would like it to be please get in touch with the ADA support 
team at supportanalysis@stfc.ac.uk. They will need to know for which group you would like to configure 
AiiDAlab for and what AiiDAlab based docker image provides all the required plugins and software for 
your workflows otherwise the default aiidalab/ful-stack will be used and users will have to configure the
required plugins and software themselves. 

If you wish to configure a manual setup and run AiiDAlab on ADA, continue with the guide below.

Manual Initialisation
~~~~~~~~~~~~~~~~~~~~~

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

It is recommended to use AiiDA's database exporting tools to save the generated database with all 
results and provenance relations. This can then be imported into another instance of AiiDA to view 
or use any of the data nodes within the database. 