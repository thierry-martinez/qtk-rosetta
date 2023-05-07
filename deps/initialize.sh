#!/bin/sh
set -ex
git submodule update --init
DEPS_DIR="$PWD"
BUILD_DIR=_build
(
    QUEST_BUILD_DIR="$BUILD_DIR/QuEST"
    mkdir -p "$QUEST_BUILD_DIR"
    cd "$QUEST_BUILD_DIR"
    cmake "$DEPS_DIR/QuEST"
    make
)
(
    CHECK_BUILD_DIR="$BUILD_DIR/check"
    mkdir -p "$CHECK_BUILD_DIR"
    cd "$CHECK_BUILD_DIR"
    autoreconf -ivf "$DEPS_DIR/check"
    $DEPS_DIR/check/configure
    make
    cd $DEPS_DIR/check
    git clean -dfx
)
