#!/bin/sh

echo "Installing libclang for Ubuntu/Debian..."
/usr/bin/apt update
/usr/bin/apt install -y clang libclang-dev build-essential libc6-dev-i386
export LIBCLANG_PATH=/usr/lib/llvm-14/lib
echo "LIBCLANG_PATH=$LIBCLANG_PATH"
