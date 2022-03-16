#!/bin/bash

########################################################################################################################
# Run this script to as sudo to create at service user, install the environment as the service user, install the systemd
# service to run the http server with said service user, and configure ngnix.
#
# This expects the repository to be cloned to /var/www/com_jrdbnntt_wedding and will error out if that is not the case.
#
# Dependencies:
# - nginx
# - systemd
# - user group 'www-data'
# - systemd-analyze
# - ssl cert at '/etc/nginx/certs/com_jrdbnntt_wedding/cert.crt'
# - ssl cert key at '/etc/nginx/certs/com_jrdbnntt_wedding/cert.key'
########################################################################################################################
set -e # Stop script if any command fails

ORIGINAL_WORKING_DIR="$(pwd)"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "${SCRIPT_DIR}/server_config_vars.sh"
cd "${PROJECT_DIR}" || exit 1

# Verify install dir
if [ ! "${PROJECT_DIR}" = "${REQUIRED_REPO_INSTALL_DIR}" ]; then
  echo "Install dir, '${PROJECT_DIR}', does not match the required install dir, '${REQUIRED_REPO_INSTALL_DIR}'"
  exit 1
fi

# Verify config files are valid
nginx -t -c "${PROJECT_NGINX_CONFIG_PATH}"
systemd-analyze verify "${PROJECT_SYSTEMD_SERVICE_PATH}"

# Build log dir
DJANGO_PROJECT_LOG_DIR="./logs"
if [ ! -d "${DJANGO_SERVER_LOG_DIR}" ]; then
  mkdir -p "${DJANGO_SERVER_LOG_DIR}"
fi
if [ ! -L "${DJANGO_PROJECT_LOG_DIR}" ]; then
  if [ -d "${DJANGO_PROJECT_LOG_DIR}" ]; then
    mv "${DJANGO_PROJECT_LOG_DIR}/*" "${DJANGO_SERVER_LOG_DIR}"
  fi
  ln -s "${DJANGO_SERVER_LOG_DIR}" "${DJANGO_PROJECT_LOG_DIR}"
fi

# Create service user
if id "${SERVICE_USER}" &>/dev/null; then
    echo "Using existing user '${SERVICE_USER}' as the service user"
else
    echo "Creating system user '${SERVICE_USER}'..."
    useradd --system "${SERVICE_USER}"
fi

# Allow service user to access required files
chown -R "${SERVICE_USER}:${FILE_OWNERSHIP_GROUP}" "${PROJECT_DIR}"
chown -R "${SERVICE_USER}:${FILE_OWNERSHIP_GROUP}" "${DJANGO_SERVER_LOG_DIR}"
chmod g+s "${PROJECT_DIR}"
chmod g+s "${DJANGO_SERVER_LOG_DIR}"

# Install environment as service user
echo "Installing project environment..."
runuser -l "${SERVICE_USER}" /etc/bin/bash ./hosting/server_install_environment.sh
echo "Project environment installed"

# Install nginx config
NGINX_CONFIG_LINK_PATH="${NGINX_CONFIG_DIR}/${PROJECT_DIR_NAME}.conf"
if [ ! -L "${NGINX_CONFIG_LINK_PATH}" ]; then
  ln -s "${PROJECT_NGINX_CONFIG_PATH}" "${NGINX_CONFIG_LINK_PATH}"
fi
nginx -t -c "${NGINX_CONFIG_LINK_PATH}"
nginx -s HUP

# Install systemd service
SYSTEMD_SERVICE_LINK_PATH="${SYSTEMD_INSTALL_DIR}/${SYSTEMD_SERVICE_NAME}"
if [ ! -L "${SYSTEMD_SERVICE_LINK_PATH}" ]; then
  ln -s "${PROJECT_SYSTEMD_SERVICE_PATH}" "${SYSTEMD_SERVICE_LINK_PATH}"
fi
systemd-analyze verify "${SYSTEMD_SERVICE_LINK_PATH}"
systemctl daemon-reload
systemcll start "${SYSTEMD_SERVICE_NAME}"
systemctl enable "${SYSTEMD_SERVICE_NAME}"

echo "System components installed and server running"
cd "${ORIGINAL_WORKING_DIR}" || exit 1
