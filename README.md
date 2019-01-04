# Overview
This code provides a Reverse Engineering module to gnuradio. It currently consists of two blocks.


## Correlate Access Code - Tag Stream - Fixed Length
This is simply a derivative of the Correlate Access Code - Tag Stream block. While the original block reads the 32 bits after the access code (aka preamble) to obtain the frame length, this new block allows you to simply set the frame length in the block properties. This allows the block to be used in situations (like reverse engineering simple protocols) where the frame is not structured with the header expected by the original block.


## Manchester Decode
This block operates on input PDUs containing Manchester-encoded bits (unsigned char values equal only to 0 or 1). It outputs a Manchester-decoded PDU. There is only one property, which allows you to select whether the block decodes per standard (IEEE 802.3) Manchester or inverted Manchester. The standard encoding maps a one to a rising edge (01) and a zero to a falling edge (10).

This block assumes you have assembled your encoded data with the proper alignment (such as using a "Correlate Access Code - Tag Stream" block followed by "Repack Bits" and "Tagged Stream to PDU"). It also assumes that you have a waveform sampled at the symbol rate of your encoded signal. Finally, the block assumes that the resulting payload contains an integer number of bytes. You can adjust Packet Length property of the "Correlate Access Code - Tagged Stream" block to ensure that the decoded payload has a length evenly divisible by 8.


## PWM Decode
This block operates on input PDUs containing PWM-encoded bits (unsigned char values equal only to 0 or 1). It outputs a PWM-decoded PDU. There are two properties, one of which defines the PWM sequence for a one bit, and the second which defines the zero bit. Both of these sequences are defined with Python tuples.  For example, a 33% duty cycle starting with zero would be expressed as (0, 0, 1).

This block assumes you have assembled your encoded data with the proper alignment (such as using a "Correlate Access Code - Tag Stream" block followed by "Repack Bits" and "Tagged Stream to PDU"). It also assumes that you have a waveform sampled at the symbol rate of your encoded signal. Finally, the block assumes that the resulting payload contains an integer number of bytes. You can adjust Packet Length property of the "Correlate Access Code - Tagged Stream" block to ensure that the decoded payload has a length evenly divisible by 8.


# Installation:
```
# make sure you have swig installed
sudo apt install swig

# then the usual flow
cd gr-reveng
mkdir build
cd build
cmake ../ # or if you have a pybombs install: cmake -DCMAKE_INSTALL_PREFIX=<pybombs target> ../
make
make install  # may need sudo make install
ldconfig      # may need sudo ldconfig
```

The new block will be at the bottom of the block list under:
"no module specified"-> Reverse Engineering

If you have gnuradio companion running, you'll need to click the "Reload Blocks" button to see the new blocks.
