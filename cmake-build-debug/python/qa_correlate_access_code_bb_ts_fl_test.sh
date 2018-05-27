#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/paul/code/gr-reveng/python
export PATH=/home/paul/code/gr-reveng/cmake-build-debug/python:$PATH
export LD_LIBRARY_PATH=/home/paul/code/gr-reveng/cmake-build-debug/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/home/paul/code/gr-reveng/cmake-build-debug/swig:$PYTHONPATH
/usr/bin/python2 /home/paul/code/gr-reveng/python/qa_correlate_access_code_bb_ts_fl.py 
