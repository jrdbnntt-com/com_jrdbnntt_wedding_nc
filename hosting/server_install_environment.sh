#!/bin/bash

########################################################################################################################
# Run this to install Python and Node.js environments and build the static front-end.
#
# Ensure the process working directory is the directory of this file.
#
# Dependencies:
# - python3.10 or python3.9 or python3.8, venv, source
# - node, npm
########################################################################################################################
set -e # Stop script if any command fails

ORIGINAL_WORKING_DIR="$(pwd)"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "${SCRIPT_DIR}/server_config_vars.sh"
cd "${PROJECT_DIR}" || exit 1

if [ "$#" -eq 2 ]; then
  NODE_CMD="$1"
  NPM_CMD="$2"
else
  NODE_CMD="node"
  NPM_CMD="npm"
fi

########################################################################################################################
# PYTHON ENVIRONMENT
########################################################################################################################
echo "Installing Python runtime"

# Initialize virtual environment
if [ ! -d "./venv" ]; then
  echo "Initializing new venv..."
  if command -v python3.10 &> /dev/null; then
      python3.10 -m venv "./venv"
  elif command -v python3.9 &> /dev/null; then
      python3.9 -m venv "./venv"
  elif command -v python3.8 &> /dev/null; then
      python3.8 -m venv "./venv"
  else
    echo "Error! Python 3.8+ required"
    exit 1
  fi
  source ./venv/bin/activate
else
  echo "Existing venv found"
  source ./venv/bin/activate
  echo "Updating pip..."
  python3 -m pip install --upgrade pip
  echo "Pip updated"
fi

echo "Installed Python runtime:"
python3 --version
python3 -m pip --version

# Handle dependencies
echo "Installing/updating Python project dependencies..."
python3 -m pip -q install -r "./requirements.txt"

echo "Python environment ready"


########################################################################################################################
# NODE.JS ENVIRONMENT
########################################################################################################################
echo "Using Node.js runtime:"
${NODE_CMD} --version
${NPM_CMD} --version

# Handle dependencies
echo "Installing/updating Node.js package dependencies..."
${NPM_CMD} install

echo "Node.js environment ready."

# Build front-end
echo "Building front-end..."
${NPM_CMD} run build

echo "Server installed and ready to start"
cd "${ORIGINAL_WORKING_DIR}" || exit 1
