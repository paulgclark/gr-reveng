#Overview
This code provides a Reverse Engineering module to gnuradio. It currently consists of a single block.


##Correlate Access Code - Tag Stream - Fixed Length
This is simply a derivative of the Correlate Access Code - Tag Stream block. While the original block reads the 32 bits after the access code (aka preamble) to obtain the frame length, this new block allows you to simply set the frame length in the block properties. This allows the block to be used in situations (like reverse engineering simple protocols) where the frame is not structured with the header expected by the original block.


#Installation:
```
# make sure you have swig installed
sudo apt install swig

# then the usual flow
mkdir build
cd build
cmake ../
make
make install  # may need sudo make install
make ldconfig # may need sudo ldconfig
```

The new block will be at the bottom of the block list under:
"no module specified"-> Reverse Engineering

If you have gnuradio companion running, you'll need to click the "Reload Blocks" button to see the block.
