#!/bin/bash

########################################################################################################################
# Run this to start the django server. Be sure to run ./server_install.sh first if the server is not installed, any
# dependencies have changed, or if the front-end needs to be re-built.
#
# Ensure process working directory is the directory of this file.
#
# CLI arguments are passed to the python application for parsing there. See com_jrdbnntt_wedding.asgi for details.
########################################################################################################################

# Initialize virtual environment
if [ ! -d "./venv" ]; then
  echo "Python venv not installed!"
  exit 1
fi

source ./venv/bin/activate

echo "Refreshing SendGrid EmailTemplates..."
python3 manage.py refresh_email_templates

echo "Starting Django ASGI application with Daphne..."
python3 -m daphne com_jrdbnntt_wedding.asgi:application "$@"
