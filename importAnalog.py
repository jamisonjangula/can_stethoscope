# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 16:43:57 2021
Author: Jamison
"""


'''
NOTES:
Haven't tested this on enought input files yet (I would guess it will not 
catch all of the rise/fall times and will miss some)

TO DO's
    1) fit equation to rise/fall
    2) modify script to do this for each rise/fall automatically and produce an 
    average fit for each file/vehicle
'''

import csv
import matplotlib.pyplot as py

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def findRise(ch, t): #using ch2 for ch give indices of rise (ch1 gives fall)
    start = 0
    end = 0
    dV = ch[0:-1]
    for i in range(1,len(t)-1,1):
        dV[i-1] = (ch[i]-ch[i-1])/(t[i]-t[i-1])
    print('Calculated Derivatives\n')
    i = 0
    d_3 = 0
    d_2 = 0
    d_1 = 0
    while(1):
        if (dV[i] > 0):
            d = 1
        else:
            d = 0
        if(d*d_1*d_2*d_3 > 0): # the last four points have been rising
            print('Found beginning of rise\n')
            start = i - 20
            if start < 0:
                start = 0
            while(1):
                d_3 = d_2
                d_2 = d_1
                d_1 = d
                if(dV[i] == 0):
                    d = 0
                else:
                    d = 1
                if(d_3*d_2*d_1*d == 0): # the last 4 points have been the same
                    print('Found end of rise\n')
                    end = i + 20
                    if end > len(dV)-1:
                        end = len(dV)-1
                    break
                i = i+1
                if (i > len(dV)-1):
                    break
            break
        d_3 = d_2
        d_2 = d_1
        d_1 = d
        i = i+1
        if(i > len(dV)-1):
            break
    return (start, end)

def main():
    time = []
    ch1 = []
    ch2 = []
    print("here\n")
    with open('F250.csv', newline='') as csvfile: # this is  the only file i've tested
        data = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in data:
            
            if (isNumber(row[0])):
                time.append(float(row[0]))
                ch1.append(float(row[1]))
                ch2.append(float(row[2]))
            else:
                print(row[0])
    
    (start, end) = findRise(ch2, time) # change to ch1 for fall 
    print("start = ", start)
    print("end = ", end)
    
    py.subplot(211)
    py.plot(time[start:end], ch2[start:end], 'r.', label='canH')
    py.legend(loc='center right')
    py.subplot(212)
    py.plot(time[start:end], ch1[start:end], 'g.', label='canL')
    py.legend(loc='center right')
    py.show()
    
            
main()