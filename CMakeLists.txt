PROJECT (dnf-plugins-extras NONE)
CMAKE_MINIMUM_REQUIRED (VERSION 2.4)

FIND_PACKAGE (PythonInterp 3 EXACT REQUIRED)

EXECUTE_PROCESS(COMMAND ${PYTHON_EXECUTABLE} -c "from sys import stdout; from sysconfig import get_path; stdout.write(get_path('purelib'))" OUTPUT_VARIABLE PYTHON_INSTALL_DIR)
MESSAGE(STATUS "Python install dir is ${PYTHON_INSTALL_DIR}")

SET (SYSCONFDIR /etc)

find_package (PkgConfig)

if (PKG_CONFIG_FOUND)
  pkg_search_module (SYSTEMD systemd)
  if (SYSTEMD_FOUND)
    execute_process (COMMAND ${PKG_CONFIG_EXECUTABLE} --variable=systemdsystemunitdir systemd
                     OUTPUT_VARIABLE SYSTEMD_DIR
                     OUTPUT_STRIP_TRAILING_WHITESPACE)
  endif ()
endif()

if (NOT SYSTEMD_DIR)
  set (SYSTEMD_DIR /usr/lib/systemd/system)
endif ()

ADD_SUBDIRECTORY (doc)
ADD_SUBDIRECTORY (etc)
ADD_SUBDIRECTORY (plugins)
ADD_SUBDIRECTORY (po)
