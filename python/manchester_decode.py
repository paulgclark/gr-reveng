#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 Paul Clark.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import pmt
import array
import numpy
from gnuradio import gr
from . import bit_utilities as bu


# converts a manchester encoded bit list to a decoded bit list
def manch_bit_decoder(encoded_bits, invert):
    i = 1
    decoded_bits = []

    while i < len(encoded_bits):
        # check that encoding is intact; paired bits cannot be the same
        if encoded_bits[i] == encoded_bits[i-1]:
            print("Manchester decode fail: fallen out of sync")
            print("                        next payload is invalid")
            return (decoded_bits)

        # now just take the second bit of the pair (assuming IEEE 802.3)
        if not invert:
            decoded_bits.append(encoded_bits[i])
        else:
            decoded_bits.append(encoded_bits[i-1])
        i = i + 2 # move to next pair
    return decoded_bits


class manchester_decode(gr.basic_block):
    """
    This block operates on input PDUs containing Manchester-encoded
    bits (unsigned char values equal only to 0 or 1). It outputs a
    Manchester-decoded PDU. There is only one property, which
    allows you to select whether the block decodes per standard
    (IEEE 802.3) Manchester or inverted Manchester. The standard encoding
    maps a one to a rising edge (01) and a zero to a falling edge (10).

    This block assumes you have assembled your encoded data with the
    proper alignment (such as using a "Correlate Access Code - Tag Stream"
    block followed by "Repack Bits" and "Tagged Stream to PDU").
    """
    def __init__(self, invert = False):
        gr.basic_block.__init__(self,
            name="manchester_decode",
            in_sig=None,
            out_sig=None)

        self.invert = invert
        # did not end up using the code below, but will employ for PWM
        if (invert):
            self.zero_seq = (0, 1)
            self.one_seq =  (1, 0)
        else:
            self.zero_seq = (1, 0)
            self.one_seq =  (0, 1)

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    # runs each time a msg pdu arrives at the block input
    # it converts the input PDU bytes to half as many output PDU bytes
    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("ERROR: Invalid data type: Expected u8vector.")
            return

        encoded_data = list(pmt.u8vector_elements(msg))

        # convert bytes to a single list of bits
        bit_list = bu.byte_list_to_bits(encoded_data)
        decoded_bits = manch_bit_decoder(bit_list, self.invert)
        decoded_bytes = bu.bit_list_to_byte_list(decoded_bits)

        # send out the decoded PDU
        self.message_port_pub(
                pmt.intern('out'), 
                pmt.cons(pmt.PMT_NIL, 
                    pmt.init_u8vector(len(decoded_bytes), decoded_bytes)))

