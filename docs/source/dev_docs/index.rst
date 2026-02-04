Developer Guide
===============

Welcome to the developer's guide to **AiiDAlab** applications for the ALC. 

AiiDAlab is a web based graphical user interface (GUI) for the popular scientific workflow 
management software package AiiDA. It presents a step-by-step approach to defining complex 
workflows utilising the relevant AiiDA plugins for the core computation. It is based on 
the ``appmode`` plugin for jupyter notebooks, enabling complex UI elements to be hosted 
within a web hosted jupyter notebook environment. This abstracts away many of the more 
challenging concepts of the AiiDA workflow itself whilst providing user friendly UI 
controls to interact with the provided plugins. 

This document aims to provide all the information required to develop AiiDA/AiiDAlab applications
for use with ALC/STFC software projects. It includes details on how to create and run the required 
docker images to package additional components on top of the core AiiDAlab application, as 
well as how to deploy these to users either locally or via a cloud host such as ADA.

Any questions can be directed to the `discussions <https://github.com/stfc/alc-ux/discussions>`_
page on GitHub or to benjamin.speake@stfc.ac.uk. 


.. toctree::
   :maxdepth: 2

   aiidalab_app_design
   workflow_implementation
   containers
   startup_and_deployment
