.. _developing_containers:

Developing With Docker Containers
=================================

Developing Within a Container
-----------------------------

AiiDAlab is setup to run efficiently within a containerised server hosting the core 
jupyter notebook and AiiDAlab plugins. AiiDAlab host several docker images which can 
be used for development of AiiDAlab applications. The most useful of which is the 
``aiidalab/full-stack`` image which will start an instance of the base AiiDAlab home 
page without installing any additional applications. To use this container you can 
run the following,

.. code:: bash 
    
    # Docker 
    docker run -it --rm -p 8888:8888 aiidalab/full-stack:latest 

The command line flags ``-it``, ``--rm`` and ``-p`` run the container interactively, delete it
when it is closed and expose the port ``8888`` to the host which is required for opening the
jupyter notebook in a browser. To run the equivalent setup with **Apptainer** instead of Docker
run the following,

.. code:: bash

    # Apptainer 
    apptainer run --compat --cleanenv --home /home/jovyan docker://aiidalab/full-stack:latest 


To enable an AiiDAlab application within the container it must be installed in the 
``/home/jovyan/apps/`` directory. This can be achieved by either installing using the 
in-built terminal page or via binding a local instance of the development code into the 
container at initialisation, 

.. code:: bash 

    # Docker 
    docker run -it --rm -p 8888:8888 -v /path/to/myApp:/home/jovyan/apps/myApp aiidalab/full-stack:latest
    # Apptainer 
    apptainer run --compat --cleanenv --home /home/jovyan --bind /path/to/myApp:/home/jovyan/apps/myApp docker://aiidalab/full-stack:latest 

If using the local bind method this allows editing of the application in a chosen local code editor
and all changes will be updated live within the container. For more complex apps this live editing 
may also require installing the project within the container as an editable python project by running
the following from a terminal within the container,

.. code:: bash

    cd /home/jovyan/apps/myApp
    pip install --no-user  -e . 

Once these two steps have been completed any local changes to the plugin will be dynamically updated within
the container and can be instantly visualised by refreshing the browser the notebook is running in. 

Python Limitations
~~~~~~~~~~~~~~~~~~

A known current limitation of the provided AiiDAlab docker images is there python version 
is capped at 3.9 which can cause compatibility issues with more up-to-data python packages.
A custom docker image is provided in this repository which will mimic the ``aiidalab/full-stack`` 
image but using 3.10 as the base python version. This can be accessed at 
`<ghcr.io/stfc/alc-ux/base:latest>`_ and used as described above.

Local AiiDA Instances
~~~~~~~~~~~~~~~~~~~~~

It is currently not possible to include local instances of an AiiDA profile or database within a container
running AiiDAlab, the container itself will need to create and manage all instances of AiiDA profiles and 
databases. These can be configured using environment variables passed to the container at startup, see 
:ref:`aiida_user_profile_setup` for more details. Once a profile and database has been setup by a AiiDAlab 
based container these can be re-used by different container instances including different images as long
as they are built of the same AiiDAlab foundation, they cannot be accessed by a local install of AiiDA 
however.


Docker Images For Distribution
------------------------------

Whilst it is possible to use the base images by installing plugins at runtime, it is often useful 
to generate a custom docker image which contains all the required components and plugins for a 
given workflow out of the box. This can be achieved by building upon the base images described above. 
An example of this is the ``aiidalab/qe`` image which contains a pre-installed Quantum ESPRESSO plugin 
and all its dependencies. To create a custom image you will need to create a ``Dockerfile`` which uses 
the desired base image, then install all required dependencies and ensure that the AiiDAlab plugins are 
installed in the ``/home/jovyan/apps/`` directory so they are discoverable by the AiiDAlab runtime. 

.. code:: dockerfile 

    # Use this for the latest official aiidalab image (Python 3.9)
    # FROM aiidalab/full-stack:latest 
    # Use this for a ported version of the above running on Python 3.10 
    FROM ghcr.io/stfc/alc-ux/base:py310  

    USER root
    
    # Install the alc-ux AiiDAlab plugin to the apps folder 
    RUN pip install git+https://github.com/stfc/alc-ux.git#egg=alc-ux --src ${HOME}/apps

    # Install alc aiida plugins (if not configured as dependencies of the AiiDAlab plugin app)
    RUN pip install aiida-chemshell aiida-mlip --no-cache-dir --no-user  

    USER ${NB_UID}
    WORKDIR ${HOME}
