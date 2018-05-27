#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/paul/code/gr-reveng/lib
export PATH=/home/paul/code/gr-reveng/cmake-build-debug/lib:$PATH
export LD_LIBRARY_PATH=/home/paul/code/gr-reveng/cmake-build-debug/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$PYTHONPATH
test-reveng 
