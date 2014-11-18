FILE( GLOB C_INTERFACE_C "*.cpp" )
FILE( GLOB C_INTERFACE_H "*.h" )

# Library for using the stereo interface
ADD_LIBRARY( sample_interface SHARED ${C_INTERFACE_C} ${C_INTERFACE_H} )
TARGET_LINK_LIBRARIES( sample_interface
  sample )

INSTALL(TARGETS sample_interface
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION python
  ARCHIVE DESTINATION python
)
