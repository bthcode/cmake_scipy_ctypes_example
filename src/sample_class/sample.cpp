#include "sample.h"

#include <vector>
#include <iostream>

int g_x;

sample::sample()
{
    this->x = g_x;
    g_x++;
    std::cout << "Initializing sample(" << this->x << ")" << std::endl;
}

sample::~sample()
{
    std::cout << "Deleting sample(" << this->x << ")" << std::endl;
}

void
sample::set_vec1( double * i_vec, std::size_t len )
{
    vec1.resize( len );
    std::copy( i_vec, i_vec+len, vec1.begin() );
}
// END set_vec1

void
sample::set_vec2( double * i_vec, std::size_t len )
{
    vec2.resize( len );
    std::copy( i_vec, i_vec+len, vec2.begin() );
}
// END set_vec2

bool sample::add_vecs( double * o_vec, unsigned int len )
{
    if ( ( vec1.size() == 0 ) || ( vec1.size() != vec2.size() ) )
    {
        return false;
    }

    unsigned int max_elements = std::min< unsigned int >( vec1.size(), len );
    for ( std::size_t idx = 0; idx < max_elements; idx++ )
    {
        o_vec[idx] = vec1[idx] + vec2[idx];
    }

    return true;
}
// - END add_vecs
