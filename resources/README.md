# Resource Files

This directory contains several useful resource files for ALC/STFC common components which can be
used accross AiiDA and AiiDAlab applications.

## remotes.json

This file is a json style database defining common STFC provided compute resources. The top most
entry is a remote host (HPC facilitiy or other remote compute resource) under which are specific
compute specifications for the given machine. This is often just a single entry however, if the
remote machine requires different configurations for, for evample, CPU and GPU specifications,
these can be separated here. Following this are 3 separate components which tell AiiDA how to
setup a code instance on this remote machine. These components are the *computer-configuration*,
*computer-setup* and *codes* sections. These closely mirror the yaml style definition files
which can be used by the AiiDA command line directly each of which is described in more detail
in the full alc-ux [documentation](https://stfc.github.io/alc-ux/).
