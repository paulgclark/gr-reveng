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
def pwm_bit_decoder(encoded_bits, zero_seq, one_seq):
    i = 0
    zlen = len(zero_seq)
    olen = len(one_seq)
    tlen = len(encoded_bits)
    decoded_bits = []

    # step through the encoded bits, matching either a zero or a
    # one sequence; exiting if neither is found
    while i < len(encoded_bits):
        decode_success = False
        # check for a zero
        if (i + zlen) <= tlen:
            if tuple(encoded_bits[i:i+zlen]) == zero_seq:
                decoded_bits.append(0)
                decode_success = True
                i += zlen
        if (i + olen) <= tlen:
            if tuple(encoded_bits[i:i+olen]) == one_seq:
                decoded_bits.append(1)
                decode_success = True
                i += olen

        if not decode_success:
            print("ERROR: Invalid PWM sequence")
            print("       The next payload is invalid")
            break

    return decoded_bits


class pwm_decode(gr.basic_block):
    """
    This block operates on input PDUs containing PWM-encoded
    bits (unsigned char values equal only to 0 or 1). It outputs a
    PWM-decoded PDU. There are two properties, one of which defines
    the PWM sequence for a one bit, and the second which defines the
    zero bit. Both of these sequences are defined with Python tuples.
    For example, a 33% duty cycle starting with zero would be expressed 
    as (0, 0, 1).

    This block assumes you have assembled your encoded data with the
    proper alignment (such as using a "Correlate Access Code - Tag Stream"
    block followed by "Repack Bits" and "Tagged Stream to PDU"). It also
    assumes that you have a waveform sampled at the symbol rate of your 
    encoded signal. Finally, the block assumes that the resulting payload
    contains an integer number of bytes. You can adjust Packet Length
    property of the "Correlate Access Code - Tagged Stream" block to 
    ensure that the decoded payload has a length evenly divisible by 8.

    For more information, see the flowgraph in the examples directory.
    """
    def __init__(self, zero_seq, one_seq):
        gr.basic_block.__init__(self,
            name="pwm_decode",
            in_sig=None,
            out_sig=None)

        # get the sequences
        self.zero_seq = zero_seq
        self.one_seq = one_seq

        # set up the input message port
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        # set up the output message port
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
        decoded_bits = pwm_bit_decoder(bit_list, self.zero_seq, self.one_seq)
        decoded_bytes = bu.bit_list_to_byte_list(decoded_bits)

        # send out the decoded PDU
        self.message_port_pub(
                pmt.intern('out'), 
                pmt.cons(pmt.PMT_NIL, 
                    pmt.init_u8vector(len(decoded_bytes), decoded_bytes)))
