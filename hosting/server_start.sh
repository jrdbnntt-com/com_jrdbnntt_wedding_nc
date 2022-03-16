#!/bin/bash

########################################################################################################################
# Run this to start the django server. Be sure to run ./server_install_environment.sh first if the server is not installed, any
# dependencies have changed, or if the front-end needs to be re-built.
#
# Ensure process working directory is the directory of this file.
#
# CLI arguments are passed to the python application for parsing there. See com_jrdbnntt_wedding.asgi for details.
########################################################################################################################
ORIGINAL_WORKING_DIR="$(pwd)"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "${SCRIPT_DIR}/server_config_vars.sh"
cd "${PROJECT_DIR}" || exit 1

function print_action {
    echo -e "######################################################################################\n$1"
}

print_action "Entering python environment..."

# Initialize virtual environment
if [ ! -d "${PROJECT_DIR}/venv" ]; then
  echo "Python venv not installed!"
  exit 1
fi

source "${PROJECT_DIR}/venv/bin/activate"

print_action "Refreshing SendGrid EmailTemplates..."
python3 manage.py refresh_email_templates

print_action "Starting Django ASGI application with Daphne..."
python3 -m daphne -b 0.0.0.0 -p "${DAPHNE_SERVER_PORT}" com_jrdbnntt_wedding.asgi:application "$@"

cd "${ORIGINAL_WORKING_DIR}" || exit 1
