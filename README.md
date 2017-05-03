# Fast-Fourier-Transforms
This repository stores the C++ and Python programs that calculate the DFT of signals using a decimation in time algorithm.
If the length of the signal is not a power of 2, the program will extend the signal and calculate teh DFT. i.e. A signal with length 50 will be extended to have length 64. The signals are extended by padding 0 at the end. This program is to be modified to calculate the DFT without extending the signal.
