#ifndef EXAMPLE_TEST_H
#define EXAMPLE_TEST_H

#include <vector>

class sample {

    public:

    sample();
    ~sample();
    
    bool add_vecs( double * o_vec, unsigned int len );

    void set_vec1( double * i_vec, std::size_t len );
    void set_vec2( double * i_vec, std::size_t len );

    std::vector< double > result;

    private:
    std::vector< double > vec1;
    std::vector< double > vec2;
    int x;
}; 
// END class sample

#endif
