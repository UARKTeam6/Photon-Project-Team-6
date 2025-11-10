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

# Helper function to work around the break-system-packages fixing pip errors for some versions and causing errors on others
pip_install_func()
{
    local args=("$@")
    if python3 -m pip install "${args[@]}" --break-system-packages 2>/dev/null; then
        return 0
    else
        echo "break-system-packages not supported retry without it"
        python3 -m pip install "${args[@]}"
    fi
}



# 4) Upgrade pip to make sure it can install all python libraries, break sys packages to prevent python from flagging these
pip_install_func --upgrade pip 

# 5) Install required Python libraries (tkinter doesnt need pip)
pip_install_func pillow psycopg2-binary pygame "playsound==1.2.2"

# 6) Install System libraries for playsound to work
sudo apt-get update -y
sudo apt-get install -y python3-tk 

# 7) Confirm libraries installed
echo "Installed package versions:"
python3 -m pip show pillow psycopg2-binary pygame playsound | grep Version

echo "=== Setup complete! ==="

