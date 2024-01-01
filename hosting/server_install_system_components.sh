#!/bin/bash

########################################################################################################################
# Run this script to as sudo to create at service user, install the environment as the service user, install the systemd
# service to run the http server with said service user, and configure ngnix.
#
# This expects the repository to be cloned to /var/www/com_jrdbnntt_wedding_nc and will error out if that is not the case.
#
# Dependencies:
# - nginx
# - systemd
# - user group 'www-data'
# - systemd-analyze
# - ssl cert at '/etc/nginx/certs/com_jrdbnntt_wedding_nc/cert.crt' (should be the Cloudflare origin cert)
# - ssl cert key at '/etc/nginx/certs/com_jrdbnntt_wedding_nc/cert.key' (should be the Cloudflare origin cert key)
#  - cloudflare origin pull cert key at '/etc/nginx/certs/cloudflare/authenticated_origin_pull_ca.pem' (https://developers.cloudflare.com/ssl/origin-configuration/authenticated-origin-pull/set-up/#certificate-value)
# - nvm installed at /usr/local/nvm
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
if [ ! -d "${DJANGO_SERVER_LOG_DIR}" ]; then
  mkdir -p "${DJANGO_SERVER_LOG_DIR}"
fi
if [ ! -L "${PROJECT_LOG_DIR}" ]; then
  if [ -d "${PROJECT_LOG_DIR}" ]; then
    mv "${PROJECT_LOG_DIR}/*" "${DJANGO_SERVER_LOG_DIR}"
  fi
  ln -s "${DJANGO_SERVER_LOG_DIR}" "${PROJECT_LOG_DIR}"
fi

# Create service user and a dummy home directory for node
echo "Checking service user..."
if id "${SERVICE_USER}" &>/dev/null; then
    echo "Using existing user '${SERVICE_USER}' as the service user"
else
    echo "Creating system user '${SERVICE_USER}'..."
    useradd --system "${SERVICE_USER}"
fi
SERVICE_USER_HOME="/home/${SERVICE_USER}"
if [ ! -d "${SERVICE_USER_HOME}" ]; then
  echo "Creating dummy home directory '${SERVICE_USER_HOME}' for service user..."
  mkdir -p "${SERVICE_USER_HOME}"
  chown -R "${SERVICE_USER}:${FILE_OWNERSHIP_GROUP}" "${SERVICE_USER_HOME}"
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
if [ ! -d "$NVM_DIR" ]; then
  echo "NVM_DIR does not exist or is not in path"
fi
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
nvm install ${NODE_RUNTIME}
nvm use ${NODE_RUNTIME}
NODE_INSTALL_DIR=$(dirname "$(dirname "$(which node)")")
chmod -R ugo+r "${NODE_INSTALL_DIR}"
chmod -R u=rwx,go=rx "${NODE_INSTALL_DIR}"/bin/*

echo "Installing user-level project environment..."
runuser -g "${SERVICE_USER}" -u "${SERVICE_USER}" -- /bin/bash ./hosting/server_install_environment.sh "$(which node)" "$(which npm)"
echo "Project environment installed"

# Install nginx config
echo "Installing nginx config..."
NGINX_CONFIG_LINK_PATH__AVAILABLE="${NGINX_DIR}/sites-available/${PROJECT_DIR_NAME}.conf"
NGINX_CONFIG_LINK_PATH__ENABLED="${NGINX_DIR}/sites-enabled/${PROJECT_DIR_NAME}.conf"
if [ ! -L "${NGINX_CONFIG_LINK_PATH__AVAILABLE}" ]; then
  ln -s "${PROJECT_NGINX_CONFIG_PATH}" "${NGINX_CONFIG_LINK_PATH__AVAILABLE}"
fi
if [ ! -L "${NGINX_CONFIG_LINK_PATH__ENABLED}" ]; then
  ln -s "${NGINX_CONFIG_LINK_PATH__AVAILABLE}" "${NGINX_CONFIG_LINK_PATH__ENABLED}"
fi
if [ ! -d "${NGINX_DEBUG_LOG_DIR}" ]; then
  mkdirs -p "${NGINX_DEBUG_LOG_DIR}"
fi
nginx -s reload

# Install systemd service
echo "Installing systemd config..."
systemctl enable "${PROJECT_SYSTEMD_SERVICE_PATH}"
systemctl daemon-reload
systemctl start "${SYSTEMD_SERVICE_NAME}"

echo "System components installed and server running"
cd "${ORIGINAL_WORKING_DIR}" || exit 1
