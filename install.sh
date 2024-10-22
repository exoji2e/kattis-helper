#!/bin/bash

set -e

function mk_link {
    src=$1
    dst=$2
    if test -L "$dst" || test -e "$dst"; then
        read -p "$dst exists. Do you wish to overwrite it? [y/N]" yn
        case $yn in
            [Yy]* )
                rm $dst;;
            * ) return;
        esac
    fi
    ln -s $src $dst
}

poetry install

BIN="$HOME/.local/bin"
mkdir -p $BIN

mk_link $(pwd)/kattis-run $BIN/kattis-run
mk_link $(pwd)/kattis-fetch $BIN/kattis-fetch
mk_link $(pwd)/kattis-fetch-problem $BIN/kattis-fetch-problem

echo "Make sure $BIN is on your path!"
