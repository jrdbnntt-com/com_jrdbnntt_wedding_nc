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


if [ -z "${RUNTIME_ENVIRONMENT}" ]; then
  RUNTIME_ENVIRONMENT="DEVELOPMENT"
fi
while [ $# -gt 0 ]; do
    case $1 in
    -p|--prod|--production)
      RUNTIME_ENVIRONMENT="PRODUCTION"
      shift 1
      ;;
    -d|--dev|--development)
      RUNTIME_ENVIRONMENT="DEVELOPMENT"
      shift 1
      ;;
    -t|--test)
      RUNTIME_ENVIRONMENT="TEST"
      shift 1
      ;;
    --runtime)
      if [ $# -ge 2 ]; then
        RUNTIME_ENVIRONMENT="$2"
      else
        echo "Error: --runtime param requires a second argument to specify the runtime to use"
        exit 1
      fi
    esac
done
export RUNTIME_ENVIRONMENT
echo "Starting server with RUNTIME_ENVIRONMENT set to '${RUNTIME_ENVIRONMENT}'"

function print_action {
    echo -e "######################################################################################\n$1"
}

print_action "Entering python environment..."
if [ ! -d "./venv" ]; then
  echo "Python venv not installed!"
  exit 1
fi
source "./venv/bin/activate"

print_action "Preforming any necessary database migrations..."
python3 manage.py migrate

print_action "Collecting static files"
if [ -d "${PROJECT_STATIC_ROOT}" ]; then
  rm -rf "${PROJECT_STATIC_ROOT}"
fi
python3 manage.py collectstatic

print_action "Refreshing SendGrid EmailTemplates..."
python3 manage.py refresh_email_templates

print_action "Starting Django ASGI application with Daphne..."
python3 -m daphne -b 0.0.0.0 -p "${DAPHNE_SERVER_PORT}" com_jrdbnntt_wedding.asgi:application "$@"

cd "${ORIGINAL_WORKING_DIR}" || exit 1
