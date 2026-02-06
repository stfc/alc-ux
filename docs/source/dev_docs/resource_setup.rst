.. _pre_configured_resource_setup:

Resource Setup and Auto Configurations
======================================

Beyond AiiDA's reliance on developer maintained plugins to define how workflows are carried
out it also relies on a user specifying how and where the backend software programs will run.
At its simplest this is specifying where the programs executable lives on the local machine
however, AiiDA excels at being able to communicate with remote high performance compute (HPC)
resources to carry out longer or more computationally intensive jobs. This setup can be 
managed by the user and is described in the 
`AiiDA documentation <https://aiida.readthedocs.io/projects/aiida-core/en/stable/howto/run_codes.html>`_
and there is a pre-defined UI interface provided by AiiDAlab, discussed in :ref:`custom_resource_management`,
which provides a more user friendly method to define custom connections. However, when developing
AiiDAlab plugins it is the goal of the developer to make the user's experience as simple and
streamline as possible and therefore, there are methods in place which enable the pre-definition
of these computer/code configurations which can be loaded directly into the UI. The AiiDAlab home
application has an example of this for some pre-configured compute resources however, these 
facilities are not available to UKRI based (or associated) researchers. Within this repository 
exists a resource database file `remote.json <https://github.com/stfc/alc-ux/blob/main/resources/remotes.json>`_
which contains pre-defined configurations for UKRI managed HPC resources. This file can be loaded
into the AiiDAlab resource setup widget as shown in 
`AiiDAlab ChemShell <https://github.com/stfc/aiidalab-chemshell/blob/main/notebooks/resources.ipynb>`_
presenting a much more user friendly method to quickly configure code instances on these pre-defined
compute resources. A description of the different entries within the *.json* file are given below.

Resource Database Structure
---------------------------

This file is a json style database defining common STFC/UKRI provided compute resources. The top most
entry is a remote host (HPC facility or other remote compute resource) under which are specific
compute specifications for the given machine. This is often just a single entry however, if the
remote machine requires different configurations for, for example, CPU and GPU specifications,
these can be separated here. Following this are 3 separate components which tell AiiDA how to
setup a code instance on this remote machine. These components are the *computer-configuration*,
*computer-setup* and *codes* sections. These closely mirror the yaml style definition files
which can be used by the AiiDA command line directly.

Within any of the sections it is possible to expose variables which the user can input to tailor
the configuration, such as the user's username on the remote machine. These are defined in the 
*metadata.template_variables* section within each of the defined subsections. Each 
*template_variables* definition provides the following fields:

- default -> The default value for the variable
- description -> A detailed description for the variable
- type -> A type defining how AiiDAlab will create the input widget i.e. text for a textbox input or list for a dropdown selector
- key_display -> The text to be displayed next to the input widget in the UI
- options -> An optional field specifying pre-defined options for the variable used when the type is set to list

The variables can then be used throughout the section via the ``{{ variable_name }}`` syntax.

computer-configure
~~~~~~~~~~~~~~~~~~

This is the most minimalist section and will often remain unchanged between compute resources
except for particularly specialised setups. Its primary purpose is to provide the users's
username on the remote machine and what connection policy to use.

computer-setup
~~~~~~~~~~~~~~

This is the most important section as it defines how AiiDA will communicate with the remote host
including how jobs will be submitted and how resources will be managed. The key fields are:

- label -> A human readable label to give the computer.
- hostname -> The hostname of the remote machine.
- transport -> An AiiDA specification for the method of connection i.e. ``core.ssh`` for ssh connections.
- scheduler -> An AiiDA specification for the job submission manager i.e. ``core.slurm`` for slurm managed machines.
- work_dir -> The location on the remote machine to store all job files.
- shebang -> The line dictating the interpreter to use for the submission script.
- mpirun_command -> Defines how to run MPI parallel jobs.
- mpiprocs_per_machine -> The total number of processors per CPU node.
- prepend_text -> Additional text to be added to the submission script before the job's run command.
- append_text -> Additional text to be added tot he submission script after the job's run command.

codes
~~~~~

This section provides configurations for available codes on the remote host with each entry defining
a separate code instance with the following fields:

- label -> A human readable label to give the code instance.
- description -> A more detailed description of the code instance.
- filepath_executable -> The executable for the given software.
- default_calc_job_plugin -> The default AiiDA calculation plugin to use for the job.
- with_mpi -> A boolean value defining whether the code supports MPI parallelism.
- prepend_text -> Additional text to be added to the submission script before the job's run command.
- append_text -> Additional text to be added tot he submission script after the job's run command.