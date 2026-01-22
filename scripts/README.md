# ALC-UX Scripts

This directory contains helper scripts for interacting with AiiDAlab specifically geared to running 
on ALC resources such as the ADA cloud platform. A description of each script is given below. 


## startup.sh 

This is a bash script that will handle the conatiner startup for running AiiDAlab. Additionally it will
handle the creation of a new AiiDA user profile (if an existing one is not found) and the forwarding 
of the host's SSH agent into the container. This provides a much more user friendly and flexible start-up 
method. It provides the following input options:

- ``--docker-image``: The docker image the conatainter will build from. The default is *aiidalab/full-stack:latest* 
- ``--home-bind``: The **absolute** path to the directory to which the container's home directory will be bound to. 
    To ensure correct restart behaviour this should always be the same value between instances of the 
    container. The default is the user's home directory (${HOME}).
- ``--use-docker``: This key will tell the script to use the Docker container engine instead of the 
    default Apptainer container engine. 

## startup.ps1

This is a powershell equivalent of ``startup.sh`` for use on Windows. Provides almost all functionality of 
the bash equivalent but is limited to only using Docker.


## aiidalab.desktop 

This is an example desktop configuration file which launches the startup script and in turn the configured 
AiiDAlab application hosted in an Apptainer container. It can be accessed from the file explorer and when 
opened runs the script as defined in the ``Exec`` field. For convenience it is recommended that a user edit
this file to give the absolute path to the ``startup.sh`` script and ``alc.svg`` image in the ``Exec`` and 
``Icon`` fields (instead of a relative path) and then place the file in the ``/home/${USER}/Desktop`` folder
where it will now show on the user's desktop and can be executed from there. 