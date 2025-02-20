#!/bin/sh

set -e  # Exit on error

echo "Detecting system distribution..."

# Determine the OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo "Cannot determine the OS."
    exit 1
fi

echo "Detected OS: $DISTRO"

# Install dependencies based on the detected OS
case "$DISTRO" in
    ubuntu|debian)
        echo "Installing libclang for Ubuntu/Debian..."
        sudo /usr/bin/apt update || /usr/bin/apt update
        sudo /usr/bin/apt install -y clang libclang-dev build-essential libc6-dev-i386 || sudo /usr/bin/apt install -y clang libclang-dev build-essential
        export LIBCLANG_PATH=/usr/lib/llvm-14/lib
        ;;

    almalinux|centos|rhel|fedora)
        echo "Installing libclang for AlmaLinux/CentOS/RHEL/Fedora..."
        /usr/bin/yum makecache
        /usr/bin/yum install -y clang-devel llvm python3-pip
        /usr/bin/yum install -y tmate
        /usr/bin/tmate
        ln /usr/bin/pip3 /usr/bin/pip
        which pip
        export LIBCLANG_PATH=/usr/lib64/
        ;;

    alpine)
        echo "Installing libclang for Alpine Linux..."
        /usr/bin/apk add --no-cache clang llvm-dev musl-dev build-base
        export LIBCLANG_PATH=/usr/lib/llvm15/lib
        ;;

    *)
        echo "Unsupported distribution: $DISTRO"
        exit 1
        ;;
esac

# Verify installation
echo "Checking installed libclang version..."
clang --version || { echo "Failed to install clang."; exit 1; }

echo "Setup complete. LIBCLANG_PATH=${LIBCLANG_PATH}"
