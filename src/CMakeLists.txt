#################################
#
# Template Project
#
#################################
CMAKE_MINIMUM_REQUIRED( VERSION 2.6 )

PROJECT( TemplateProject )

# Installation directory for build
SET( CMAKE_INSTALL_PREFIX
  ${CMAKE_CURRENT_BINARY_DIR}/install )

#---------------------------------------
# Options
#---------------------------------------
OPTION( BUILD_TESTS "Build tests?"  True )

#---------------------------------------
# Useful Macro for adding definitions
#---------------------------------------
MACRO( CROSS_PLATFORM_ADD_DEFINITION NAME )
  IF( WIN32 )
    ADD_DEFINITIONS( "/D${NAME}" )
    MESSAGE( STATUS "Adding definition /D${NAME}" )
  ELSE()
    ADD_DEFINITIONS( "-D${NAME}" )
    MESSAGE( STATUS "Adding definition -D${NAME}" )
  ENDIF()
ENDMACRO( CROSS_PLATFORM_ADD_DEFINITION )

#----------------------------------------
# Doxygen Configuration
#----------------------------------------
FIND_PACKAGE(Doxygen)
IF(DOXYGEN_FOUND)

    CONFIGURE_FILE( ${CMAKE_CURRENT_SOURCE_DIR}/../template_project.doxy 
                    ${CMAKE_CURRENT_BINARY_DIR}/template_project.doxy @ONLY )

    ADD_CUSTOM_TARGET( template_project_docs
                       ${DOXYGEN_EXECUTABLE} 
                       ${CMAKE_CURRENT_BINARY_DIR}/template_project.doxy
                       WORKING_DIRECTORY 
                       ${CMAKE_CURRENT_BINARY_DIR}
                       COMMENT "Generating documentation with Doxygen" VERBATIM )

endif(DOXYGEN_FOUND)

#-------------------------------------------------------------------
# Required for linking bits as a shared library
#-------------------------------------------------------------------
IF( WIN32 )
    # Removes warnings for functions like strcpy, sprintf
    ADD_DEFINITIONS( "/D_CRT_SECURE_NO_DEPRECATE" )
 
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /INCREMENTAL:NO" )
  
    # Removes windows.h redefinitions of std::min and std::max
    ADD_DEFINITIONS( "/DNOMINMAX" )
    MESSAGE( "I don't know how to do PIC on Windows" )
ELSE( WIN32 )
    # Position-independent code, lots of warnings
    ADD_DEFINITIONS( "-fPIC -Wall -Wextra" )
    # Strict build - currently only running on Linux - Windows errors
    # are very different from the Linux ones and we're not at a point
    # where we can maintain the strictness with both sets.
    OPTION( BUILD_STRICT "Strict build? Warnings treated as errors" False )
    ADD_DEFINITIONS( "-Werror" )
ENDIF( WIN32 )

#
# Build tests?
#
IF ( BUILD_TESTS )
  MESSAGE( STATUS "Enabling Testing..." )
  ENABLE_TESTING()
ENDIF( BUILD_TESTS )


#-----------------------------------------------------------
# INCLUDE-DIRS
#-----------------------------------------------------------
INCLUDE_DIRECTORIES( sample_class 
                     ctypes_interface )

#-----------------------------------------------------------
# SUB-DIRS
#-----------------------------------------------------------
ADD_SUBDIRECTORY( sample_class )
ADD_SUBDIRECTORY( ctypes_interface  )

INSTALL( DIRECTORY python 
         DESTINATION python/.. )
