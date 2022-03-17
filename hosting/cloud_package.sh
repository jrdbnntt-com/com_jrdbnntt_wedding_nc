#!/bin/bash

########################################################################################################################
# Run this to tar the static cloud directory to logs/cloud_copy/static_cloud_copy_<timestamp>.tar.gz so that it can be
# copied to the hosting server.
########################################################################################################################
set -e # Stop script if any command fails

ORIGINAL_WORKING_DIR="$(pwd)"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "${SCRIPT_DIR}/server_config_vars.sh"
cd "${PROJECT_DIR}" || exit 1

CLOUD_ARCHIVE_DIR="${PROJECT_LOG_DIR}/static_cloud_archives"
if [ ! -d "${CLOUD_ARCHIVE_DIR}" ]; then
  mkdir -p "${CLOUD_ARCHIVE_DIR}"
fi

cd "${PROJECT_STATIC_CLOUD_DIR}" || exit 1
ARCHIVE_PATH="${CLOUD_ARCHIVE_DIR}/static_cloud_${FILENAME_DATETIME_NOW_SUFFIX}.tar.gz"
FILES_TO_TAR="$(find -L "." -mindepth 1 '(' -type f -regextype posix-extended -regex '^.*\.(jpg|jpeg|png|ttf|woff|js|css|xml|txt|pdf|json|ico)$' ')' -printf "\"%P\" ")"
echo -n "${FILES_TO_TAR}" | xargs tar -czvf "${ARCHIVE_PATH}"
cd "${PROJECT_DIR}" || exit 1

cd "${ORIGINAL_WORKING_DIR}" || exit 1