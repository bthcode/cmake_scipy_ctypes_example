cmake_scipy_ctypes_example
==========================

Examples of Integration of CMake, Scipy, Ctypes, IPython

List of examples:
----------------

1. python / numpy / ctypes interface

  Shows how to communicate between python and C/C++ in a very easy way.

     - sample_class: a sample C++ class 
     - ctypes_interface: a c-style interface for communicating with sample_class
     - python: pysample.py: a python class and main loop that demonstrates how to use the ctypes interface

   Or:

   pysample.py <- ctypes -> sample_interface <- C/C++ -> sample_class


2. gdb-plot:

  Shows how to plot stuff from gdb using gdb's built-in python system and matplotlib    
   
3. lcm / zmq interface:

  Shows how to use the lcm system for message serialization with zeromq for data transport

4.  py_crust_example.py:
  
  Shows how to enable a python shell from within any wxPython application




