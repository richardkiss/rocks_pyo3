#!/bin/sh

echo 'Alma linux'

# Install clang and clang-devel for bindgen/libclang
yum install -y clang clang-devel

# Set LIBCLANG_PATH for bindgen
export LIBCLANG_PATH=/usr/lib64

echo "LIBCLANG_PATH=$LIBCLANG_PATH"

#/usr/bin/yum install -y python3-pip
python3 -m ensurepip --upgrade
ln /usr/local/bin/pip3 /usr/local/bin/pip

# Install 32-bit cross-compiler for i686 builds
yum install -y gcc gcc-c++ glibc-devel.i686 libgcc.i686
