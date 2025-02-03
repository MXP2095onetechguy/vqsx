#!/bin/sh

PY3EXEC="/usr/bin/env python3";

$PY3EXEC testpacker.py -s -t testpacker.vBin;
printf '\n';
$PY3EXEC testrunner.py testpacker.vBin -s;