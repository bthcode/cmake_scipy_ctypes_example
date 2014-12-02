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

/**
 * @brief Creates an instance of a C++ class, passes the pointer back as a void*
 * @returns Pointer to instance as void * (for python storage as int)
 */
EXPORT void * CreateInstanceOfSample( void );

/**
 * @brief Deletes an instance of a C++ class.
 * @param [in] ptr: A pointer to a C++ class.  Comes in as a void * and is typecast internally
 */
EXPORT void DeleteInstanceOfSample (void *ptr);

/**
 * @brief Copies data from a pointer to an internal C++ class member.  
 * @param [in] ptr: A pointer to a C++ class.  Comes in as a void * and is typecast internally
 * @param [in] data: A pointer to a data buffer (for example, a numpy ctypes buffer)
 * @param [in] len: number of elements in the data buffer
 */
EXPORT void SetVec1( void * ptr, double * data, unsigned int len );

/**
 * @brief Copies data from a pointer to an internal C++ class member.  
 * @param [in] ptr: A pointer to a C++ class.  Comes in as a void * and is typecast internally
 * @param [in] data: A pointer to a data buffer (for example, a numpy ctypes buffer)
 * @param [in] len: number of elements in the data buffer
 */
EXPORT void SetVec2( void * ptr, double * data, unsigned int len );

/**
 * @brief Copies data from a pointer to an internal C++ class member.  
 * @param [in] ptr: A pointer to a C++ class.  Comes in as a void * and is typecast internally
 * @param [out] result: A pointer to a result buffer (for example, a numpy ctypes buffer).  Buffer is assumed to be allocated before calling.  
 * @param [in] len: number of elements to write to the buffer
 */
EXPORT int add_vecs( void * ptr, double * result, unsigned int len );

#ifdef __cplusplus
}
#endif

#endif
