# Copyright 2011 Free Software Foundation, Inc.
#
# This file was generated by gr_modtool, a tool from the GNU Radio framework
# This file is a part of gr-reveng
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Include python install macros
########################################################################
include(GrPython)
if(NOT PYTHONINTERP_FOUND)
    return()
endif()

add_subdirectory(bindings)

########################################################################
# Install python sources
########################################################################
GR_PYTHON_INSTALL(
    FILES
    __init__.py
    bit_utilities.py
    manchester_decode.py
    pwm_decode.py
    message_print.py
    DESTINATION ${GR_PYTHON_DIR}/reveng
)

########################################################################
# Handle the unit tests
########################################################################
include(GrTest)

set(GR_TEST_TARGET_DEPS gnuradio-reveng)
GR_ADD_TEST(qa_correlate_access_code_bb_ts_fl ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_correlate_access_code_bb_ts_fl.py)
GR_ADD_TEST(qa_manchester_decode ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_manchester_decode.py)
GR_ADD_TEST(qa_pwm_decode ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_pwm_decode.py)
GR_ADD_TEST(qa_message_print ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_message_print.py)
