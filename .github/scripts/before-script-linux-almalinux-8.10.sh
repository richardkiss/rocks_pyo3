#!/bin/sh

echo 'Alma linux'

/usr/bin/yum install -y clang-devel

/usr/bin/yum install -y python3-pip
ln -s /usr/bin/pip3 /usr/bin/pip
