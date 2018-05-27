/* -*- c++ -*- */

#define REVENG_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "reveng_swig_doc.i"

%{
#include "reveng/correlate_access_code_bb_ts_fl.h"
%}


%include "reveng/correlate_access_code_bb_ts_fl.h"
GR_SWIG_BLOCK_MAGIC2(reveng, correlate_access_code_bb_ts_fl);
