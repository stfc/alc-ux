.. _startup_and_deployment:

Creating Startup Scripts For AiiDAlab
======================================

Startup Script
--------------

To ease user accessibility it is often useful to abstract the container initialisation 
behind a startup script that can be configured to use default parameters or ask the user 
for inputs at run time. This can then be used in the next stages to directly integrate 
into a desktop UI application. An example of a startup script is included within this 
`github repo <https://github.com/stfc/alc-ux/tree/main/scripts>`_ and will be the basis for this guide 
which details the key features required at startup. The example is given in both 
bash ``startup.sh`` and powershell ``startup.ps1`` for both linux and windows systems 
respectively. In general references in this document will be to the linux bash script.

Container Image
~~~~~~~~~~~~~~~

The core component of an AiiDAlab deployment is which container image to use at runtime which 
will determine what additional components and software is available to the user on top of the 
core AiiDAlab home application and AiiDA configuration. The section :ref:`_developing_containers`
covers how to create custom docker images for deploying additional components alongside the core 
AiiDAlab tools. When creating a startup script, this has to correctly point to whichever image 
you wish to expose to users for their workflows.  Whilst available components and applications 
can be installed once inside the container, having these pre-installed and configured greatly 
improves user experience. In the case of the example script contained within this repository 
a dynamic approach has been employed where the default AiiDAlab image ``aiidalab/full-stack:latest`` 
is used unless a command line argument ``docker_image`` is passed to the script which will 
enable the script to use a different image at the user's discretion. 

Container Engine
~~~~~~~~~~~~~~~~

It is important when developing a startup script that the target systems available container engine(s) is 
known so that the container run configuration can be appropriately tailored. The example script provided 
demonstrates an ability to provide a flexible approach which runs with either Apptainer or Docker as the 
requested container engine, setting all required command line arguments appropriately for each run call. 

AiiDA User Profile
~~~~~~~~~~~~~~~~~~

One of the requirements for utilising AiiDA as a workflow manager is an AiiDA user profile. 
Typically the AiiDAlab docker images simply create a default user profile however, this can 
be controlled via environment variables passed to the container at runtime. The environment 
variables used for profile creation are as follows:

- AIIDA_PROFILE_NAME
- AIIDA_USER_EMAIL
- AIIDA_USER_FIRST_NAME
- AIIDA_USER_LAST_NAME
- AIIDA_USER_INSTITUTION

The profile creation can also be switched off by setting the ``SETUP_DEFAULT_AIIDA_PROFILE`` 
variable to ``false``. Since this is directly linked to a specific user exposing these inputs 
is a valuable step to improve usability, particularly if a user is not familiar with importing 
environment variables into containers. The example startup script provided details a dynamic 
approach that will check if an existing AiiDA profile exists, and if it does not it will 
enable the profile creation step within the container startup and ask the user to input 
values for the variables listed above, which are then passed to the container run command.

An important concept to be aware of is the ability for a user to continually be able to stop and 
restart the container without having to create a new profile or database each time. If a user 
profile has been created then a file ``config.json`` will exist within the core ``.aiida`` 
directory, typically located in the user's home directory. This can be used as a simple runtime 
check to determine if profile creation is required.

Bind Paths
~~~~~~~~~~

Another key component of the container runtime is where the data is bound to in the users local machine, 
this enables data persistence beyond the scope of a single container instance and enables the retention of 
AiiDA profile and database information as detailed above. The most typical approach for this is to mount the
users home directory onto the containers home directory usually specified as ``/home/jovyan`` from the 
default AiiDAlab image configuration. This needs to be included in the container run command within any 
startup script otherwise data persistence will not be available to the user. Whilst the default bind location 
is appropriate for the majority of users there may be cases where the user will want to control this setting
which is demonstrated in the example startup script by use of a dedicated command line argument, which if not 
present defaults to the user's home directory. 


Linux Desktop Entries
---------------------

Within a linux based desktop environment it is possible to configure a bash script as defined above for 
the startup of AiiDAlab as a UI entry in the applications menu or on the desktop itself. This is achieved 
by writing a desktop entry file and placing it in the required applications folder for your Linux OS (e.g. 
``$HOME/.local/share/applications/``). An example desktop entry file would be as follows:

.. code::

    [Desktop Entry]
    Name=AiiDAlab
    Comment=AiiDAlab Application Startup
    Exec=/absolute/path/to/startup.sh
    Icon=/absolute/path/to/icon.ico
    Terminal=True # Required for user interaction in startup script
    Type=Application
    Categories=Utilities




ADA Deployment (Ansible)
------------------------

The ADA cloud platform uses `Ansible <https://docs.ansible.com/>`_ to manage software deployment on its 
virtual machines (workspaces). This allows tailored deployments for different user groups using a common 
setup process for available software. A software role has been created for AiiDAlab which will install 
an AiiDAlab startup script such as those described above onto the workspace's desktop environment making 
it available through the desktop UI. This script has been created such that the core docker image used 
can be changed depending on the required plugins and software configurations. To enable AiiDAlab for your
user group within ADA, contact the ADA developers at supportanalysis@stfc.ac.uk and request an AiiDAlab 
role be set up for your group and specify the backend docker image to be associated with it. 

For setup from scratch using Ansible as a framework an example playbook is given here which will pull the 
AiiDAlab docker image using Apptainer as the container engine and copy the startup script and desktop 
entries to the remote machine. 

.. code:: yaml

    - name: Install AiiDAlab container
      ansible.builtin.command: >
        apptainer pull --force --dir /opt/containers/
        aiidalab/full-stack:latest

    - name: Copy startup script 
      ansible.builtin.copy:
        src: aiidalab_startup.sh
        dest: /opt/aiidalab/

    - name: Copy menu shortcut for AiiDAlab 
      ansible.builtin.copy:
        src: aiidalab.desktop
        dest: /etc/xdg/applications/
        owner: root
        mode: "0444"

    - name: Copy icon for AiiDAlab
      ansible.builtin.copy:
        src: alc.svg
        dest: /usr/share/pximaps/aiidalab.ico 
        mode: "0644"