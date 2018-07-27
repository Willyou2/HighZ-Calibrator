import openScio as sc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math


#With the gain, since gain is measured via: gain = 10*log10(P_out/P_in), we are only plotting power_out/power_in, so this is a ratio instead of formal gain
#This means that by algebra, u do power measured / gain to get the actual calibrated power
#Thanks to Olga for the getPolynomial code

def getOffs(x): #This converts the arrays to readable lists. This applies to the lists in our program, which are 2 dimensional. If 1 dimensional, remove the for loop
    #x = scioRead('D:/Documents/Green Bank Stuff/switch_data/15294/1529450971/res50.scio')
    x = list(x)
    for i in range(len(x)):
        x[i] = list(x[i])
    return x

def getPolynomial(): #This is more of a function to do an initialization job, since all it does is call the polynomial fit function from already stored data
    noise_data = pd.read_excel('1.xlsx', sheet_name='1')

    noise=noise_data.as_matrix()

    x = noise[50:,0].astype(float)
    y = noise[50:,1].astype(float)

    #V2_noise = 50 * 10**(y/10-9)

    #logx = np.log10(x)
    #y = np.log10(y)
    #logV2_noise = np.log10(V2_noise)

    coefficients = np.polyfit(x, y, 4)
    polynomial = np.poly1d(coefficients)

    #ASK OLGA ABOUT THE POLYNOMIAL BECAUSE I DONT THINK IT CONVERTS Hz TO DBM BUT MAYBE LOG10(HZ)?

    return polynomial 

def nVHz(x, bandwidth): #This takes a dBm value and its bandwidth and converts it to nanovolts squared per Hz)
    watt = 10**((x - 30)/10)
    res = 50 #This is default. If your experiment uses a different resistance, replace the value
    nV2 = (watt*res*10**(18))/bandwidth
    return nV2

def dBm(x): #This takes a computer unit value and converts it to dBm
    return 10*math.log10(x) - 147

def numpydBm(x): #Same but for numpy arrays (I'm not sure if numpy float 64s work the same way as python default values do, so I avoid generally using np.log10)
    return 10*np.log10(x) - 147

def calcGain(x1, x2, y1, y2): #In this case, x1 is the measured res50, y1, is the theoretical res50, x2 is the measured noise source, y2 is the theoretical noise source 
    gain = []
    #Gathers gain per frequency
    for i in range(len(x1)):
        Dx = x2[i]-x1[i]
        Dy = y2[i]-y1[i]
        #print(Dx)
        gain += [Dy/Dx]
    return gain

print(nVHz(-174, 1000)) #0.00398107 is in Watts