import numpy
import os

def scioRead(path):
	f = open(path)
	ndim = numpy.fromfile(f, 'int32', 1)
	x = int(ndim)
	if (x<0):
		diff=True
		x=-1*x
	else:
		diff=False

	sz = numpy.fromfile(f, 'int32', x)
	mytype=numpy.fromfile(f,'int32',1)
	vec = numpy.fromfile(f, dtype=int2dtype(mytype))
	nmat=vec.size/numpy.product(sz)
	new_sz=numpy.zeros(sz.size+1,dtype='int32')
	new_sz[0]=nmat
	new_sz[1:]=sz


	mat=numpy.reshape(vec,new_sz)
	if diff:
		mat=numpy.cumsum(mat,0)

	return mat

def int2dtype(myint):
    if (myint==8):
        return 'float64'
    if (myint==4):
        return 'float32'
    if (myint==-4):
        return 'int32'
    if (myint==-8):
        return 'int64'
    if (myint==-104):
        return 'uint32'
    if (myint==-108):
        return 'uint64'
'''
y = scioRead('D:/Documents/Green Bank Stuff/switch_data/15294/1529450971/noise.scio')
x = scioRead('D:/Documents/Green Bank Stuff/switch_data/15294/1529450971/res50.scio')
x = list(x)
for i in range(len(x)):
	x[i] = list(x[i])
y = list(y)
for j in range(len(y)):
	y[i] = list(y[i])
print('res50 starts: ', x[0][1], ' to ', x[1][1])
print('noise starts: ', y[0][1], ' to ', y[1][1])
print('res50 starts: ', x[2][1], ' to ', x[3][1])
print('noise starts: ', y[2][1], ' to ', y[3][1])'''

#According to data, res50 turns off and noise turns on, etc

#x = scioRead('D:/Documents/Green Bank Stuff/data_70MHz/15294/1529450985/time_start.raw')
#print((x[0][1]/86400)/365)
#print(179593 - 15101)
#print(325654 - 179593)
#The switch_data reveals alternating 1 and 0. Also, the difference between any consecutive time is alternating around 30 and around 270 aka: x[1][1] - x[0][1] = 30, x[2][1] - x[1][1] = 270 
#Exact diff: 30.164492 and 270.146061 - basically indicates there is a fixed time gap between any two switch data for 50 Ohm resistor - perhaps this is the time gap between when its on and off, since this data records when its on and off (aka 1 and 0)
#Basically after 30.164492 computer unit time, the 50 resistor turns off? Since it becomes 0 state. Then it turns on (or is recorded on) for 270.146061 computer units?
#print(type(x))
#print(len(x))
