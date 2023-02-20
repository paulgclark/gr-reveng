#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: v3.9.2.0-95-g02c0d949

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import blocks
from gnuradio import digital
import reveng
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation



from gnuradio import qtgui

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.zero = zero = (1, 0)
        self.one = one = (0, 1)
        self.samp_rate = samp_rate = 32000
        self.preamble = preamble = 8*(0, 1)
        self.manch_payload = manch_payload = one+zero+zero+one  +  zero+zero+one+one  +  one+one+zero+one  +  zero+one+zero+zero
        self.dead_air = dead_air = 50*(0,)

        ##################################################
        # Blocks
        ##################################################
        self.reveng_manchester_decode_0 = reveng.manchester_decode(False)
        self.reveng_correlate_access_code_xx_ts_fl_0 = reveng.correlate_access_code_bb_ts_fl('0101010101010101',
          0, 'packet_len', 4)
        self.blocks_vector_source_x_0 = blocks.vector_source_b(3*(dead_air + preamble + manch_payload), False, 1, [])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, 'packet_len')
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, 8, "packet_len", False, gr.GR_MSB_FIRST)
        self.blocks_message_debug_0_0 = blocks.message_debug(True)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.reveng_manchester_decode_0, 'in'))
        self.msg_connect((self.reveng_manchester_decode_0, 'out'), (self.blocks_message_debug_0_0, 'print_pdu'))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.reveng_correlate_access_code_xx_ts_fl_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.reveng_correlate_access_code_xx_ts_fl_0, 0), (self.blocks_repack_bits_bb_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_zero(self):
        return self.zero

    def set_zero(self, zero):
        self.zero = zero
        self.set_manch_payload(self.one+self.zero+self.zero+self.one  +  self.zero+self.zero+self.one+self.one  +  self.one+self.one+self.zero+self.one  +  self.zero+self.one+self.zero+self.zero)

    def get_one(self):
        return self.one

    def set_one(self, one):
        self.one = one
        self.set_manch_payload(self.one+self.zero+self.zero+self.one  +  self.zero+self.zero+self.one+self.one  +  self.one+self.one+self.zero+self.one  +  self.zero+self.one+self.zero+self.zero)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble
        self.blocks_vector_source_x_0.set_data(3*(self.dead_air + self.preamble + self.manch_payload), [])

    def get_manch_payload(self):
        return self.manch_payload

    def set_manch_payload(self, manch_payload):
        self.manch_payload = manch_payload
        self.blocks_vector_source_x_0.set_data(3*(self.dead_air + self.preamble + self.manch_payload), [])

    def get_dead_air(self):
        return self.dead_air

    def set_dead_air(self, dead_air):
        self.dead_air = dead_air
        self.blocks_vector_source_x_0.set_data(3*(self.dead_air + self.preamble + self.manch_payload), [])




def main(top_block_cls=top_block, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
