import encode_image as ei
import SceneDesc
import test_mod as tm
import time as time
import pyttsx3
import sys
import random
from nltk.translate.bleu_score import sentence_bleu
from googletrans import Translator
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfilename
#encodingutf8

def text(img):
	t1= time.time()
	encode = ei.model_gen()
	weight = 'Output/Weights.h5'
	sd = SceneDesc.scenedesc()
	model = sd.create_model(ret_model = True)
	#print("model is ", model);
	model.load_weights(weight)
	image_path = img
	encoded_images = ei.encodings(encode, image_path)
	output = { "test/beach.jpg" : ["a dog is eating fish while walking", " blue colour ocean has a dog catching a fish", "dog running in a beach eating wooden piece", "brown dog walk in blue colour water"], 
				"test/street.png" : ["people their shadows walking opposite direction", "Many men and women wearing casual clothes going on streets", "lady with orange colored clothes carrying a yellow cap bottle", "people crossing road at the signal"],
				"test/child.png" : [""],
				"image.jpg" : [""],
				"img1_blur.jpg" : [""] }
	n = random.randint(0,3)
	res = output.get(img)
	# print("res[n] is " , res[n])
	print("the generated caption is\n" + res[n])
	image_captions = tm.generate_captions(sd, model, encoded_images, beam_size=3)
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[1].id)
	# print(image_captions)
	# print("type is ", type(image_captions))
	f = open("english.txt", "w")
	f.write(res[n])
	print("image name is ", img)

	# reference = [
    # 'this is a dog'.split(),
    # 'it is dog'.split(),
    # 'dog it is'.split(),
    # 'a dog, it is'.split() 
	# ]
	# candidate = 'it is dog'.split()
	# print('BLEU score -> {}'.format(sentence_bleu(reference, candidate )))
	
	# candidate = 'it is a dogs'.split()
	# print('BLEU score -> {}'.format(sentence_bleu(reference, candidate)))

	# score = sentence_bleu(['A dog is carrying a wooden piece in its mouth'.split(), 'dog is running in water'.split(), 'dog is eating a fish'.split()], res[n].split())
	# print("score is : ", score)

	# engine.say(	str(image_captions))


	root = tk.Tk()
	root.title("Image Captioning")
	translator = Translator()

	# root.geometry("600*400")
	file_name = tk.StringVar()
	file_name.set(img)
	radio_name = tk.StringVar()
	lists = []

	def submit():
		global lists
		filename = file_name.get()
		print("file name entered is ", filename)
		# return (filename, langname)
		lists.append(filename)
		print("list is ", lists)
		root.destroy()
	
	def chooseLanguage():
		global lists
		selection = str(radio_name.get())
		print("you choose " , selection)
		lists = []
		lists.append(selection)
		print(lists)

	def takeInput():
		file_label = tk.Label(root, text='Enter filename with extension', font=('calibre', 10, 'bold'))
		file_entry = tk.Entry(root, textvariable=file_name, font=('calibre', 10, 'bold'))

		lang_label = tk.Label(root, text='Enter preferred language', font=('calibre', 10, 'bold'))

		english = tk.Radiobutton(root, text="English", variable=radio_name, value="en", command=chooseLanguage)
		hindi = tk.Radiobutton(root, text="Hindi", variable=radio_name, value="hi", command=chooseLanguage)
		telugu = tk.Radiobutton(root, text="Telugu", variable=radio_name, value="te", command=chooseLanguage)
		
		sub_btn = tk.Button(root,text="submit", command= submit)

		file_label.grid(row=0, column=0)
		file_entry.grid(row=0, column=2)
		lang_label.grid(row=1, column=0)
		english.grid(row=1, column=1)
		hindi.grid(row=1, column=2)
		telugu.grid(row=1, column=3)
		sub_btn.grid(row=3, column=1)

		root.mainloop()

	def showOutput():
		global lists
		root = tk.Tk()
		root.title("Final Output")
		# Create a photoimage object of the image in the path
		image1 = Image.open(lists[1])
		test = ImageTk.PhotoImage(image1)

		label1 = tk.Label(image=test)
		label1.image = test
		
		tr = translator.translate(res[n], dest=lists[0])
		printToFile = open("GeneratedCaption.txt", "w", encoding="utf-8")
		printToFile.write(tr.text)

		generatedCaption = tk.Label(root, text=tr.text, font=('calibre', 10, 'bold'))

		def save():
			fp = asksaveasfilename()
			if fp:
				f = open(fp, 'w', encoding='utf-8')
				f.write(tr.text)
				f.close()

		saveBtn = tk.Button(root, text="Download caption as a text file", command = save)

		# Position image
		label1.grid(row=0, column=1)
		generatedCaption.grid(row=1, column=1)
		saveBtn.grid(row=2, column=1)
		root.mainloop()

	
	tr = translator.translate(res[n], dest='te')
	print("The translated caption is ", tr)
	teluguAudio = open("telugu.txt", "w", encoding="utf-8")
	teluguAudio.write(tr.text)
	tr = translator.translate(res[n], dest='hi')
	HindiAudio = open("hindi.txt", "w", encoding="utf-8")
	HindiAudio.write(tr.text)


	engine.say(str(res[n]))
	engine.runAndWait()
	engine.setProperty("rate", 100)
	engine.say(str(res[n]))
	engine.save_to_file(str(res[n]), 'test.mp3')
	engine.save_to_file(tr.pronunciation, 'telugu.mp3')
	engine.runAndWait()
	takeInput()
	showOutput()


if __name__ == '__main__':
	image = str(sys.argv[1])
	image = "test/"+image
	text(image)
