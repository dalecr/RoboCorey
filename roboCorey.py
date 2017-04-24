'''
	roboCorey.py
	Created by Connor Dale

	This program feeds inputted text to coreySpeaks.py to generate spoken versions of that text.

	03/06/17 

'''
from coreySpeaks import speak
from functools import wraps
from re import sub
from time import time
import wave, struct
from tkinter import*
from PIL import ImageTk,Image
from pygame import mixer

class Interface(Frame):

	def __init__(self, mapping, sounds, master=None):
		self.map = mapping # word --> sound mappings
		self.sounds = sounds # data from sound files

		super().__init__(master)

		master.title("RoboCorey")
		self.grid()

		self.lastSaved = "" # last phrase to be submitted

		# Image for display
		path = "images/robocorey.png"
		self.robot = ImageTk.PhotoImage(Image.open(path))
		self.displayImage = Label(master, image=self.robot)
		self.displayImage.grid(padx=0, pady=0, row=0, column=0, rowspan=50)

		# Textbox for phrase
		Label(text='Enter a word or phrase').grid(padx=10, pady=10, row=6, column=2)
		self.wordBox = Entry(master, width=50)
		self.wordBox.grid(padx=10, pady=10, row=7, column=2)
    
		# Textbox for file name
		Label(text='Enter a file name for saving').grid(padx=10, pady=10, row=10, column=2)
		self.fileBox = Entry(master, width=50)
		self.fileBox.grid(padx=10, pady=10, row=11, column=2)
		
		# Submit button
		subButton = Button(master, bg="White", text="Say it", width=9, height=2, relief=GROOVE,
                    command=self.playSound)
		subButton.grid(row=14, column=2)

		# Play button
		# self.playButton = Button(master, bg="White", text="Play Sound", width=9, height=2, relief=GROOVE,
  #                   command=self.playSound)
		# self.playButton.grid(row=18, column=2)

		# Status Label
		self.statusMessage = StringVar()
		self.statusMessage.set("")
		Label(master,textvariable=self.statusMessage).grid(padx=10, pady=10, row=18, column=2)


	# gets text box inputs and calls coreySpeaks.speak()
	# def makeFile(self):
	# 	# self.playButton.config(state = DISABLED)
	# 	phrase = self.wordBox.get()
	# 	phrase = sub(r'[\.\,\?\;\:\!/]*',r'',phrase)

	# 	fname = self.fileBox.get()
	# 	if fname != "":
	# 		speak(phrase,self.map,self.sounds,fname)
	# 	else:
	# 		speak(phrase,self.map,self.sounds)

	# 	self.statusMessage.set("")
		# self.playButton.config(state = NORMAL)


	# plays file with file name from text box
	def playSound(self):
		phrase = self.wordBox.get()
		phrase = sub(r'[\.\,\?\;\:\!/]*',r'',phrase)
		phrase = phrase.lower()
		self.statusMessage.set("")

		fname = self.fileBox.get()
		if phrase != self.lastSaved:			
			if fname != "":
				speak(phrase,self.map,self.sounds,fname)
			else:
				speak(phrase,self.map,self.sounds)

			self.lastSaved = phrase

		if fname == "":
			fname = "save_files/newFile.wav"
		else:
			fname = "save_files/"+fname+".wav"

		try:
			mixer.init()
			sound = mixer.Sound(fname)
			sound.play()
		except:
			self.statusMessage.set('File Not Found')


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
	    data = struct.unpack("<h", waveData)
	    values.append(int(data[0]))
	
	waveFile.close()

	return (values,length,framerate,compname,comptype)


def corey(words,mapping,sounds):
	t1 = time()
	words = sub(r'[\.\,\?\;\:\!/]*',r'',words) # remove punctuation from input
	coreySpeaks.speak(words,mapping,sounds)
	t2 = time()
	print ("corey took " + str(t2 - t1) + " seconds")


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
	
	for key in soundFileDict.keys():
		curFileName = soundFileDict[key]
		soundDict[key] = getDataFromFile(curFileName)
	
	mapping = getMapping()

	root = Tk()
	win = Interface(mapping,soundDict,master=root)
	win.mainloop()

		
if __name__=='__main__':
	main()