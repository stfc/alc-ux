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

