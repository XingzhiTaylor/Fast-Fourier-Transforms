#!/usr/bin/env python

from math import log, ceil, floor, pi
from cmath import exp

def is_prime(num):
    return all(num%i for i in xrange(2,num))

def fft(signal): 
    N = len(signal)
    if is_prime(N):
        #If the length is prime, calculate the DFT by definition
        result = [0]*N
        for k in range(N):
            for n in range(N):
                result[k] += signal[n]*exp(-2*pi*1j*n*k/N)
        return result      
    else:
        #if the length of the signal is a composite number, extract sublists from the signal and recursively calculate the DFT of each sublist
        p = 2    #Start with the smallest prime 2
        while N % p:
            p += 1   #If p is not a factor of N, try p+1
        else:
            q = N/p   #If p is a factor of N, then q = N/p        
        sub_result = []
        result = [0]*N         #Initialize the list of sub-results and the final result
        for i in range(p):
            sub_result.append(fft(signal[i:N:p]))          #Extract sub-lists from the signal by indexing. Append the DFT of the sub-lists to the sub-result list
        for k in range(N):
            for l in range(p):
                result[k] += sub_result[l][k%q]*exp(-2*pi*1j*l*k/N) 
        return result
        """
        The multiplication of twiddle factors:
        In each level of the recursion there are p sub-results each has length q. To get the kth value in the final result, pick the kth value in the sub-result
        and multiply it with its twiddle factor. The twiddle factor for the lth sub-result is W(lk,N). k is p times larger than the length of the sub-results q.
        Therefore, the k%q-th value in the sub-result is used when k > q.
        """

signal = []
infile = open('test.txt','r')
for line in infile:
    l = line.replace('i', 'j').split()
    if l: 
        sample = [complex(num) for num in l]
        signal = signal + sample
infile.close()
#Read data from a file called signal.txt

spectrum = fft(signal)

outfile = open('output.txt','w')
for frequency in spectrum:
    outfile.write(str(frequency.real) + ' + ' + str(frequency.imag) + '*j  ')
outfile.close()
#Write the results to a file called output.txt