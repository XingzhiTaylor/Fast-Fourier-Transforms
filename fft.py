#!/usr/bin/env python
from math import log
from cmath import *
import numpy as np

def reverse(b, n):
    bits = log(n,2);
    b = (b & 0xFFFF0000) >> 16 | (b & 0x0000FFFF) << 16
    b = (b & 0xFF00FF00) >> 8 | (b & 0x00FF00FF) << 8
    b = (b & 0xF0F0F0F0) >> 4 | (b & 0x0F0F0F0F) << 4
    b = (b & 0xCCCCCCCC) >> 2 | (b & 0x33333333) << 2
    b = (b & 0xAAAAAAAA) >> 1 | (b & 0x55555555) << 1
    b = b >> (32-bits)
    if b < 0:
        largest = 2**bits
        b = b + largest
    return b;

def fft(data,is_reversed):
    data_size = len(data)
    if data_size > 2:
        len_base_two = log(data_size,2)
        if len_base_two == round(len_base_two):
            length = 2**len_base_two
        else:
            length = 2**(len_base_two+1)
        extended_data = data + [0] * (length-data_size)
        
        if(not is_reversed):
            tmp = [0] * length
            for n in range(length):
                m = reverse(n)
                tmp[m] = extended_data[n]
            extended_data = tmp
            
        left = extended_data[0:length/2]
        right = extended_data[length/2:length]
        
        left_result = fft(left,True)
        right_result = fft(right,True)
        
        for k in range(length/2):
            right_result[k] = right_result[k] * e**(-2*pi*1j*k/length)
            extended_data[k] = left_result[k] + right_result[k];
            extended_data[k+length/2] = left_result[k] - right_result[k];
            
        if length == data_size:
            return extended_data
        else:
            return extended_data[0:data_size]
    elif data_size == 2:
        result = []
        result.append(data[0]+data[1])
        result.append(data[0]-data[1])
        return result
    else:
        print "Invalid Data."
        return []

def transform_complex(line):
    return line.replace(b'+ -', b'- ')  

signal = []
infile = open('signal.txt','r')
print "shit"
#for line in infile:
    #print "fuck"
    #l = line.replace('i', 'j').split()
    #if l: 
    #    sample = [complex(num) for num in l]
    #    signal = signal + sample
lines = map(transform_complex, infile)
arr = np.loadtxt(lines, dtype=np.complex128)
infile.close()
            
spectrum = fft(signal,False)

outfile = open('output.txt','w')
for frequency in spectrum:
    outfile.write('%f ' % frequency)
outfile.close() 