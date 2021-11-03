import matplotlib.pyplot as py
from typing import List

"""
Created on Wed Oct 27 16:43:57 2021
Author: Jamison
Integration / Edits: Emerson
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


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def find_rise(ch, t):  # using ch2 for ch give indices of rise (ch1 gives fall)
    start = 0
    end = 0
    dV = ch[0:-1]
    for i in range(1, len(t) - 1, 1):
        dV[i - 1] = (ch[i] - ch[i - 1]) / (t[i] - t[i - 1])
    print('Calculated Derivatives\n')
    i = 0
    d_3 = 0
    d_2 = 0
    d_1 = 0
    while (1):
        if (dV[i] > 0):
            d = 1
        else:
            d = 0
        if (d * d_1 * d_2 * d_3 > 0):  # the last four points have been rising
            print('Found beginning of rise\n')
            start = i - 20
            if start < 0:
                start = 0
            while (1):
                d_3 = d_2
                d_2 = d_1
                d_1 = d
                if (dV[i] == 0):
                    d = 0
                else:
                    d = 1
                if (d_3 * d_2 * d_1 * d == 0):  # the last 4 points have been the same
                    print('Found end of rise\n')
                    end = i + 20
                    if end > len(dV) - 1:
                        end = len(dV) - 1
                    break
                i = i + 1
                if (i > len(dV) - 1):
                    break
            break
        d_3 = d_2
        d_2 = d_1
        d_1 = d
        i = i + 1
        if (i > len(dV) - 1):
            break
    return (start, end)


def plot_data(input_data: List[dict]):
    time = [x['timestamp'] for x in input_data]
    ch1 = [x['ch1_v'] for x in input_data]
    ch2 = [x['ch2_v'] for x in input_data]

    (start, end) = find_rise(ch2, time)  # change to ch1 for fall
    print("start = ", start)
    print("end = ", end)

    py.subplot(211)
    py.plot(time[start:end], ch2[start:end], 'r.', label='canH')
    py.legend(loc='center right')
    py.subplot(212)
    py.plot(time[start:end], ch1[start:end], 'g.', label='canL')
    py.legend(loc='center right')
    py.show()

