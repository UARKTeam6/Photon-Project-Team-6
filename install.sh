#!/bin/bash
# Shebang line, tells the system to use linux to run this script

set -e  # script completely stops when error, prevents installs from being half-finished

echo "Install Script for Photon Game on Debian Virtual Machine"

# 1) Check for Python 3, if no python version found then print and exit
if ! command -v python3; then
    echo "Error: Python3 not found, please install Python3"
    exit 1
fi

# 2) Check Python version, version 3.6 and higher is standard because f-strings
PYTHON_VERSION=$(python3 -c 'import sys; print("{}.{}".format(sys.version_info.major, sys.version_info.minor))')
REQ_VERSION="3.6"

# used python script to obtain python version, check if that version >=3.6
if [ "$(printf '%s\n' "$REQ_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQ_VERSION" ]; then
    echo "Error: Python version $REQ_VERSION or higher is required. Detected Python version $PYTHON_VERSION"
    exit 1
fi
echo "Python version $PYTHON_VERSION Acceptable."

# 3) Make sure pip installed, if version not found then print and install
if ! python3 -m pip --version; then
    echo "pip for python3 not found, installing python3-pip..."
    #refreshed the debian package list and install pip w/o permission(-y)
    sudo apt-get update -y
    sudo apt-get install -y python3-pip
fi

# 4) Upgrade pip to make sure it can install all python libraries, break sys packages to prevent python from flagging these
python3 -m pip install --upgrade pip --break-system-packages

# 5) Install required Python libraries (tkinter doesnt need pip)
python3 -m pip install pillow psycopg2-binary pygame --break-system-packages
sudo apt-get install -y python3-tk

# 6) Confirm python libraries installed
echo "Installed package versions:"
python3 -m pip show pillow psycopg2-binary pygame | grep Version

echo "=== Setup complete! ==="

