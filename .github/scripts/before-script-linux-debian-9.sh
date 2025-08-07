#!/bin/sh

echo "Installing libclang for Debian 9..."

cat > /etc/apt/sources.list <<EOF
deb http://archive.debian.org/debian stretch main
EOF

/usr/bin/apt update
/usr/bin/apt install -y clang libclang-dev

# Install 32-bit multilib toolchain for 32-bit builds
/usr/bin/apt install -y gcc-multilib g++-multilib libc6-dev-i386

export LIBCLANG_PATH=/usr/lib/llvm-14/lib
echo "LIBCLANG_PATH=$LIBCLANG_PATH"
