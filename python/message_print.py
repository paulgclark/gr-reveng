#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Factoria Labs.
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


import numpy
from gnuradio import gr
import sys
import pmt


def break_list(in_list, chunk_size):
    num_full_chunks = int(len(in_list)/chunk_size)
    size_partial_chunk = len(in_list) - num_full_chunks*chunk_size
    ret_list = []

    for i in range(num_full_chunks):
        chunk_list = []
        for j in range(chunk_size):
            chunk_list.append(in_list[i*chunk_size+j])
        ret_list.append(chunk_list)

    # now pick up last chunk if there is one
    chunk_list = []
    for i in range(size_partial_chunk):
        chunk_list.append(in_list[i + num_full_chunks*chunk_size])
    ret_list.append(chunk_list)

    return ret_list


def hex_to_str_leading(val, digits):
    return "{0:0{1}x}".format(val, digits)


def list_to_hex_str(byte_list, index):
    ret_str = ""
    ret_str += hex_to_str_leading(index * 16, 4) + ": "
    for hex_byte in byte_list:
        ret_str += hex_to_str_leading(hex_byte, 2) + " "
    return ret_str


class message_print(gr.basic_block):
    """
    The Message Print block performs a similar function to the Message Debug block, but when
    rendering payloads as ASCII, it traps non-printable characters and prevents gnuradio-companion
    from crashing.
    """
    def __init__(self, display_ascii):
        gr.basic_block.__init__(self,
            name="message_print",
            in_sig=None,
            out_sig=None)
        # grab a copy of the display mode
        self.display_option = display_ascii
        self.payload_count = 0

        self.message_port_register_in(pmt.intern('msg_in'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)

    # runs each time a msg pdu arrives at the block input
    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("ERROR: Invalid data type: Expected u8vector.")
            return

        byte_list = list(pmt.u8vector_elements(msg))
        byte_count = len(byte_list)

        self.payload_count += 1
        sys.stdout.write("Message {}, len={}\n".format(self.payload_count, byte_count))

        # in the clumsy way I pass an enum value, the following hold:
        # 0 - print hex only
        # 1 - print ascii only
        # 2 - print both

        # hex only
        if self.display_option == 0:
            chunk_list = break_list(byte_list, 16)
            for i, chunk in enumerate(chunk_list):
                print(list_to_hex_str(chunk, i))
        # ascii only
        elif self.display_option == 1:
            sys.stdout.write("ASCII: ")
            for hex_byte in byte_list:
                if 32 <= hex_byte <= 126:
                    sys.stdout.write("{}".format(chr(hex_byte)))
                else:
                    sys.stdout.write("{}".format('~'))
            sys.stdout.write("\n")
        # both hex and ascii
        elif self.display_option == 2:
            chunk_list = break_list(byte_list, 16)
            for i, chunk in enumerate(chunk_list):
                # first print ascii
                sys.stdout.write("ASCII:")
                for hex_byte in chunk:
                    if 32 <= hex_byte <= 126:
                        sys.stdout.write(" {:1} ".format(chr(hex_byte)))
                    else:
                        sys.stdout.write("{:2} ".format('~~'))
                sys.stdout.write("\n")
                # now the hex
                sys.stdout.write(hex_to_str_leading(i * 16, 4) + ": ")
                for hex_byte in chunk:
                    sys.stdout.write(hex_to_str_leading(hex_byte, 2) + " ")
                sys.stdout.write("\n")

        sys.stdout.write("\n")
