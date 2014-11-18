#include "sample_interface.h"
#include "sample.h"
#include <iostream>


#ifdef __cplusplus
extern "C" {
#endif

void * CreateInstanceOfSample( void )
{
    return new(  sample );
}

 void DeleteInstanceOfSample (void *ptr)
{
     sample * ref = reinterpret_cast<sample*>(ptr);
     delete( ref ); 
}

 void SetVec1( void * ptr, double * data, unsigned int len )
{
    if ( len <= 0 ) { return; }

    sample * ref = reinterpret_cast<sample*>(ptr);
    ref->set_vec1( data, len );    
}

void SetVec2( void * ptr, double * data, unsigned int len )
{
    if ( len <= 0 ) { return; }

    sample * ref = reinterpret_cast<sample*>(ptr);
    ref->set_vec2( data, len );
}

int add_vecs( void * ptr, double * result, unsigned int len )
{
    sample * ref = reinterpret_cast<sample*>(ptr);
    ref->add_vecs( result, len );

    return 0;    
}


#ifdef __cplusplus
}
#endif
