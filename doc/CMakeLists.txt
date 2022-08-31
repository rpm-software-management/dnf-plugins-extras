# html and man documentation are separate targets, apparently there's no way to
# tell sphinx-build to do them both in one go:

if (${PYTHON_VERSION_MAJOR} STREQUAL "2")
    SET(SPHINX_BUILD_NAME "sphinx-build")
else()
    SET(SPHINX_BUILD_NAME "sphinx-build-3")
endif()

ADD_CUSTOM_TARGET (doc-html
		  PYTHONPATH=${CMAKE_SOURCE_DIR} ${SPHINX_BUILD_NAME} -b html
		  ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}
		  COMMENT "Building html documentation")
ADD_CUSTOM_TARGET (doc-man
		  PYTHONPATH=${CMAKE_SOURCE_DIR} ${SPHINX_BUILD_NAME} -b man
		  ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}
		  COMMENT "Building manpage documentation")
ADD_CUSTOM_TARGET (doc)
ADD_DEPENDENCIES (doc doc-html doc-man)

INSTALL(FILES ${CMAKE_CURRENT_BINARY_DIR}/dnf-kickstart.8
    ${CMAKE_CURRENT_BINARY_DIR}/dnf-snapper.8
    ${CMAKE_CURRENT_BINARY_DIR}/dnf-tracer.8
    ${CMAKE_CURRENT_BINARY_DIR}/dnf-showvars.8
	DESTINATION share/man/man8)
if (${PYTHON_VERSION_MAJOR} STREQUAL "3")
    INSTALL(FILES ${CMAKE_CURRENT_BINARY_DIR}/dnf-rpmconf.8
        ${CMAKE_CURRENT_BINARY_DIR}/dnf-torproxy.8
        DESTINATION share/man/man8)
endif()
