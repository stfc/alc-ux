FROM ghcr.io/stfc/alc-ux/base:py310 

USER root
 
# Install some extra required dendencies to speed up start up 
RUN pip install aiidalab_widgets_base --no-cache-dir --no-user

# Install alc aiida plugins 
RUN pip install aiida-chemshell aiida-mlip --no-cache-dir --no-user  

# This will install alc-ux on container start up 
COPY 61_prepare-aiidalab_alc.sh /usr/local/bin/before-notebook.d/

USER ${NB_UID}
WORKDIR ${HOME}

