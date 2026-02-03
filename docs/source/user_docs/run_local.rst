.. _loca_aiidalab:

Running AiiDAlab
================

Start-up Script 
---------------

For convenience a start-up script is provided within this repository, which will handle the container start up, 
AiiDA user profile generation and ssh agent forwarding using either apptainer or docker. This can be found `here <https://github.com/stfc/alc-ux/tree/main/scripts>`_
along with guidance on how it can be customised at runtime. Note that by default the script will mount the users 
entire home space into the container, this will bring any existing AiiDA profiles/databases into the container however, 
it will also create two new directories (if they don't already exist) called ``apps`` and ``work`` within the users 
home directory. 

If you wish to manually configure the AiiDAlab start-up then follow the remaining guides on this page.

Running The Container
---------------------

AiiDAlab is setup to run efficiently within a containerised server hosting the core 
jupyter notebook and AiiDAlab plugins. AiiDAlab host a base docker image which 
will provide a minimal AiiDAlab home page and ability to install additional 
applications. This image can be used to run AiiDAlab locally on your machine 
using either `Docker <https://www.docker.com/get-started>`_ or other compatible container engines such as 
`Apptainer <https://apptainer.org/docs/user/main/index.html>`_. 
To use the base container, run the following,

.. code:: bash 

    docker run -it --rm -p 8888:8888 aiidalab/full-stack:latest  

For convenience, many applications create their own images based on those provided by 
AiiDAlab which contain the additional requirements for their applications. 
One such image is provided in this repository which contains the AiiDAlab 
ALC application and its dependencies. This image is hosted at 
`<ghcr.io/stfc/alc-ux/full:latest>`_ and can be run locally in the same manner. 

AiiDA User Profile Setup
------------------------

By default the AiiDA instance within the container defines a default user however, it is possible 
to configure this user at start up, which is important since all data generated will be tagged with 
this user configuration. To do this certain environment variables need to be passed to the container 
at start-up, 

- ``AIIDA_PROFILE_NAME``: The name of the new user profile 
- ``AIIDA_USER_EMAIL``: Email address associated with the user 
- ``AIIDA_USER_FIRST_NAME``: User's fisrt name 
- ``AIIDA_USER_LAST_NAME``: User's second name 
- ``AIIDA_USER_INSTITUTION``: Institution associated with the user 

These can be passed to the container by using the ``--env`` command line option, or they can all be written to 
a file and read in by the ``--env-file`` option.

There are certain circumstances where a new profile is not required, either if you want to manually setup 
one from within the container or if you are binding in an existing AiiDA configuration folder containing an 
existing user profile. In this instance you would pass in the ``--env SETUP_DEFAULT_AIIDA_PROFILE=false`` 
variable, which will disable the creation of a new profile on startup. 

Data Persistence 
----------------

When running AiiDAlab through a container, it is important to ensure that the 
folders within the container which will store the user data produced by AiiDAlab 
are mounted to local directories so they are not lost when the container is stopped. The containers provided create a ``work`` directory within the 
home space of the container (``/home/jovyan/work``) which can be used as the mounting 
point within the contianer. To run the container with the correct bind mount run the following, 

.. code:: bash 

    docker run -it --rm -p 8888:8888 -v /path/to/local/folder:/home/jovyan/work aiidalab/full-stack:latest 

Another option, is to mount the entire home directory of the container to a local folder. 
This will ensure that the AiiDA database and profile information persist between container 
instances, not just the files produced under the work directory

.. code:: bash 

    docker run -it --rm -p 8888:8888 -v /path/to/local/folder:/home/jovyan aiidalab/full-stack:latest 


SSH Connections
---------------

To fully leverage AiiDA's capabilities it is often necessary to connect to a remote hight performance compute
(HPC) facility to submit jobs. This is typically achieved via SSH connections. Therefore, when running AiiDAlab within
a container it is important to ensure that the SSH configuration and keys are available within the container. 
This can be achieved by SSH agent forwarding. First ensure that your local SSH agent is running and has the required 
keys added, 

.. code:: bash 

    eval "$(ssh-agent -s)"
    ssh-add /path/to/private/key 

Then run the docker container with the following additional arguments, 

.. code:: bash 
    
        docker run -it --rm -p 8888:8888 \
            -v /path/to/local/folder:/home/jovyan/work \
            -v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK=$SSH_AUTH_SOCK \
            aiidalab/full-stack:latest 

This will mount the SSH agent socket into the container and set the appropriate environment variable so that SSH 
connections from within the container will use the local SSH key. This is a very important step since AiiDA 
relies on SSH key authentication to connect to remote HPC resources. 

