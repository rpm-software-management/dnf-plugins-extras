INSTALL (FILES
         "dnf-system-upgrade.service"
         "dnf-system-upgrade-cleanup.service"
         "dnf-offline-upgrade.service"
         "dnf-offline-upgrade-cleanup.service"
         DESTINATION ${SYSTEMD_DIR})
