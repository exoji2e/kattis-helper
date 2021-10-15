#!/bin/bash

set -e

function mk_link {
    src=$1
    dst=$2
    if test -f "$dst"; then
        read -p "$dst exists. Do you wish to overwrite it? [y/N]" yn
        case $yn in
            [Yy]* ) 
                rm $dst;;
            * ) return;
        esac
    fi
    ln -s $src $dst
}

python3 -m pip -r requirements.txt

BIN="$HOME/.local/bin"
mkdir -p $BIN

mk_link $(realpath run.py) $BIN/kattis-run
mk_link $(realpath fetcher.py) $BIN/kattis-fetch

echo "Make sure $BIN is on your path!"
