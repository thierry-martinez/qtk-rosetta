#!/bin/sh
set -ex
git submodule update --init
(
    cd check
    autoreconf -ivf
    ./configure
    make
)
