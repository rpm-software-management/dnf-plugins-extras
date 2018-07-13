# html and man documentation are separate targets, apparently there's no way to
# tell sphinx-build to do them both in one go:
ADD_CUSTOM_TARGET (doc-html
		  PYTHONPATH=${CMAKE_SOURCE_DIR} sphinx-build -b html
		  ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}
		  COMMENT "Building html documentation")
ADD_CUSTOM_TARGET (doc-man
		  PYTHONPATH=${CMAKE_SOURCE_DIR} sphinx-build -b man
		  ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}
		  COMMENT "Building manpage documentation")
ADD_CUSTOM_TARGET (doc)
ADD_DEPENDENCIES (doc doc-html doc-man)

INSTALL(FILES ${CMAKE_CURRENT_BINARY_DIR}/dnf.plugin.kickstart.8
    ${CMAKE_CURRENT_BINARY_DIR}/dnf.plugin.snapper.8
    ${CMAKE_CURRENT_BINARY_DIR}/dnf.plugin.system-upgrade.8
    ${CMAKE_CURRENT_BINARY_DIR}/dnf.plugin.tracer.8
	DESTINATION share/man/man8)
if (${PYTHON_VERSION_MAJOR} STREQUAL "3")
    INSTALL(FILES ${CMAKE_CURRENT_BINARY_DIR}/dnf.plugin.rpmconf.8
        ${CMAKE_CURRENT_BINARY_DIR}/dnf.plugin.torproxy.8
        DESTINATION share/man/man8)
endif()
