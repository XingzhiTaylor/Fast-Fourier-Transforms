#!/usr/bin/env python
from math import log, ceil, floor

def reverse(b, n):
    bits = log(n,2);
    b = (b & 0xFFFF0000) >> 16 | (b & 0x0000FFFF) << 16
    b = (b & 0xFF00FF00) >> 8 | (b & 0x00FF00FF) << 8
    b = (b & 0xF0F0F0F0) >> 4 | (b & 0x0F0F0F0F) << 4
    b = (b & 0xCCCCCCCC) >> 2 | (b & 0x33333333) << 2
    b = (b & 0xAAAAAAAA) >> 1 | (b & 0x55555555) << 1
    b = b >> (32-int(bits))
    if b < 0:
        largest = 2**bits
        b = b + largest
    return b;

def fft(data,is_reversed):
    data_size = len(data)
    if data_size > 2:
        len_base_two = log(data_size,2)
        if len_base_two == floor(len_base_two):
            length = data_size
        else:
            length = int(2**(ceil(len_base_two)))
        extended_data = data + [0] * (length-data_size)
        #If the length is not a power of 2, extend the data with 0
        if(not is_reversed):
            tmp = [0] * length
            for n in range(length):
                m = reverse(n,length)
                tmp[m] = extended_data[n]
            extended_data = tmp
        #The data list should be bit-reversed. 
        #The bit-reverse happens only once at the first recursion. So the flag is set to false after the reverse
        left = extended_data[0:length/2]
        right = extended_data[length/2:length]     
        left_result = fft(left,True)
        right_result = fft(right,True)
        #Calculate the DFT of the left and right half of the data, respectively
        for k in range(length/2):
            right_result[k] = right_result[k] * e**(-2*pi*1j*k/length)
            extended_data[k] = left_result[k] + right_result[k]
            extended_data[k+length/2] = left_result[k] - right_result[k]
        return extended_data
        #Merge the data by multiplying with the exponential term and add
    elif data_size == 2:
        result = []
        result.append(data[0]+data[1])
        result.append(data[0]-data[1])
        return result
        #If the length of the data is 2, directly calculate the DFT
    else:
        return data
        #The DFT of a single sample is itself

signal = []
infile = open('signal.txt','r')
for line in infile:
    l = line.replace('i', 'j').split()
    if l: 
        sample = [complex(num) for num in l]
        signal = signal + sample
infile.close()
#Read data from a file called signal.txt

spectrum = fft(signal,False)

outfile = open('output.txt','w')
for frequency in spectrum:
    outfile.write(str(frequency.real) + '+' + str(frequency.imag) + '*j  ')
outfile.close()
#Write the results to a file called output.txt
