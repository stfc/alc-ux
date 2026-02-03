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
    # Apptainer 
    apptainer run --compat --cleanenv --home /home/jovyan docker://aiidalab/full-stack:latest 

To enable an AiiDAlab application within the container it must be installed in the 
``/home/jovyan/apps/`` directory. This can be achieved by either installing using the 
in build terminal page or via binding a local instance of the development code into the 
container at initialisation, 

.. code:: bash 

    # Docker 
    docker run -it --rm -p 8888:8888 -v /path/to/myApp:/home/jovyan/apps/myApp aiidalab/full-stack:latest
    # Apptainer 
    apptainer run --compat --cleanenv --home /home/jovyan --bind /path/to/myApp:/home/jovyan/apps/myApp docker://aiidalab/full-stack:latest 

Python Limitations
------------------

A known current limitation of the provided AiiDAlab docker images is there python version 
is capped at 3.9 which can cause compatibility issues with more up-to-data python packages.
A custom docker image is provided in this repository which will mimic the ``aiidalab/full-stack`` 
image but using 3.10 as the base python version. This can be accessed at 
`<ghcr.io/stfc/alc-ux/base:latest>`_ and used as described above. 

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
