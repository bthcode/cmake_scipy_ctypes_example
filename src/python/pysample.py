#!/usr/bin/python

import ctypes as C
from ctypes import cdll
import numpy as np
import pprint
import os

class pysample:
    def __init__(self):
        self.init_library()
    # end __init__

    def init_library(self):
        print "############## LOADING LIBRARY ####################"
         
        searchpath = os.path.dirname( __file__ )
        print searchpath
        self.lib = np.ctypeslib.load_library("libsample_interface.so", searchpath )

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
        print "############# DELETING INSTANCE ###################"
        self.lib.DeleteInstanceOfSample( self.instance )
        pass
    # end cleanup_library

    def add(self, x,y ):
        z = np.zeros( len(y) )
        print "############# CALLING FUNCTIONS ###################"
        self.lib.SetVec1( self.instance,x.ctypes.data_as(C.POINTER(C.c_double)), len(x))
        self.lib.SetVec2( self.instance,y.ctypes.data_as(C.POINTER(C.c_double)), len(y))
        res = self.lib.add_vecs( self.instance, z.ctypes.data_as( C.POINTER( C.c_double)), len(z) )
        return z
    # end add
#end class pysample

if __name__=="__main__":
    p = pysample()
    x = np.arange(12, dtype=np.double)
    y = np.arange(12, dtype=np.double)
    z = p.add( x, y )

    print " [in1] {0}".format( pprint.pformat( x ) )
    print " [in2] {0}".format( pprint.pformat( y ) )
    print " [out] {0}".format( pprint.pformat( z ) )
    p.cleanup()






