/********************************************************
 * SAMPLE Integration of LCM Serialization and 
 *  ZMQ Message Passing
 *
 * SUBSCRIBER
 *******************************************************/

#include <example_lcm/image_t.hpp>
#include <zmq.hpp>
#include <iostream>
#include <sstream>

int main (int argc, char *argv[])
{
    
    //-------------------------------------------
    //  Prepare our context and subscriber
    //  NOTE: socket type is SUB
    //        socket connect method is connect
    //--------------------------------------------
    zmq::context_t context (1);

    //  Socket to talk to server
    std::cout << "connecting to server...\n" << std::endl;
    zmq::socket_t subscriber (context, ZMQ_SUB);
    subscriber.connect("tcp://localhost:5556");

    //--------------------------------------
    // Buffer and constants for
    //  serialization
    //  FORMAT:
    //   - 3 character key
    //   - 4093 buffer
    //--------------------------------------
    int MAXLEN  = 4096;
    int KEYLEN  = 3;
    int MSGMAX  = MAXLEN - KEYLEN;
    const char *filter = "KEY";

    //--------------------------------------
    // Tell zmq to filter for messages 
    //  starting with 'KEY'
    //--------------------------------------
    subscriber.setsockopt(ZMQ_SUBSCRIBE, filter, strlen (filter));

    std::cout << "Beginning Loop..." << std::endl;

    for ( std::size_t ii=0; ii < 1024; ii++ )
    {
        //-------------------------------
        // Receive a message
        //-------------------------------
        zmq::message_t message;
        subscriber.recv(&message);

        // LCM object to decode into
        example_lcm::image_t I;

        // Storage of the raw bytestring from zmq
        char * buf = (char*) message.data();

        // Print and advance past the key
        std::cout << buf[0] << buf[1] << buf[2] << ": "; std::cout.flush();
        buf += 3;

        // ----------------------------------
        // De-serialize the message
        // ----------------------------------
        I.decode( (void*) buf, 0, MSGMAX );

        // The rest is just printing
        std::cout << I.size  << " " 
                  << I.width << " " 
                  << I.height << "(";
        for ( std::size_t ii=0; ii < I.size; ii++ ) 
            std::cout << (int)I.data[ii] << ",";
        std::cout << ")" << std::endl;
    }

    return 0;
}
