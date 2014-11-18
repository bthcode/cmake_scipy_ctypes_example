#ifndef SAMPLE_INTERFACE_H
#define SAMPLE_INTERFACE_H

#include "sample.h"
#include <iostream>

#ifdef WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif


#ifdef __cplusplus
extern "C" {
#endif

EXPORT void * CreateInstanceOfSample( void );

EXPORT void DeleteInstanceOfSample (void *ptr);

EXPORT void SetVec1( void * ptr, double * data, unsigned int len );

EXPORT void SetVec2( void * ptr, double * data, unsigned int len );

EXPORT int add_vecs( void * ptr, double * result, unsigned int len );

#ifdef __cplusplus
}
#endif

#endif
