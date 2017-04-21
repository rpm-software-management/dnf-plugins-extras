if (${PYTHON_DESIRED} STREQUAL "3")
INSTALL (FILES torproxy.conf DESTINATION ${SYSCONFDIR}/dnf/plugins)
INSTALL (FILES rpmconf.conf DESTINATION ${SYSCONFDIR}/dnf/plugins)
endif()
