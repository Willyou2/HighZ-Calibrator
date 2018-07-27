#This is a calibration for the values from the pol0.scio files
#Every noise.scio and res50.scio is of length 48 and ends with 0, meaning a cycle of res50 and noise ends at the end of each file
#NOTE: TIME START AND STOP AND POL0.scio have 15 or 14 rows instead of 11
#Expected db gain (10 log10(ratio)) = 65
#Don't forget first data point is always crazy

import getGain
import openScio as sc
import os
import numpy
import bz2Decompress as bd
import matplotlib.pyplot as plt

#ASK DR PETERSON HOW HE WANTS THE PROGRAM TO WORK, SINCE THE NUMBER OF FOLDERS DIFFERS!

#This is the folder directory (The root folder (main folder))
direc = 'D:/Documents/Green Bank Stuff'

def init():
	#Decompresses all the pol0.scio.bz2 files for use
	newPath = direc + '/' + 'data_70MHz'
	for folder in os.listdir(newPath):
		if os.path.isdir(newPath + '/' + folder) and folder.isdigit():
			for subfolder in os.listdir(newPath + '/' + folder):
				if os.path.isdir(newPath + '/' + folder + '/' + subfolder):
					print("Decompressing " + newPath + '/' + folder + '/' + subfolder + '/' + 'pol0.scio.bz2 ........', end='')
					if bd.decomp(newPath + '/' + folder + '/' + subfolder + '/' + 'pol0.scio.bz2') != None:
						print('Complete!')
					#print('Failed: Either already decompressed or nonexistent')
def calUI(): 
	init()
	#Navigates to the switch_data
	if os.path.isdir(direc):
		#If there are multiple time folders (unlikely since 15294 will not change for a long time since you'd have to basically pass 100000 seconds)
		timeFolders = []
		timedirec = direc + '/' + 'switch_data'
		for folder in os.listdir(timedirec): #navigates to switch data folder
			if folder.isdigit():
				timeFolders += [folder]
		#print(timeFolders)
		timeFolders.sort()

		#Iterates over every time folder and does a calibration based on the files within each

		resCarryOn, noiseCarryOn, noneCarryOn = [],[],[] #If any of the ends of the time list continues onto the next folder, this will be used

		#Initializes text file for creating huge data set
		finishedData = []

		for folder in timeFolders: #Goes through each large time folder (first 5 digits: aka 15294)
			for subfolder in os.listdir(timedirec + '/' + folder): #Goes through each time folder inside
				print(timedirec + '/' + folder + '/' + subfolder)

				#This is where every action takes place
				res50path = timedirec + '/' + folder + '/' + subfolder + '/' + 'res50.scio' #sets the res50 path
				noisepath = timedirec + '/' + folder + '/' + subfolder + '/' + 'noise.scio' #sets the noise path

				#Converts to readable list
				res50 = getGain.getOffs(sc.scioRead(res50path))
				noise = getGain.getOffs(sc.scioRead(noisepath))


				while(len(res50) > 1 and len(noise) > 1): #For looping through the entire pairs of on and off -> remember to pop each time so you can keep using [0][1] and [1][1]
					#The above statement is applied because the final switch_data folder may have issues in terms of being incomplete

					#Even though the files are on, off, on, off,
					if res50[0][0] == 1:
						resOn, resOff = res50[0][1], res50[1][1]
					else:
						res50.pop(0)

					#index is the index in the list where the noise ends, and the same index (not time) as when res50 turns on again
					if noise[0][0] == 1:
						noiseOn, noiseOff = noise[0][1], noise[1][1]
					else:
						noise.pop(0)

					noneOn = noiseOff
					if len(noise) > 2:
						noneOff = res50[2][1]
					elif len(noise) == 2:
						noneOff = noneOn + 210.09543991088867 #This number is gathered by calculating the difference until the next cycle starts, or when the res50 turns on again - when the noise source turns off
						#It's also fine if this overlaps with the start of the res50, since that data is irrelevant besides the time stamp (which isn't changed), since we are using the midpoint value, and also deleting the noise/res50 data -> This is all done in the creation of the new file
					else: #This does nothing, but if the code were modified in the while loop, it may be of use for debugging
						print("Reached an incident where the time recording is inconsistent") #This would be the case where the length would be 1, meaning something unprecedented happens with the time recording I didn't account for
					#print("res50 length: ", len(res50), ' noise length: ', len(noise))
					res50 = res50[2:]
					noise = noise[2:]
					finishedData += Calibrate(resOn, resOff, noiseOn, noiseOff, noneOn, noneOff, folder)

		#Writes the finished data to a text file called Experimental Data
		expData = open(direc + '/' + 'exData.txt', 'w')
		for i in range(len(finishedData)):
			for j in range(len(finishedData[i])):
				if j == len(finishedData[i]) - 1:
					expData.write(str(finishedData[i][j]))
				else:
					expData.write(str(finishedData[i][j]) + ',') #TypeError: ufunc 'add' did not contain a loop with signature matching types dtype('<U32') dtype('<U32') dtype('<U32') - > possibly due to too large a value?
			if i == len(finishedData)-1:
				break
			else:
				expData.write('\n')


	else:
		print("This is an incorrect path")

#In every switch_data time folder, there is a noise and res50 scio file. In each of those, the res50 always turns on first

def Calibrate(resOn, resOff, noiseOn, noiseOff, noneOn, noneOff, folder): #noneOff and noneOn is the gap between when neither res50 or noise are turned on - data to calibrate. Folder is the 15294 (first 5 digits)
	resCalTime = 0.5*(resOff+resOn) #midpoint when res50 is on
	noiseCalTime = 0.5*(noiseOff+noiseOn) #midpoint when noise is on
	
	#Gets pol0 folders
	pol0direc = direc + "/" + 'data_70MHz' + '/' + folder
	if os.path.isdir(pol0direc):
		polFolders = sorted(os.listdir(pol0direc))

		#Finds closest folder to time for res50
		for i in range(len(polFolders)):
			if resCalTime - int(polFolders[i]) < 0: #Since each folder name is made the instant it's created, if the time is less than the folder name, it could not have happened in that folder
				break
			resIndex = i
			resClosest = resCalTime - int(polFolders[i])

		resTimes = list(numpy.fromfile(pol0direc + '/' + polFolders[resIndex] + '/' + 'time_start.raw')) #gets list of start times for each row for res50

		for i in range(len(polFolders)):
			if noiseCalTime - int(polFolders[i]) < 0:
				break
			noiseIndex = i
			noiseClosest = resCalTime - int(polFolders[i])

		noiseTimes = list(numpy.fromfile(pol0direc + '/' + polFolders[noiseIndex] + '/' + 'time_start.raw')) #gets list of start times for each row for noise

		#Gets row that started closest to midtime of the res50
		for i in range(len(resTimes)):
			if resCalTime - int(resTimes[i]) < 0:
				break
		resTime = int(resTimes[i-1])
		resRow = i-1

		#Now that we have the row of the res50, we can find the measured res50 power. Remember this is constant throughout frequencies, unlike the noise source

		#Gets row that started closest to midtime of the noise source
		for i in range(len(noiseTimes)):
			if noiseCalTime - int(noiseTimes[i]) < 0:
				break
		noiseTime = int(noiseTimes[i-1])
		noiseRow = i-1

		#Now that we have the row for the noise source, we can find the measured noise source power. This should be done for each frequency, since it differs

		#Opens pol0 file with times corresponding to res50 midTime
		resPol = getGain.getOffs(sc.scioRead(pol0direc + '/' + polFolders[resIndex] + '/' + 'pol0.scio'))

		#Opens pol0 file with times corresponding to noise source midTime
		noisePol = getGain.getOffs(sc.scioRead(pol0direc + '/' + polFolders[noiseIndex] + '/' + 'pol0.scio'))

		#Used resPol[0] since it's same in each pol0 file: 4096. 250 is megahertz
		bandwidth = 250*(10**6)/len(resPol[0]) 
		#print(bandwidth)

		############################################################################
		#Creates a list of measured powers in nanoVolts^2 per Hz for each frequency#
		############################################################################

		#Res50
		resList = []
		#for i in range(len(resPol[resRow])):
		#	resList += [resPol[resRow][i]* 6.31 * 10**(-22)]
		for i in range(len(resPol[resRow])):
			resList += [getGain.nVHz(getGain.dBm(resPol[resRow][i]), bandwidth)]
		#The res list isn't actually relatively constant because of the general down-sloping line in the data
		#print(resList[40])
		#Noise
		noiseList = []
		#for i in range(len(noisePol[noiseRow])):
		#	noiseList += [noisePol[noiseRow][i]* 6.31 * 10**(-22)]
		for i in range(len(noisePol[noiseRow])):
			noiseList += [getGain.nVHz(getGain.dBm(noisePol[noiseRow][i]), bandwidth)]
		#print(noisePol)
		polynomial = getGain.getPolynomial() #Gets dbm as a function of frequency
		#NEED TO FIND GAIN NOW

		#res50 noise constant
		resTheory = getGain.nVHz(-174, 1000) #Converts -174 dbm to nV^2/Hz -> Res50 has a bandwidth of 1000 Hz and the noise source is 10000Hz
		#Odd: The value
		#print(resTheory)
		resTheory = [resTheory]*len(resPol[0]) #This is to create a list of the same value and length so it can be easily iterated on

		freqRange = numpy.arange(0, 250*10**6, bandwidth) #Creates frequency range to iterate over

		#print(len(freqRange))
		noiseTheory = list(getGain.nVHz(polynomial(freqRange), 10000)) #Uses the polynomial to convert the numpy array to an array of theoretical noise values for the noise source at each frequency (converted to nV^2/Hz)
		#print(noiseTheory)
		#print(len(resList),len(noiseList),len(noiseTheory), len(resTheory))
		gain = getGain.calcGain(resTheory, noiseTheory, resList, noiseList)
		#print(gain)
		#plt.plot(freqRange, gain)
		#plt.show()
		#scioFiles = [] #This contains all the scio files over which the data should be calibrated as tuples, with the path as the first index, row as second
		
		#Finds folder closest in time to when the data to be calibrated starts
		for i in range(len(polFolders)):
			if noneOn - int(polFolders[i]) < 0: 
				break
			noneOnIndex = i
			noneOnClosest = noneOn - int(polFolders[i])

		noneOnFolder = pol0direc + '/' + polFolders[noneOnIndex] #Folder name for where the noneOn lies
		noneOnTimes = list(numpy.fromfile(pol0direc + '/' + polFolders[noneOnIndex] + '/' + 'time_start.raw'))

		#Finds folder closest in time to when the data to be calibrated stops
		for i in range(len(polFolders)):
			if noneOff - int(polFolders[i]) < 0:
				break
			noneOffIndex = i
			noneOffClosest = noneOn - int(polFolders[i])

		noneOffFolder = pol0direc + '/' + polFolders[noneOffIndex] #Folder name for where the noneOff lies
		noneOffTimes = list(numpy.fromfile(pol0direc + '/' + polFolders[noneOffIndex] + '/' + 'time_start.raw'))

		for i in range(len(noneOnTimes)):
			if noneOn - int(noneOnTimes[i]) < 0:
				break
		noneOnTime = int(noneOnTimes[i-1])
		noneOnRow = i-1 #Row where the data to be calibrated starts

		for i in range(len(noneOffTimes)):
			if noneOn - int(noneOffTimes[i]) < 0:
				break
		noneOffTime = int(noneOffTimes[i-1])
		noneOffRow = i-1 #Row where the data to be calibrated ends

		#Initialize data and time matrices
		calData = []
		calTime = []

		if noneOnFolder == noneOffFolder:
			nonePol = getGain.getOffs(sc.scioRead(noneOnFolder + '/' + 'pol0.scio'))

			###############################
			#Create Time and Data Matrices#
			###############################
			calData += nonePol[noneOnRow:noneOffRow] #Puts in the power data in the range for calibration
			calTime += noneOnTimes[noneOnRow:noneOffRow] #Puts in the time data in the range for calibration
		else:
			noneOnPol = getGain.getOffs(sc.scioRead(noneOnFolder + '/' + 'pol0.scio'))
			noneOffPol = getGain.getOffs(sc.scioRead(noneOffFolder + '/' + 'pol0.scio'))

			###############################
			#Create Time and Data Matrices#
			###############################
			#This method of X: and :Y added together allows the collapse of two separate, but continuous files from 2 folders to combine into 1 chronological data set
			calData += noneOnPol[noneOnRow:]
			calData += noneOffPol[:noneOffRow+1]
			calTime += noneOnTimes[noneOnRow:]
			calTime += noneOffTimes[:noneOffRow+1]

		#The actual calibration of the data we now hold# 
		#print(len(calData))

		#WARNING INCOMPLETE. LENGTH OF CALIBRATION DATA FOR SOME REASON IS QUITE INCONSISTENT
		for i in range(len(calData)):
			for j in range(len(calData[i])):
				calData[i][j] = getGain.nVHz(getGain.dBm(calData[i][j]), bandwidth) #Converts it to nano volts ^2 per hz
				try:
					calData[i][j] = int(calData[i][j]/gain[j])
				except:
					calData[i][j] = 0
			#print(type(calData[i][j]))
		return calData
		#Need to use the gain and create 2 text files (for time and data) for every calibration (put them all together in the end) and name them (for now) in order of the huge encompassing for loop
		#for i in range(len(calData)):
		#print("done")
	else:
		print("Invalid data_70MHz folder!")
	#Gets the time values
	#res50 = 'D:/Documents/Green Bank Stuff/switch_data/15294/1529450971/res50.scio' #This is my path. Input your own here (remember replace \ with /)
	#noise = 'D:/Documents/Green Bank Stuff/switch_data/15294/1529450971/noise.scio'
	#res50 = getGain.getOffs(sc.scioRead(res50))
	#noise = getGain.getOffs(sc.scioRead(noise))

calUI()