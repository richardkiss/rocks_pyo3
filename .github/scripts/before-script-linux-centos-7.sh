#!/bin/sh
set -e

echo "Running before-script for centos-7..."

# Install 32-bit cross-compiler and dependencies for i686 builds
yum install -y gcc gcc-c++ glibc-devel.i686 libgcc.i686

echo "Finished installing i686 cross-compiler dependencies."
