Developing With Docker Containers
=================================

Developing Within a Container
-----------------------------

AiiDAlab is setup to run efficiently within a containerised server hosting the core 
jupyter notebook and AiiDAlab plugins. AiiDAlab host several docker images which can 
be used for development of AiiDAlab applications. The most useful of which is the 
AiiDAlab/full-stack image which will start an instance of the base AiiDAlab home 
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
is capped at 3.9 which can cause compatability issues with more up-to-data python packages.
A custom docker image is provided in this repository which will mimic the aiidalab.full-stack 
image but using 3.10 as the base python version. This can be accessed at 
`<ghcr.io/stfc/alc-ux/base:latest>`_ and used as described above. 

Docker Images For Distribution
------------------------------

Whilst it is possible to use the base images by installing plugins at runtime, it is often useful 
to generate a custom docker image which contains all the required components and plugins for a 
given workflow out of the box. This can be achieved by bulding upon the base images described above. 
An example of this is the ``aiidalab/qe`` image which contains a pre-installed Quantum ESPRESSO plugin 
and all its dependencies. To create a custom image you will need to create a ``Dockerfile`` which uses 
the disired base image, then install all required dependencies and ensure that the AiiDAlab plugins are 
installed in the ``/home/jovyan/apps/`` directory so they are discoverable by the AiiDAlab runtime. 

.. code:: dockerfile 

    FROM aiidalab/full-stack:latest 

    USER root

    # Install some extra required dendencies to speed up start up
    RUN pip install aiidalab_widgets_base --no-cache-dir --no-user

    # Install any required aiida plugins
    RUN pip install aiida-chemshell aiida-mlip --no-cache-dir --no-user

    # This will install alc-ux AiiDAlab app on container start up into the correct directory
    COPY 61_prepare-aiidalab_alc.sh /usr/local/bin/before-notebook.d/

    USER ${NB_UID}
    WORKDIR ${HOME}

where the initialisation script ``61_prepare-aiidalab_alc.sh`` contains the following, 

.. code:: bash 

    #!/bin/bash

    echo "INSTALLING AiiDAlab ALC app"
    cd "${HOME}"/apps
    wget https://github.com/stfc/alc-ux/archive/refs/heads/main.zip
    unzip main.zip
    rm -f main.zip
    cd "${HOME}"/apps/alc-ux-main
    pip install -q .

    cd "${HOME}"