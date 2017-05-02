#include<iostream>
#include<complex>
#include<math.h>
#include<ctime>
#include<cstdlib>
#include<fstream>
#define _USE_MATH_DEFINES

using namespace std;

int reverse(int b, int n) {
    //cout << b << endl;
    double bits = log2(n);
    //bits = (int)bits;
    b = (b & 0xFFFF0000) >> 16 | (b & 0x0000FFFF) << 16;
    b = (b & 0xFF00FF00) >> 8 | (b & 0x00FF00FF) << 8;
    b = (b & 0xF0F0F0F0) >> 4 | (b & 0x0F0F0F0F) << 4;
    b = (b & 0xCCCCCCCC) >> 2 | (b & 0x33333333) << 2;
    b = (b & 0xAAAAAAAA) >> 1 | (b & 0x55555555) << 1;
    b >>= (32-(int)bits);
    if(b < 0){
        double largest = pow(2,bits);
        b += (int)largest;
    }
    return b;
}

complex<double>* fft(complex<double> data[], int data_size, bool is_reversed){
    const complex<double> i(0.0,1.0);
    if(data_size > 2){
        double len_base_two = log2((double)data_size);
        int len = (len_base_two == floor(len_base_two)) ? pow(2,(int)len_base_two) : pow(2,(int)len_base_two + 1);
        complex<double>* extended_data = new complex<double>[len];
        if(len_base_two != floor(len_base_two)){         
            for(int k = 0; k < data_size; k++){
                extended_data[k] = data[k];
            }
            for(int j = data_size; j < len; j++){
                extended_data[j] = 0;
            }
        }else{
            for(int k = 0; k < data_size; k++){
                extended_data[k] = data[k];
            }
        }
        //If the length of data isn't a power of 2, we pad 0s at the end of it
        
        if(!is_reversed){
            complex<double> tmp[len];
            
            for(int k = 0; k < len; k++){
                int r = reverse(k,len);
                tmp[r] = extended_data[k];
            }
            
            for(int j = 0; j < len; j++){
                extended_data[j] = tmp[j];
            }
        }
        //Bit-reverse the array index for the time decimation algorithm
        
        complex<double> left[len/2];
        complex<double> right[len/2];
        
        for(int k = 0; k < len/2; k++){
            left[k] = extended_data[k];
        }
        for(int j = 0; j < len/2; j++){
            right[j] = extended_data[j+len/2];
        }
        //Extract the left and right half of the array
        
        complex<double>* left_result = fft(left,len/2,true);
        complex<double>* right_result = fft(right,len/2,true);

        //Do fft for the two halves respectively
        for(int k = 0; k < len/2; k++){
            right_result[k] *= exp(-2*M_PI*i*(double)k/(double)len);
        }
        //Multiply the right half by the W(n,N) term beform summing
        
        for(int k = 0; k < len/2; k++){
            extended_data[k] = left_result[k] + right_result[k];
        }
        for(int k = 0; k < len/2; k++){
            extended_data[k+len/2] = left_result[k] - right_result[k];
        }
        //Evaluate the ft value with the result on shorter arrays
        if(len != data_size){
            complex<double>* result = new complex<double>[data_size];
            for(int j = 0; j < data_size; j++){
                result[j] = extended_data[j];
                
            }
            return result;
        }else{
            
            return extended_data;
        }
        //If we padded 0 to the data, we have to delete them in the output
        
    }else if(data_size == 2){
        complex<double>* result = new complex<double>[2];
        result[0] = data[0] + data[1];
        result[1] = data[0] - data[1];
        //Evaluate the DFT with the conventional method
        return result;
    }else{
        cerr << "Invalid data" << endl;
    }
}

int main(){
    const complex<double> i(0.0,1.0);
    int signal_length;
    cout << "Length please: " << endl;
    cin >> signal_length;
    //cout << signal_length << endl;
    complex<double> signal[signal_length];
    
    double realPart, imagPart; 
    for(int j = 0; j < signal_length; j++){
 	realPart = rand() % 5;
	imagPart = rand() % 5;
        signal[j] = (double)realPart + (double)imagPart * i;
    }

    complex<double>* result;
    result = fft(signal,signal_length,false);

    ofstream input;
    input.open("input.txt");
    for(int m = 0; m < signal_length; m++){
        input << real(signal[m]) << "+" << imag(signal[m]) << "*i" << endl;
    }
    input.close();
    
    ofstream output;
    output.open("output.txt");
    for(int n = 0; n < signal_length; n++){
        output << real(result[n]) << "+" << imag(result[n]) << "*i" << endl;
    }
    output.close();
}
