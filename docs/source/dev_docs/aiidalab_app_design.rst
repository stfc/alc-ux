General Plugin Design 
=====================

AiiDAlab plugins are designed as jupyter notebook UIs with a core package providing the 
UI components. Each plugin is required to have a ``setup.cfg`` and a ``start.py`` files 
within their root directory to specify to AiiDAlab the plugin metadata and how to display 
the start banner for the plugin. From here each page defined within the application is 
described by a jupyter notebook (\*.ipynb) file which may call components from the 
core python package. 


Core Requirements
-----------------

Project Meta-Data
~~~~~~~~~~~~~~~~~

AiiDAlab uses the python style ``setup.cfg`` configuration file to define project meta-data which 
it parses and associates with the plugin inside the AiiDAlab interface. This file must be 
present within the plugins root directory or within a special ``.aiidalab`` directory under the 
project root. Within it all the required meta-data can be specified such as project name, description,
version number etc. More detail on the available and required meta-data inputs can be found 
`here <https://aiidalab.readthedocs.io/en/latest/app_development/publish.html>`_ .

Start Banner
~~~~~~~~~~~~

To be displayed in the core AiiDAlab home interface a plugin must contain a start banner, which can 
either be defined in a python file (``start.py``) or a markdown file (``start.md``). This is the main 
interface from the AiiDAlab home page to your developed plugin so should contain any relevant logos 
and navigation buttons for the plugin. The example presented alongside this documentation in the 
`github repo <https://github.com/stfc/alc-ux>`_ defines a python based approach with an embedded 
HTML element which provides the application logo as a navigation button alongside a selection 
of navigation buttons below the logo which all navigate to different components of the underlying 
AiiDAlab plugin. 


Main Application
~~~~~~~~~~~~~~~~

The main AiiDAlab plugin application will be written in jupyter notebook files ``.ipynb`` which 
can either be self contained or for more complex UI project will reference an underlying python 
library associated with the plugin. For the `example plugin <https://github.com/stfc/alc-ux>`_ 
provided the main application page is defined in ``main.ipynb`` and refers to the ``aiidalab_alc`` 
python library which contains all the required UI elements and how they interact with each other
and the user. This library is defined in ``src/aiidalab-alc/`` and has various components that 
each contribute to different aspects of the AiiDAlab plugins UI. 


Making Your App Discoverable
----------------------------

When installing new plugins via the AiiDAlab plugin manager interface, plugins will be installed 
and configured into the correct directories to be picked up by the AiiDAlab home page. However, 
when developing plugins it is often required to manually manipulate these directories to make 
sure your in-development application can be found and displayed by AiiDAlab. By default AiiDAlab 
will create an ``apps`` directory within the home space of the container running the jupyter server
instance. This is where all AiiDAlab plugin apps reside and where the home app looks to determine 
which plugins are available. The process for AiiDAlab to install an application typically follows 
as first checkout a specific release version of the plugin's code from its online host e.g. GitHub 
into the ``apps`` folder. Following this it will run a pip install within the root source directory 
of the plugin if required to install the required backend python UI package. 


General Plugin Design Concepts
------------------------------

Model-View-Controller Paradigm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is recommended that an AiiDAlab plugin follows the widely recognised Model-View-Controller 
design paradigm for UI development. 
The core UI package will use ``IPywidgets`` (or aiidalab's own pre-configured widgets) to display 
the various UI components that a user will interact with (described later). This defines the 
*view* for the application. The data that is being handled should exist seperate to any visual 
components that are part of the applications *view* layer. They are handled by the ``traitlets``
python packages and can be dynamically linked to user inputs through the *view* layer but should exist indendantly, thus 
defining the *model* layer. The controller layer is an optional additional layer that defines user 
controll over that application that doesn't directly interact with any of the stored data. 


Widgets
~~~~~~~

Jupyter notebook based GUI's rely on components called widgets, often (but not exclusively) provided 
by a library called `IPywidgets <https://ipywidgets.readthedocs.io/en/stable/>`_\. These form the core 
UI elements that can be used as building blocks to create your application. They provide widgets for 
formatting such as vertical/horizontal layout boxes, as well as different forms of input/output or 
interaction interfaces, such as text display/input boxes, drop down lists or buttons. These can be 
combined to build a complex GUI application. 

In addition to the core widgets provided by IPywidgets, AiiDAlab provides several of its own widgets
specifically tailored for interacting with AiiDA components such as data structures and the database
itself. These are provided in the *aiidalab-widgets-base* python package and are documented
`here <https://aiidalab-widgets-base.readthedocs.io/en/latest/>`_\.

Each widget will expose a data value, typically named ``value`` if using IPywidgets, which contains
the user's input and which can be linked to internal data variables to dictate functionality within
the AiiDAlab application using the ``link``, ``dlink`` or ``observe`` functions from the
**traitlets** module.


AiiDA Integration
-----------------

At its core AiiDAlab is designed to be a UI for the AiiDA workflow management software, therefore
deep integration between the two is essential. This goes beyond simply designing your AiiDAlab UI
to follow a given AiiDA plugin but would also include how to interact with and manage the AiiDA 
database, create AiiDA code instances and remote computer connections or visualise full data
provenance to understand how data has been generated. 

At present the current AiiDAlab home UI
does not expose any of this functionality therefore it is up to individual plugins to expose what
they deem required for their user base. However, AiiDAlab provides several notebook pages or 
pre-configured widgets which will provide the functionality required and can be included within
any plugin application. 


.. _aiidalab_registry:

The AiiDAlab Plugin Registry
----------------------------

AiiDAlab hosts many plugin applications in a registry which is exposed within the core AiiDAlab UI
allowing a user to interactively install and uninstall plugins depending on their desired workflows. Therefore, it is very valuable for any plugin that is developed to be included within
this registry. 

The registry itself is based on `github <https://github.com/aiidalab/aiidalab-registry>`_ and
is open to contributions which add new applications to it. New plugins can be registered by editing
the ``apps.yaml`` file within the registry's repository to include an entry for the new plugin,
which points to the source code for the new plugin e.g. its GitHub link. 

.. code:: yaml

    hello-world:
        releases:
            - "git+https://github.com/aiidalab/aiidalab-hello-world.git@master:"


Additional keys can be
included in the URL to limit the registry entries to certain released versions of the plugin. These
options are discussed in more detail in the 
`AiiDAlab documentation <https://aiidalab.readthedocs.io/en/latest/app_development/publish.html>`_\.
