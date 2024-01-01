#!/bin/bash

########################################################################################################################
# Run this script as sudo to update the project environment as the service user and restart the systemd service. This
# expects the system components to have been installed as defined in ./server_install_system_components.sh.
#
# Note: This does not update the local project files, so do that with git prior to running this script.
#
# Dependencies:
# - systemd
# - nginx
# - systemd-analyze
########################################################################################################################
set -e # Stop script if any command fails

SERVICE_USER='com_jrdbnntt_wedding_nc'

ORIGINAL_WORKING_DIR="$(pwd)"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "${SCRIPT_DIR}/server_config_vars.sh"
cd "${PROJECT_DIR}" || exit 1

# Verify config files are valid
test_nginx_config
test_systemd_config

# Ensure all project files are owned by service user
chown -R "${SERVICE_USER}:${FILE_OWNERSHIP_GROUP}" "${PROJECT_DIR}"
chown -R "${SERVICE_USER}:${FILE_OWNERSHIP_GROUP}" "${DJANGO_SERVER_LOG_DIR}"

# Stop service
systemctl stop "${SYSTEMD_SERVICE_NAME}"

# Archive logs
cd "${DJANGO_SERVER_LOG_DIR}" || exit 1
LOG_ARCHIVE_PATH="${DJANGO_SERVER_LOG_DIR}/logs_${FILENAME_DATETIME_NOW_SUFFIX}.tar.gz"
FILES_TO_LOG=$(runuser -g "${SERVICE_USER}" -u "${SERVICE_USER}" -- find -P "." -mindepth 1 -maxdepth 1 '(' -type d,f ! -name '*.gz' ')' -printf "%P\0")
echo -n "${FILES_TO_LOG}" | xargs -0 runuser -g "${SERVICE_USER}" -u "${SERVICE_USER}" -- tar -czvf "${LOG_ARCHIVE_PATH}"
echo -n "${FILES_TO_LOG}" | xargs -0 runuser -g "${SERVICE_USER}" -u "${SERVICE_USER}" -- rm -rf
cd "${PROJECT_DIR}" || exit 1

# Restart service and reload nginx
systemctl daemon-reload
systemctl start "${SYSTEMD_SERVICE_NAME}"
nginx -s reload

echo "Server updated"
cd "${ORIGINAL_WORKING_DIR}" || exit 1
