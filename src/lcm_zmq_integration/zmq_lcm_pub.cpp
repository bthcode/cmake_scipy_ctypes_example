/********************************************************
 * SAMPLE Integration of LCM Serialization and 
 *  ZMQ Message Passing
 *
 * PUBLISHER
 *******************************************************/

#include <example_lcm/image_t.hpp>
#include <iostream>
#include <zmq.hpp>
#include <stdlib.h>


int main (void) 
{
    //--------------------------------------------
    //  Prepare our context and publisher
    //  NOTE: socket type is PUB
    //        socket connect method is bind
    //--------------------------------------------
    zmq::context_t context (1);
    zmq::socket_t publisher (context, ZMQ_PUB);
    publisher.bind("tcp://*:5556");

    //--------------------------------------
    // Buffer and constants for
    //  serialization
    //  FORMAT:
    //   - 3 character key
    //   - 4093 buffer
    //--------------------------------------
    int counter = 0;
    int offset  = 0;
    int MAXLEN  = 4096;
    int KEYLEN  = 3;
    int MSGMAX  = MAXLEN - KEYLEN;
    char* buf       = new char[MAXLEN];
    char* msg_start = buf + KEYLEN;
    

    //for ( std::size_t ii=0; ii < 1024; ii++ )
    while ( 1 )
    {
        // Zero out the buffer - probably overkill
        memset( buf, 0, MAXLEN );

        // Populate an LCM data structure with made up data
        example_lcm::image_t I;
        I.data.resize(12);
        for ( int i =0; i < I.data.size(); i++ )
        {
            I.data[i] = i;
        }
        I.data[0] = counter;
        I.height = 4;
        I.width  = 3;
        I.size   = I.data.size();

        // Serialize
        int msg_len = I.encode( (void*)(buf+KEYLEN), 0, MSGMAX );

        // Check for errors in serialization
        if ( (msg_len <= 0 ) || ( msg_len > MSGMAX ) )
        {
            std::cout << "warning: msg_len = " << msg_len << std::endl;
            continue;
        }
        
        // Adjust message length to include keyword
        msg_len += KEYLEN;

        // Set keyword.  Simulate multiple message types by
        //   changing the key on odd iterations
        if (( counter % 2 ) == 0 )
        {
            // Key
            buf[0] = 'K';
            buf[1] = 'E';
            buf[2] = 'Y';
        }
        else
        {
            buf[0] = 'X';
            buf[1] = 'Y';
            buf[2] = 'Z';
        }

        // Set up the ZMQ output buffer
        zmq::message_t message(msg_len);
        memcpy( message.data(), buf, msg_len );
        
        // Fire and forget
        publisher.send(message);

        counter++;

    }
    if ( NULL != buf )
        delete[] buf;
    return 0;
}
