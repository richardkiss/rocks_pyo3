#!/bin/sh

set -e  # Exit on error

echo "Detecting system distribution..."

# Determine the OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID-$VERSION_ID
else
    echo "Cannot determine the OS."
    exit 1
fi

echo "Detected OS: $DISTRO"

. .github/scripts/before-script-linux-${DISTRO}.sh
