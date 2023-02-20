# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT reveng_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT reveng_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND reveng_python_files
    correlate_access_code_bb_ts_fl_python.cc
    python_bindings.cc)

GR_PYBIND_MAKE_OOT(reveng 
   ../..
   gr::reveng
   "${reveng_python_files}")

install(TARGETS reveng_python DESTINATION ${GR_PYTHON_DIR}/reveng COMPONENT pythonapi)
