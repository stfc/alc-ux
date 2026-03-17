.. _local_aiidalab:

Running AiiDAlab
================

Since AiiDAlab is a jupytper notebook environment it is recommended to run AiiDAlab through a container engine 
such as Docker or Apptainer. Many different docker images exist for different configurations of AiiDAlab 
with various software pre-configured within the container's environment or a simple base container can be 
used for you to configure as you utilise AiiDAlab. 

AiiDAlab Launch
---------------

AiiDAlab provides a python based utility for managing and running these containerised environments called 
`AiiDAlab Launch <https://aiidalab.readthedocs.io/en/latest/usage/access/launch.html>` which provides a 
simplified command line interface to run AiiDAlab without the user needing to understand and configure 
docker containers directly. It uses docker as the backend container engine and can be installed via ``pip``
(or ``pipx`` if you do not have a locally configured python installation), 

.. code:: bash 

    pip install aiidalab-launch

It facilitates multiple AiiDA profiles with various home directories and ports for more complex AiiDAlab 
configurations. To create a new profile and start the AiiDAlab interaface run, 

.. code:: bash

    aiidalab-launch profile add --image aiidalab/full-stack:latest aiidalab
    aiidalab-launch start -p aiidalab

This will produce the required URL to open the AiiDAlab interface within a browser. To see more information 
on how to configure the profile further run, 

.. code:: bash 

    aiidalab-launch profile --help


This is the recommended way to run AiiDAlab locally particularly for users who are not familiar with 
managing docker containers directly. Most of the remaining sections on this page deal with manually
configuring AiiDAlab startup directly via the container engine however, sections such as 
:ref:`data_persistence_within_the_container` and :ref:`software_within_the_container` are still 
relevant when running via AiiDAlab launch. 


Start-up Script 
---------------

For convenience a start-up script is provided within this repository, which will handle the container start up, 
AiiDA user profile generation and ssh agent forwarding using either apptainer or docker. This is an alternative 
but less featured option than AiiDAlab-launch but demonstrates how the deployment of AiiDAlab can be configured 
for container engines other than Docker. It is also how AiiDAlab has been deployed to cloud platforms such as 
ADA, see :ref:`cloud_deployment_guide`\. This example script can be found `here <https://github.com/stfc/alc-ux/tree/main/scripts>`_
along with guidance on how it can be customised at runtime. Note that by default the script will mount the users 
entire home space into the container, this will bring any existing AiiDA profiles/databases into the container however, 
it will also create two new directories (if they don't already exist) called ``apps`` and ``work`` within the users 
home directory. 


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

These can be passed to the container by using the ``--env`` command line option,

.. code:: bash 

    docker run -it --rm -p 8888:8888 --env AIIDA_PROFILE_NAME=username aiidalab/full-stack:latest 


or they can all be written to a file and read in by the ``--env-file`` option. See the 
`docker documentation <https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/>`_ 
for more details on how to pass environment variables into a container. 

There are certain circumstances where a new profile is not required, either if you want to manually setup 
one from within the container or if you are binding in an existing AiiDA configuration folder containing an 
existing user profile. In this instance you would pass in the ``--env SETUP_DEFAULT_AIIDA_PROFILE=false`` 
variable, which will disable the creation of a new profile on startup. 

.. _data_persistence_within_the_container:

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


.. _software_within_the_container:

Making Software Available Within AiiDAlab
-----------------------------------------

Since AiiDAlab runs within a container, much like with the data persistence configuration, it is 
up to users to enable local software within the container. By default Docker cannot see anything 
on the local machine unless it is specifically forwarded into the container. There are three main 
ways for accessing software to run on the local machine:

- Run the container via an image which comes pre-configured with the required software stack.
- Install the software directly into the container's local home environment.
- Mount existing software into the container via bind mounts.

The simplest option is to choose a base docker image which has the required local software pre-configure,
many of these exist for software such as `Quantum ESPRESSO <https://hub.docker.com/r/aiidalab/qe>`_\ 
or `ChemShell <https://github.com/stfc/aiidalab-chemshell/pkgs/container/aiidalab-chemshell%2Ffull>`_\. 


Installing software directly within the container is the second most recommended option for enabling 
local software stacks within AiiDAlab. This can be achieved either through the AiiDAlab plugin manager
which can be accessed via the UI, or through the command line to manually install software which 
can also be accessed through the main AiiDAlab UI. Many plugins (particularly python focused software)
bundles the required executables with their respective AiiDAlab plugin which can be installed via the
plugin manager, Quantum ESPRESSO being one of these examples. These plugins will install all required 
components for both their AiiDAlab UI plugin, AiiDA plugin and core software stack whilst also 
pre-configuring a local AiiDA code instance for the given app which can then be accessed through the
AiiDAlab UI to run the software. If choosing to manually install software you must also manually configure
the AiiDA code instance and restart the AiiDA daemon to enable access to the installed software through
the AiiDAlab UI. Examples of how to do this can be found here: :ref:`custom_resource_management`\. 
Of particular note is that most AiiDAlab containers use `mamba <https://mamba.readthedocs.io/en/latest/user_guide/mamba.html>`_
to manage python packages within the container and therefore, the user can use both ``mamba`` and ``pip``
to install software where applicable.

The final and potentially most complex option is to mount existing software into the container. This is
not recommended for those that aren't highly familiar with running hybrid containerised applications as it can
cause dependency and security issues if not handled correctly. 


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

