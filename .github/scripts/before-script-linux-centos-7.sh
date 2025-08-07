#!/bin/sh
set -e

echo "Running before-script for centos-7..."

# Install 32-bit cross-compiler and dependencies for i686 builds
yum install -y gcc gcc-c++ glibc-devel.i686 libgcc.i686

# Install clang and libclang for bindgen
yum install -y clang clang-devel

# Set LIBCLANG_PATH for bindgen
export LIBCLANG_PATH=/usr/lib64
echo "LIBCLANG_PATH=$LIBCLANG_PATH"

echo "Finished installing dependencies."
