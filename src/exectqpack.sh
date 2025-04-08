#!/bin/sh

PY3EXEC="/usr/bin/env python3";

$PY3EXEC qpack.py;
printf '\n';
$PY3EXEC turtleren.py -b qpack.vBin -k -j $@; # Fixed path, ask for black and unscrolled/static canvas