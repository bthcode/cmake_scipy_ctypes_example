FILE( GLOB SAMPLE_C "*.cpp" )
FILE( GLOB SAMPLE_H "*.h" )
FILE( GLOB SAMPLE_HPP "*.hpp" )

ADD_LIBRARY( sample
             ${SAMPLE_C} 
             ${SAMPLE_H} 
             ${SAMPLE_HPP} )

INSTALL( TARGETS sample
         RUNTIME DESTINATION bin
         LIBRARY DESTINATION lib
         ARCHIVE DESTINATION lib )


