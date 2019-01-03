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

##########
# The following functions are used to convert lists of bits to lists of
# bytes (and vice-versa). The primary OOT block code follows these
# functions.


# returns a bit list of the specified length, corresponding to
# the integer value passed; the input integer must be greater than
# or equal to zero and less than 2**(len)
def int_to_padded_bits(int_val, num_bits):
    # make sure the input value is an int
    val = int(int_val)
    if val.bit_length() > num_bits:
        print "WARNING: decToBits() passed too few bits ({}) to render integer: {}".format(num_bits, val),
        return [0]
    # build minimum bit count equivalent
    bits = [int(digit) for digit in bin(val)[2:]]
    # now pad the front end with zeros as needed
    pad_count = num_bits - len(bits)
    bits = pad_count*[0] + bits
    return bits


# returns a list of bits corresponding to an input list of bytes
def byte_list_to_bits(byte_list):
    bit_list = []
    for byte in byte_list:
        bit_list += int_to_padded_bits(byte, 8)
    return bit_list


# returns the integer value of the binary value represented by
# the bit list; by default, the function assumes MSB, in which
# the item at index 0 is the most significant bit. You can choose
# an LSB conversion by setting reverse to True. You can also
# invert the bits before the conversion
def bits_to_int(bit_list, invert = False, reverse = False):
    # invert bits if necessary
    bit_list2 = []
    if invert:
        for bit in bit_list:
            if bit == 0:
                bit_list2.append(1)
            else:
                bit_list2.append(0)
    else:
        bit_list2 = bit_list[:]

    # reverse bits if necessary
    if reverse:
        bit_list3 = reversed(bit_list2)
    else:
        bit_list3 = bit_list2[:]

    value = 0
    for bit in bit_list3:
        if isinstance(bit, int):
            value = (value << 1) | bit
        else:
            # if we don't have an integer, then we ended up with a
            # logic error at some point
            value = -1
            break
    return int(value)


# converts list of input bits to a list of bytes
def bit_list_to_byte_list(bits):
    if len(bits) % 8 != 0:
        print "WARNING: incomplete byte detected in input to bit_list_to_byte_list"
        print "         len = " + str(len(bits))
    byte_list = []
    for i in xrange(0, len(bits), 8):
        bits_in_byte = bits[i:i+8]
        byte = bits_to_int(bits_in_byte)
        byte_list.append(byte)
    return byte_list


# converts a manchester encoded bit list to a decoded bit list
def manch_bit_decoder(encoded_bits, invert):
    i = 1
    decoded_bits = []

    while i < len(encoded_bits):
        # check that encoding is intact; paired bits cannot be the same
        if encoded_bits[i] == encoded_bits[i-1]:
            print "Manchester decode fail: fallen out of sync"
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
            print "ERROR: Invalid data type: Expected u8vector."
            return

        encoded_data = list(pmt.u8vector_elements(msg))

        # convert bytes to a single list of bits
        bit_list = byte_list_to_bits(encoded_data)
        decoded_bits = manch_bit_decoder(bit_list, self.invert)
        decoded_bytes = bit_list_to_byte_list(decoded_bits)

        # send out the decoded PDU
        self.message_port_pub(
                pmt.intern('out'), 
                pmt.cons(pmt.PMT_NIL, 
                    pmt.init_u8vector(len(decoded_bytes), decoded_bytes)))

