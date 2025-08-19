#!/bin/sh

set -e

echo "Running before-script for almalinux-8.10..."

# Enable 32-bit architecture support
dnf install -y glibc-devel.i686 libgcc.i686

# Install C/C++ compilers
dnf install -y gcc gcc-c++

# Install clang and its development libraries
dnf install -y clang clang-devel

# Set LIBCLANG_PATH for bindgen
export LIBCLANG_PATH=/usr/lib64
echo "LIBCLANG_PATH=$LIBCLANG_PATH"

python3 -m ensurepip --upgrade
ln /usr/local/bin/pip3 /usr/local/bin/pip

echo "Finished installing dependencies."
