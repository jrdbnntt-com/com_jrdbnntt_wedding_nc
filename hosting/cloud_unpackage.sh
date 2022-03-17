#!/bin/bash

########################################################################################################################
# Run this to untar the static cloud directory to the website static cloud directory. Previous cloud dir will be
# fully deleted.
########################################################################################################################
set -e # Stop script if any command fails
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "${SCRIPT_DIR}/server_config_vars.sh"

CLOUD_ARCHIVE_PATH="$1"
if [ -d "${PROJECT_STATIC_CLOUD_DIR}" ]; then
  rm -rf "${PROJECT_STATIC_CLOUD_DIR}"
fi
if [ -L "${PROJECT_STATIC_CLOUD_DIR}" ]; then
  echo "Error: will not overwrite linked cloud dir"
  exit 1
fi
mkdir -p "${PROJECT_STATIC_CLOUD_DIR}"
tar -xvf "${CLOUD_ARCHIVE_PATH}" --directory "${PROJECT_STATIC_CLOUD_DIR}"

