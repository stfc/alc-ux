# ALC-UX Scripts

This directory contains helper scripts for interacting with AiiDAlab specifically geared to running 
on ALC resources such as the ADA cloud platform. A description of each script is given below. 


## startup.sh 

This is a bash script that will handle the conatiner startup for running AiiDAlab. Additionally it will
handle the creation of a new AiiDA user profile (if an existing one is not found) and the forwarding 
of the host's SSH agent into the container. This provides a much more user friendly and flexible start-up 
method. It provides the following input options:

- ``--docker-image``: The docker image the conatainter will build from. The default is *aiidalab/full-stack:latest* 
- ``--home-bind``: The directory to which the container's home directory will be bound to. 
    To ensure correct restart behaviour this should always be the same value between instances of the 
    container. The default is the user's home directory (${HOME}).
- ``--use-docker``: This key will tell the script to use the docker container engine instead of the 
    default apptainer container engine. 