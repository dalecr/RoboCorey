"""
coreySpeaks.py

A modified version of elizaSpeaks.py, created 11/22/15 by Cody Bohlman and Connor Dale. 
Originally used in conjunction with eliza.py to add a speaking component to the therapist's 
verbal responses, this program speaks any text it recieves. 
Uses the melodious voice of Mr. Corey Allred.

elizaSpeaks.py created by Cody Bohlman and Connor Dale

November 22, 2015

coreySpeaks.py created by Connor Dale for improved speed and generalized use

March 6, 2017
"""

import wave, struct
from re import match
import winsound


def smooth(data,phones):
	'''
	smooths transitions between phonemes
	  Inputs: 
	  	data ----------- data from .wav files for all phonemes in the word
	  	phones --------- letters associated with phonemes
	  Outputs:
	  	newData -------- smoothed version of the data
	'''
	newData = []
	SMOOTH_FACTOR = .9
	newLastData = []

	if len(data) > 1:
		for i in range(1,len(data)): #Does the middle smoothing first
			if not (match(r'[bcdfghjklmnpqrstvwxyz]',phones[i][0].lower()) and not match(r'[bcdfghjklmnpqrstvwxyz]',phones[i-1][0].lower())):
				firstLen = len(data[i-1])
				secondLen = len(data[i])

				actualLen = min(firstLen,secondLen)
				firstValueList = [data[i-1][j] for j in range(len(data[i-1][(int(actualLen*SMOOTH_FACTOR)):]))]

				secondValueList = [data[i][j] for j in range(len(data[i][0:(int(actualLen*(1-SMOOTH_FACTOR)))]))]

				curNewData = [(int(firstValueList[j]+secondValueList[j])/2) for j in range(min(len(firstValueList),len(secondValueList)))]

				newFirstData = data[i-1][0:int(actualLen*SMOOTH_FACTOR)]

				newSecondData = data[i][int(actualLen*(1-SMOOTH_FACTOR)):]

				newFirstData += curNewData

				newLastData = newSecondData
				newData.append(newFirstData)

			elif not match(r'[bcdfghjklmnpqrstvwxyz]',phones[i][0].lower()) and not match(r'[bcdfghjklmnpqrstvwxyz]',phones[i-1][0].lower()):
				firstLen = len(data[i-1])
				secondLen = len(data[i])

				actualLen = min(firstLen,secondLen)
				firstValueList = []

				for j in range(len(data[i-1][(int(actualLen*SMOOTH_FACTOR)):])):
					firstValueList.append(data[i-1][j])

				secondValueList = []

				for j in range(len(data[i][0:(int(actualLen*(1-SMOOTH_FACTOR)))])):
					secondValueList.append(data[i][j])

				curNewData = []

				for j in range(min(len(firstValueList),len(secondValueList))):
					curNewData.append(int(firstValueList[j]+secondValueList[j])/2)

				newFirstData = data[i-1][0:int(actualLen*SMOOTH_FACTOR)]

				newSecondData = data[i][int(actualLen*(1-SMOOTH_FACTOR)):]

				for j in range(len(curNewData)):
					newFirstData.append(curNewData[j])

				newLastData = newSecondData
				newData.append(newFirstData)

			elif not match(r'[bcdfghjklmnpqrstvwxyz]',phones[i][0].lower()) and match(r'[bcdfghjklmnpqrstvwxyz]',phones[i-1][0].lower()):
				firstLen = len(data[i-1])
				secondLen = len(data[i])

				actualLen = min(firstLen,secondLen)
				firstValueList = []

				for j in range(len(data[i-1][(int(actualLen*SMOOTH_FACTOR)):])):
					firstValueList.append(data[i-1][j])

				secondValueList = []

				for j in range(len(data[i][0:(int(actualLen*(1-SMOOTH_FACTOR)))])):
					secondValueList.append(data[i][j])

				curNewData = []

				for j in range(min(len(firstValueList),len(secondValueList))):
					curNewData.append(int(firstValueList[j]+secondValueList[j])/2)

				newFirstData = data[i-1][0:int(actualLen*SMOOTH_FACTOR)]

				newSecondData = data[i][int(actualLen*(1-SMOOTH_FACTOR)):]

				for j in range(len(curNewData)):
					newFirstData.append(curNewData[j])

				newLastData = newSecondData
				newData.append(newFirstData)

			else:
				newData.append(data[i-1])
				newLastData = data[i]

		newData.append(newLastData)
		return newData

	else:
		return data


def doGuess(word):
	'''
	Guesses a word's pronunciation if it cannot be found in the pronunciation dictionary
	  Inputs:
	    word ------------- the word to be pronounced
	  Outputs:
	    phones ----------- the word spelled phonetically
	'''
	basicPronunciations = {'a':['AE'],'b':['B'],'c':['K'],'d':['D'],'e':['EH'],'f':['F'],'g':['G'],'h':['HH'],'i':['IH'],
							'j':['JH'],'k':['K'],'l':['L'],'m':['M'],'n':['N'],'o':['OW'],'p':['P'],'qu':['K','W'],'r':['R'],
							's':['S'],'t':['T'],'u':['AH'],'v':['V'],'w':['W'],'x':['K','S'],'y':['Y'],'z':['Z'],'ch':['CH'],
							'sh':['SH'],'th':['TH'],'dg':['JH'],'dge':['JH'],'psy':['S','AY'],'oi':['OY'],'ee':['IY'],
							'ao':['AW'],'ck':['K'],'tt':['T'],'nn':['N'],'ai':['EY'],'eu':['Y','UW'],'ue':['UW'],
							'ie':['IY'],'ei':['IY'],'ea':['IY'],'ght':['T'],'ph':['F'],'gn':['N'],'kn':['N'],'wh':['W'],
							'wr':['R'],'gg':['G'],'ff':['F'],'tt':['T'],'oo':['UW'],'ua':['W','AO'],'ng':['NG'],'bb':['B'],
							'tch':['CH'],'rr':['R'],'dd':['D'],'cc':['K','S'],'wr':['R'],'oe':['OW'],'igh':['AY'],'eigh':'EY'}
	phones = []

	progress = len(word)-1
	while progress >= 0:
		if word[0:3] in basicPronunciations.keys():
			for phone in basicPronunciations[word[0:3]]:
				phones.append(phone)
			word = word[3:]
			progress -= 3
		elif word[0:2] in basicPronunciations.keys():
			for phone in basicPronunciations[word[0:2]]:
				phones.append(phone)			
			word = word[2:]
			progress -= 2
		elif word[0] in basicPronunciations.keys():
			for phone in basicPronunciations[word[0]]:
				phones.append(phone)
			word = word[1:]
			progress -= 1
		else:
			# speak(['I','cant','say','that'])
			return ['AY','K','AE','N','T','S','EY','TH','AE','T']
	return phones


def speak(words,wordMapping,soundMap,fname="newFile"):
	'''
	creates a .wav file of the "spoken" version of a word/phrase, then plays the file
	  Inputs:
	    words ------------- phrase to be "spoken"
	    wordMapping ------- dictionary of phonetic pronunciations of words
	    soundMap ---------- dictionary of phonetic alphabet units to actual sound data
	    fname ------------- name for the new .wav file
	  Outputs:
	    NONE
	'''
	nchannels = 1
	sampwidth = 2
	framerate = 0
	frate = 0
	nframes = 0
	comptype = "NONE"
	compname = "not compressed"

	allData = []
	masterMapping = []

	for word in words.split():
		mapping = []

		if word.upper() in wordMapping.keys():
			mapping = wordMapping[word.upper()]

		else:
			mapping = doGuess(word.lower())
		for thing in mapping:
			masterMapping.append(thing)
			curData,curLen,curFrate,compname,comptype = soundMap[thing]
			nframes += curLen
			allData.append(curData)
			frate = curFrate
	
	framerate = int(frate)
	
	allData = smooth(allData,masterMapping)

	counter = sum(len(data) for data in allData)
	numPauseFrames = int((nframes-counter) / len(words))
	title = "save_files/"+str(fname)+".wav"
	wavFile = wave.open(title,'w')
	wavFile.setparams((nchannels, sampwidth, frate, nframes, comptype, compname))

	pause = [0]*numPauseFrames
	for data in allData:
		data+=pause
		for d in data:
			wavFile.writeframes(struct.pack('<h',int(d)))

	wavFile.close()


