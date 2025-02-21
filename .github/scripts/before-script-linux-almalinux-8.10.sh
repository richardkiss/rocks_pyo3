#!/bin/sh

echo 'Alma linux'

/usr/bin/yum install -y clang-devel

#/usr/bin/yum install -y python3-pip
python3 -m ensurepip --upgrade
ln /usr/local/bin/pip3 /usr/local/bin/pip

dnf install -y gcc gcc-c++ glibc-devel.i686

dnf install -y tmate

script -q -c "tmate" /dev/null
