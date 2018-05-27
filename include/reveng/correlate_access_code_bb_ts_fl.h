/* -*- c++ -*- */
/*
 * Copyright 2014 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_DIGITAL_CORRELATE_ACCESS_CODE_BB_TS_FL_H
#define INCLUDED_DIGITAL_CORRELATE_ACCESS_CODE_BB_TS_FL_H

#include <gnuradio/digital/api.h>
#include <reveng/api.h>
#include <gnuradio/block.h>
#include <string>

namespace gr {
  namespace reveng {

    /*!
     * \brief Examine input for specified access code, one bit at a time.
     * \ingroup packet_operators_blk
     *
     * \details
     * input:  stream of bits (unpacked bytes)
     * output: a tagged stream set of bits from the payload following
     * the access code.
     *
     * This block searches for the given access code by reading in the
     * input bits. Once found, it uses the packet length property 
     * to capture that many samples in order to set up the the tagged stream 
     * key information. This block is a derivative of the Correlate Access Code -
     * Tagged Stream block with the removal of the header and a fixed frame
     * length.
     *
     * The output of this block is appropriate for use with tagged
     * stream blocks.
     */
    class REVENG_API correlate_access_code_bb_ts_fl : virtual public block
    {
    public:
      // gr::digital::correlate_access_code_bb_ts_fl::sptr
      typedef boost::shared_ptr<correlate_access_code_bb_ts_fl> sptr;

      /*!
       * \param access_code is represented with 1 byte per bit,
       *                    e.g., "010101010111000100"
       * \param threshold maximum number of bits that may be wrong
       * \param tag_name key of the tag inserted into the tag stream
       */
      static sptr make(const std::string &access_code,
		       int threshold,
		       const std::string &tag_name,
                       int len);

      /*!
       * \param access_code is represented with 1 byte per bit,
       *                    e.g., "010101010111000100"
       */
      virtual bool set_access_code(const std::string &access_code) = 0;
      virtual unsigned long long access_code() const = 0;
    };

  } /* namespace digital */
} /* namespace gr */

#endif /* INCLUDED_DIGITAL_CORRELATE_ACCESS_CODE_BB_TS_FL_H */
