#!/bin/bash
DIR="$(dirname "$(readlink "$0")")"
python3 $DIR/run.py "$@"
