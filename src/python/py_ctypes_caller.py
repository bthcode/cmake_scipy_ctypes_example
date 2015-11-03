#!/usr/bin/python

import ctypes as C
from ctypes import cdll
import numpy as np
import pprint
import os

class py_ctypes_caller:
    ''' Sample class to show good practices for interfacing with a C interface to C++ via ctypes '''
    def __init__(self):
        self.init_library()
    # end __init__

    def init_library(self):
        ''' Library Initialization:
              - Loads .so / .dll
              - Tells ctypes the arg types for the functions we want to call
              - Inits the class via the CreateInstance... call
                  - a C pointer to the C++ class is stored as an integer in this class as self.instance
                  - it will be cast to the correct type before use
        '''
        print "############## LOADING LIBRARY ####################"
         
        searchpath = os.path.dirname( __file__ )
        print searchpath
        self.lib = np.ctypeslib.load_library("libsample_interface.dylib", searchpath )

        self.lib.CreateInstanceOfSample.restype = C.c_ulong

        self.lib.SetVec1.argtypes = [  C.POINTER( None ), 
                                       C.POINTER(  C.c_double ),
                                       C.c_int ]

        self.lib.SetVec2.argtypes = [  C.POINTER( None ), 
                                       C.POINTER(  C.c_double ),
                                       C.c_int ]

        self.lib.add_vecs.argtypes = [ C.POINTER( None ), 
                                       C.POINTER( C.c_double ), 
                                       C.c_int ]
        self.lib.add_vecs.restype  = C.c_int


        print "############# CREATING INSTANCE ###################"
        self.instance  = self.lib.CreateInstanceOfSample()
    # end init_library

    def cleanup(self):
        ''' Shows clean deletion of an C++ object via ctypes '''
        print "############# DELETING INSTANCE ###################"
        self.lib.DeleteInstanceOfSample( self.instance )
        pass
    # end cleanup_library

    def add(self, x,y ):
        ''' Sample method for calling C++ class methods via a c-interface from ctypes '''
        z = np.zeros( len(y) )
        print "############# CALLING FUNCTIONS ###################"

        # ----------------------------------------------------------------
        # NOTE on Numpy / Ctypes Integration:
        #  - numpy maintains its data in fixed length memory buffers 
        #  - each numpy object has a ctypes member that provides access to those buffers
        #  - you can pass pointers to those buffers to C as show below
        # ---------------------------------------------------------------
        self.lib.SetVec1( self.instance,x.ctypes.data_as(C.POINTER(C.c_double)), len(x))
        self.lib.SetVec2( self.instance,y.ctypes.data_as(C.POINTER(C.c_double)), len(y))
        res = self.lib.add_vecs( self.instance, z.ctypes.data_as( C.POINTER( C.c_double)), len(z) )
        return z
    # end add
#end class py_ctypes_caller

if __name__=="__main__":
    p = py_ctypes_caller()
    x = np.arange(12, dtype=np.double)
    y = np.arange(12, dtype=np.double)
    z = p.add( x, y )

    print " [in1] {0}".format( pprint.pformat( x ) )
    print " [in2] {0}".format( pprint.pformat( y ) )
    print " [out] {0}".format( pprint.pformat( z ) )
    p.cleanup()






