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
# - nvm
########################################################################################################################
set -e # Stop script if any command fails

ORIGINAL_WORKING_DIR="$(pwd)"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "${SCRIPT_DIR}/server_config_vars.sh"
cd "${PROJECT_DIR}" || exit 1

# Verify project dir
echo "Verifying project dir..."
if [ ! "${PROJECT_DIR}" = "${REQUIRED_REPO_INSTALL_DIR}" ]; then
  echo "Install dir, '${PROJECT_DIR}', does not match the required install dir, '${REQUIRED_REPO_INSTALL_DIR}'"
  exit 1
fi

# Verify config files are valid
test_nginx_config
test_systemd_config

# Build log dir
echo "Building log dir..."
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
echo "Checking service user..."
if id "${SERVICE_USER}" &>/dev/null; then
    echo "Using existing user '${SERVICE_USER}' as the service user"
else
    echo "Creating system user '${SERVICE_USER}'..."
    useradd --system "${SERVICE_USER}"
fi

# Allow service user to access required files
echo "Setting project file permissions..."
chown -R "${SERVICE_USER}:${FILE_OWNERSHIP_GROUP}" "${PROJECT_DIR}"
chown -R "${SERVICE_USER}:${FILE_OWNERSHIP_GROUP}" "${DJANGO_SERVER_LOG_DIR}"
chmod g+s "${PROJECT_DIR}"
chmod g+s "${DJANGO_SERVER_LOG_DIR}"

# Install environment as service user
echo "Installing root-level project environment..."
NODE_RUNTIME=v16
echo "Installing Node.js runtime (${NODE_RUNTIME})..."
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
nvm install ${NODE_RUNTIME}
nvm use ${NODE_RUNTIME}
NODE_INSTALL_DIR=$(dirname "$(dirname "$(which node)")")
chmod -R ugo+r "${NODE_INSTALL_DIR}"
chmod -R u=rwx,go=rx "${NODE_INSTALL_DIR}/bin/*"

echo "Installing user-level project environment..."
runuser -g "${SERVICE_USER}" -u "${SERVICE_USER}" -- /bin/bash ./hosting/server_install_environment.sh
echo "Project environment installed"

# Install nginx config
echo "Installing nginx config..."
NGINX_CONFIG_LINK_PATH="${NGINX_CONFIG_DIR}/${PROJECT_DIR_NAME}.conf"
if [ ! -L "${NGINX_CONFIG_LINK_PATH}" ]; then
  ln -s "${PROJECT_NGINX_CONFIG_PATH}" "${NGINX_CONFIG_LINK_PATH}"
fi
nginx -s HUP

# Install systemd service
echo "Installing systemd config..."
SYSTEMD_SERVICE_LINK_PATH="${SYSTEMD_INSTALL_DIR}/${SYSTEMD_SERVICE_NAME}"
if [ ! -L "${SYSTEMD_SERVICE_LINK_PATH}" ]; then
  ln -s "${PROJECT_SYSTEMD_SERVICE_PATH}" "${SYSTEMD_SERVICE_LINK_PATH}"
fi
systemctl daemon-reload
systemcll start "${SYSTEMD_SERVICE_NAME}"
systemctl enable "${SYSTEMD_SERVICE_NAME}"

echo "System components installed and server running"
cd "${ORIGINAL_WORKING_DIR}" || exit 1
