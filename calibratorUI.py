#This is a calibration for the values from the pol0.scio files
#Every noise.scio and res50.scio is of length 48 and ends with 0, meaning a cycle of res50 and noise ends at the end of each file
#NOTE: TIME START AND STOP AND POL0.scio have 15 or 14 rows instead of 11

import getGain
import openScio as sc
import os
import numpy

#ASK DR PETERSON HOW HE WANTS THE PROGRAM TO WORK, SINCE THE NUMBER OF FOLDERS DIFFERS!

#This is the folder directory (The root folder (main folder))
direc = 'D:/Documents/Green Bank Stuff'

def calUI(): 

	#Navigates to the switch_data
	if os.isdir(direc):
		#If there are multiple time folders (unlikely since 15294 will not change for a long time since you'd have to basically pass 100000 seconds)
		timeFolders = []
		timedirec = direc + '/' + 'switch_data'
		for folder in os.listdir(timedirec): #navigates to switch data folder
			if folder.isdigit():
				timeFolders += [folder]
		timeFolders = timeFolders.sort()

		#Iterates over every time folder and does a calibration based on the files within each

		resCarryOn, noiseCarryOn, noneCarryOn = [],[],[] #If any of the ends of the time list continues onto the next folder, this will be used


		for folder in timeFolders: #Goes through each large time folder (first 5 digits: aka 15294)
			for subfolder in os.listdir(timedirec + '/' + folder): #Goes through each time folder inside

				#This is where every action takes place
				res50path = timedirec + '/' + folder + '/' + subfolder + '/' + 'res50.scio' #sets the res50 path
				noisepath = timedirec + '/' + folder + '/' + subfolder + '/' + 'noise.scio' #sets the noise path

				#Converts to readable list
				res50 = getGain.getOffs(sc.scioRead(res50path))
				noise = getGain.getOffs(sc.scioRead(noisepath))

				while(len(res50))
				if res50[0][0] == 1:
					resOn, resOff = res50[0][1], res50[1][1]
				else:
					resOn, resOff = res50[1][1], res50[2][1]

				#index is the index in the list where the noise ends, and the same index (not time) as when res50 turns on again
				if noise[0][0] == 1:
					index = 1
					noiseOn, noiseOff = noise[0][1], noise[1][1]
				else:
					index = 2
					noiseOn, noiseOff = noise[1][1], noise[2][1]

				noneOn = noiseOff
				noneOff = res50[index][1]

				Calibrate(resOn, resOff, noiseOn, noiseOff, noneOn, noneOff, folder)
	else:
		print("This is an incorrect path")

#In every switch_data time folder, there is a noise and res50 scio file. In each of those, the res50 always turns on first

def Calibrate(resOn, resOff, noiseOn, noiseOff, noneOn, noneOff, folder): #noneOff and noneOn is the gap between when neither res50 or noise are turned on - data to calibrate. Folder is the 15294 (first 5 digits)
	resCalTime = 0.5*(resOff+resOn) #midpoint when res50 is on
	noiseCalTime = 0.5*(noiseOff+noiseOn) #midpoint when noise is on
	
	#Gets pol0 folders
	pol0direc = direc + "/" + 'data_70MHz' + '/' + folder
	if os.isdir(pol0direc):
		polFolders = sort(os.listdir(pol0direc))

		#Finds closest folder to time for res50
		closest = resCalTime - polFolders[0] #should always be positive, since we constructed the time from the current folder, and 0 is the earliest
		index = 0
		for i in range(len(polFolders)):
			if resCalTime - polFolders[i] < 0:
				break
			index = i
			closest = resCalTime - polFolders[i]

		resTimes = numpy.fromfile(pol0direc + '/' + polFolders[index] + '/' + 'time_start.raw') #gets list of start times for each row for res50

		closest = noiseCalTime - polFolders[0]
		index = 0
		for i in range(len(polFolders)):
			if noiseCalTime - polFolders[i] < 0:
				break
			index = i
			closest = resCalTime - polFolders[i]

		noiseTimes = numpy.fromfile(pol0direc + '/' + polFolders[index] + '/' + 'time_start.raw') #gets list of start times for each row for noise

		#Gets row that started closest to midtime of the res50
		for i in range(len(resTimes)):
			if resCalTime - resTimes[i] < 0:
				break
		resTime = resTimes[i-1]
		resRow = i-1

		#Now that we have the row of the res50, we can find the measured res50 power. Remember this is constant throughout frequencies, unlike the noise source

		#Gets row that started closest to midtime of the noise source
		for i in range(len(noiseTimes)):
			if noiseCalTime - noiseTimes[i] < 0:
				break
		noiseTime = resTimes[i-1]
		noiseRow = i-1

		#Now that we have the row for the noise source, we can find the measured noise source power. This should be done for each frequency, since it differs




		
	else:
		print("Invalid data_70MHz folder!")
	#Gets the time values
	#res50 = 'D:/Documents/Green Bank Stuff/switch_data/15294/1529450971/res50.scio' #This is my path. Input your own here (remember replace \ with /)
	#noise = 'D:/Documents/Green Bank Stuff/switch_data/15294/1529450971/noise.scio'
	#res50 = getGain.getOffs(sc.scioRead(res50))
	#noise = getGain.getOffs(sc.scioRead(noise))


