CMAKE_MINIMUM_REQUIRED (VERSION 3.5.0...4.0.2)
PROJECT (dnf-plugins-extras NONE)

cmake_policy(SET CMP0148 OLD)
FIND_PACKAGE (PythonInterp 3 EXACT REQUIRED)

EXECUTE_PROCESS(COMMAND ${PYTHON_EXECUTABLE} -c "from sys import stdout; from sysconfig import get_path; stdout.write(get_path('purelib'))" OUTPUT_VARIABLE PYTHON_INSTALL_DIR)
MESSAGE(STATUS "Python install dir is ${PYTHON_INSTALL_DIR}")

SET (SYSCONFDIR /etc)

ADD_SUBDIRECTORY (doc)
ADD_SUBDIRECTORY (etc)
ADD_SUBDIRECTORY (plugins)
ADD_SUBDIRECTORY (po)
