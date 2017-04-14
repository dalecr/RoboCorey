'''
	roboCorey.py
	Created by Connor Dale

	This program feeds inputted text to coreySpeaks.py to generate spoken versions of that text.

	03/06/17 

'''
# import coreySpeaks,elizaSpeaks
import elizaSpeaks
# from coreySpeaks import speak
from functools import wraps
from re import sub
from time import time
import wave, struct
import coreySpeaks
import coreySpeaks_1


def eliza(words):
	t1 = time()
	elizaSpeaks.speak(words)
	t2 = time()
	print ("eliza took " + str(t2 - t1) + " seconds")


# returns map of words to phonetic spellings
def getMapping():
	wordMapping = {}
	f = open('pronunciationGuide.txt')
	for line in f:
		line = line.split()
		w = line[0]
		symbols = line[1:]
		listOfSymbols = symbols # []
		for i in range(len(symbols)):
			# symbol = re.sub(r'[0-9]','',symbol)
			listOfSymbols[i] = sub(r'[0-9]','',symbols[i]) # .append(symbol)
		wordMapping[w] = listOfSymbols
	f.close()
	return wordMapping


# returns amplitude values from the given .wav file
def getDataFromFile(fileName):
	values = []

	waveFile = wave.open(fileName, 'rb')
	framerate = waveFile.getframerate()
	length = waveFile.getnframes()
	compname = waveFile.getcompname()
	comptype = waveFile.getcomptype()

	for i in range(0,length):
	    waveData = waveFile.readframes(1)
	    #channels.append(waveFile.getnchannels())
	    data = struct.unpack("<h", waveData)
	    values.append(int(data[0]))
	
	waveFile.close()

	return (values,length,framerate,compname,comptype)


def corey(words,mapping,sounds):
	t1 = time()
	words = sub(r'[\.\,\?\;\:\!/]*',r'',words) # remove punctuation from input
	coreySpeaks.speak(words,mapping)
	t2 = time()
	print ("corey took " + str(t2 - t1) + " seconds")

	t1 = time()
	words = sub(r'[\.\,\?\;\:\!/]*',r'',words) # remove punctuation from input
	coreySpeaks_1.speak(words,mapping,sounds)
	t2 = time()
	print ("corey_1 took " + str(t2 - t1) + " seconds")

def main():
	soundFileDict = {'AA':'sounds/o_swan.wav','AE':'sounds/a_bat.wav','AH':'sounds/e_end.wav',
					'AO':'sounds/aw_paw.wav','AW':'sounds/ow_pow.wav','AY':'sounds/i_hi.wav',
					'B':'sounds/b.wav','CH':'sounds/ch.wav','D':'sounds/d.wav','DH':'sounds/th_voiced.wav',
					'EH':'sounds/e_end.wav','ER':'sounds/r_bird.wav','EY':'sounds/a_base.wav','F':'sounds/f.wav',
					'G':'sounds/g.wav','HH':'sounds/h.wav','IH':'sounds/i_it.wav','IY':'sounds/e_bee.wav',
					'JH':'sounds/dg.wav','K':'sounds/k.wav','L':'sounds/l.wav','M':'sounds/m.wav','N':'sounds/n.wav',
					'NG':'sounds/ng.wav','OW':'sounds/o_boat.wav','OY':'sounds/oi_boy.wav','P':'sounds/p.wav',
					'R':'sounds/r.wav','S':'sounds/s.wav','SH':'sounds/sh.wav','T':'sounds/t.wav',
					'TH':'sounds/th_unvoiced.wav','UH':'sounds/uh_would.wav','UW':'sounds/oo_doo.wav','V':'sounds/v.wav',
					'W':'sounds/w.wav','Y':'sounds/y.wav','Z':'sounds/z.wav','ZH':'sounds/zh_treasure.wav'}
	soundDict = {}
	
	t1 = time()
	for key in soundFileDict.keys():
		curFileName = soundFileDict[key]
		soundDict[key] = getDataFromFile(curFileName)

	mapping = getMapping()
	t2 = time()
	print("loading data took "+str(t2-t1)+" seconds")
	
	words = "hello please tell me about your problems"
	# eliza(words)
	corey(words,mapping,soundDict)
	print('\n')

	words = "it is over anakin i have the high ground"
	# eliza(words)
	corey(words,mapping,soundDict)
	print('\n')

	words = "go ahead mister joestar"
	# eliza(words)
	corey(words,mapping,soundDict)
	print('\n')

	words = "have you ever heard the tragedy of darth plagueis the wise"
	# eliza(words)
	corey(words,mapping,soundDict)
	print('\n')

	words = "alrighty then picture this if you will"
	# eliza(words)
	corey(words,mapping,soundDict)
	print('\n')

	words = "you shall not pass"
	# eliza(words)
	corey(words,mapping,soundDict)



	# coreySpeaks.speak('hello connor')
	# print('Hello Connor')

	# Continues until 'q' is input by the user
	# while(True):
		# response = input(" ==> ")
		# if response == 'q':
			# exit()
		# else:
			# response = re.sub(r'[\.\,\?\;\:\!/]*',r'',words) # remove punctuation from input


			# coreySpeaks.speak(response)

		

# Starts the program
if __name__=='__main__':
	main()