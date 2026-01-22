Developer Guide
===============

Welcome to the developer's guide to AiiDAlab applications for the ALC. 

This document contains all the information required to develop AiiDA/AiiDAlab applications
for use with ALC software projects. It includes details on how to create and run the required 
docker images to package additional components on top of the core AiiDAlab application, as 
well as how to deploy these to users either locally or via a cloud host such as ADA.

Introduction
============

AiiDAlab is a web based graphical user interface (GUI) for the popular scientific workflow 
management software package AiiDA. It presents a step-by-step approach to defining complex 
workflows utilising the relevant AiiDA plugins for the core computation. It is based on 
the ``appmode`` plugin for jupyter notebooks, enabling complex UI elements to be hosted 
within a web hosted jupyter notebook environment. This abstracts away many of the more 
challenging concepts of the AiiDA workflow itself whilst providing user friendly UI 
controls to interact with the provided plugins. 

This guide aims to help developers get started with AiiDAlab plugin design and 
deployment across the wide variety of software applications developed within 
the ALC and STFC.  

Any questions can be directed to the `discussions <https://github.com/stfc/alc-ux/discussions>`_
page on GitHub or to benjamin.speake@stfc.ac.uk. 


Contents
========

.. toctree::
   :maxdepth: 2

   aiidalab_app_design
   containers
   startup_and_deployment