#!/bin/sh

echo "Installing libclang for Debian 9..."

echo "BEFORE"
cat /etc/apt/sources.list
# debian 9 is EOL so we have to tweak the sources.list
sed -i 's/http:\/\/deb.debian.org\/debian/http:\/\/archive.debian.org\/debian/g' /etc/apt/sources.list
sed -i 's/http:\/\/security.debian.org\/debian/http:\/\/archive.debian.org\/debian/g' /etc/apt/sources.list

echo "AFTER"
cat /etc/apt/sources.list

/usr/bin/apt update
/usr/bin/apt install -y clang libclang-dev build-essential libc6-dev-i386
export LIBCLANG_PATH=/usr/lib/llvm-14/lib
echo "LIBCLANG_PATH=$LIBCLANG_PATH"
