import numpy as np
import sys

def beam_gain(pattern, degree):						#pattern = [0x01~0x1F], degree = [0, 360]
    degree = int(degree)
    
    if pattern == 0x0:
        return 0
    
    if pattern > 0x1F or pattern < 0x01:
        sys.exit('Input pattern is out of range')	

    if degree > 360 or degree < 0:
        sys.exit('Input degree is out of range')

    if degree % 2 == 1:
        degree -= 1
	
    filename = './Pattern/'
    for i in range(5):								#Use the power of 2 to do bit-wise check
        bit_check = np.power(2, i)
        if pattern & bit_check:
                filename += str(i+1) + '_'
    filename += 'on.csv'							#Ex. if pattern = 0x1F, then filename = 1_2_3_4_5_on.csv
													#       pattern = 0x04, then filename = 3_on.csv
	#print filename
    with open(filename, 'r') as file:				#According to the result of the bit checking, open corresponding file
        file.readline()								#The first line of the file is useless

        if degree >= 180:							#In order to ease the leverage of simulation, map the degree.
            degree -= 360
    
        target_index = (degree + 180.0)/2			#According to the inpur degree, calculate the corresponding index of the csv file

        for index, line in enumerate(file):			#File processing stuff
            part = line.rstrip('\r\n').split(',')
            if index == target_index:
                return float(part[1])

if __name__ == '__main__':
    print (beam_gain(26, 258.9))
    print (beam_gain(int(0x1a), 258.9))

