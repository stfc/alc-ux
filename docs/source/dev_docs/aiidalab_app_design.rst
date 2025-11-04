Plugin Design 
=============

AiiDAlab plugins are designed as jupyter notebook UIs with a core package providing the 
UI components. Each plugin is required to have a ``setup.cfg`` and a ``start.py`` files 
within their root directory to specify to AiiDAlab the plugin metadata and how to display 
the start banner for the plugin. From here each page defined within the application is 
described by a jupyter notebook (\*.ipynb) file which may call components from the 
core python package. 

Model-View-Controller Paradigm
------------------------------

It is recommended that an AiiDAlab plugin follows the widely recognised Model-View-Controller 
design paradigm for UI development. 
The core UI package will use ``IPywidgets`` (or aiidalab's own pre-configured widgets) to display 
the various UI components that a user will interact with. This defines the *view* for the application.
The data that is being handled should exist seperate to any visual components that are part 
of the applications *view* layer. They are handled by the ``traitlets`` python packages and can 
be dynamically linked to user inputs through the *view* layer but should exist indendantly, thus 
defining the *model* layer. The controller layer is an optional additional layer that defines user 
controll over that application that doesn't directly interact with any of the stored data. 