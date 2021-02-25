from tkinter import *
import random
import os
from os import path
import sys
import pickle

class GUI:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Kawthi Dictionary");
        self.tk.attributes('-zoomed', False)  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.
        self.frame = Frame(self.tk)
        self.frame.grid()
        self.enter_english_label=Label(self.tk, text="Enter English Word", font="none 12 bold")
        self.enter_english_label.grid(row=1,column=0, sticky=W)
        self.english_input = Entry(self.tk, width=50, bg="white")
        self.english_input.grid(row=2, column=0, sticky=W)
        self.enter_kawthi_label=Label(self.tk, text="Enter Kawthi Word", font="none 12 bold")
        self.enter_kawthi_label.grid(row=3,column=0, sticky=W)
        self.kawthi_input = Entry(self.tk, width=25, bg="white", font ="Kawthi 20")
        self.kawthi_input.grid(row=4, column=0, sticky=W)
        self.ipa_pron_label=Label(self.tk, text="IPA Pronunciation", font="none 12 bold")
        self.ipa_pron_label.grid(row=3,column=0, sticky=E)
        self.ipa_display = Entry(self.tk, width=25, bg="white")
        self.ipa_display.grid(row=4, column=0, sticky=E)
        self.enter_literal_label=Label(self.tk, text="Enter Literal Meaning", font="none 12 bold")
        self.enter_literal_label.grid(row=5,column=0, sticky=W)
        self.meaning_input = Entry(self.tk, width=50, bg="white")
        self.meaning_input.grid(row=6, column=0, sticky=W)
        self.button1 = Button(self.tk, text="SUBMIT", width=6, command=self.click)
        self.button1.grid(row=7, column=0, sticky=W)
        self.tk.bind("<Return>", lambda event: self.button1.invoke())
        self.button2 = Button(self.tk, text="CLEAR", width=6, command=self.clear)
        self.button2.grid(row=7, column=0)
        self.tk.bind("<Control-d>", lambda event: self.button2.invoke())
        self.delete_button=Button(self.tk, text="DELETE", width=6, command=self.delete)
        self.delete_button.grid(row=7, column=0, sticky=E)
        self.export_button=Button(self.tk, text="Export", width=6, command=self.export)
        self.export_button.grid(row=11, column=0, sticky=W)
        self.output = Text(self.tk, width=82, height=1, wrap=WORD, background="white")
        self.output.grid(row=8, column=0, columnspan=2, sticky=W)
        self.dictionary_label=Label(self.tk, text="Dictionary", font="none 12 bold")
        self.dictionary_label.grid(row=9,column=0, sticky=W)
        self.dict_output = Text(self.tk, width=82, height=10, wrap=WORD, background="white")
        self.dict_output.grid(row=10, column=0, columnspan=2, sticky=W)
        self.info_label=Label(self.tk, text="ctrl + d clears fields, SUBMIT or ENTER looks up a word if only one box is filled otherwise a new entry is made.", font="none 9")
        self.info_label.grid(row=12,column=0, sticky=W)
        
        # set up assets (images, sounds, words) folders
        self.game_folder = path.dirname(__file__) #finds the location of the game file
        self.img_folder = path.join(self.game_folder, "img") #finds image folder in game folder
        self.sound_folder = path.join(self.game_folder, "sounds")
        self.words_folder = path.join(self.game_folder, "words")
        
        #loads dictionary as a list of objects
        self.kawthi_dict = list()
        if os.path.exists(path.join(self.game_folder, "kawthi_dictionary.pkl")):
            with open(path.join(self.game_folder, "kawthi_dictionary.pkl"), "rb", -1) as FILE:
                self.kawthi_dict=pickle.load(FILE)
        else:
            with open(path.join(self.game_folder, "kawthi_dictionary.pkl"), "wb", -1) as FILE:
                pickle.dump(self.kawthi_dict, FILE)
        
        #This dictionary maps Kawthi to the IPA
        self.ipa = {'h':'h', 'm':'m', 'f':'f', 'p':'p', 'w':'w', 'v':'v', 'b':'b', 'T':'θ', 'n':'n', 's':'s', 't':'t', 'D':'ð', 'l':'l', 'z':'z', 'd':'d', 'S':'ɬ', 'M':'ɲ', 'C':'ʃ', 'c':'tʃ', 'Z':'ɮ', 'r':'r', 'J':'ʒ', 'j':'dʒ', 'x':'χ', 'N':'ŋ', 'q':'x', 'k':'k', 'R':'ʁ', 'L':'ʟ', 'G':'ɣ', 'g':'g', 'a':'a', 'u':'ʌ', 'i':'ɪ', 'A':'æ', 'e':'ɛ', 'E':'e', 'Y':'i', 'I':'aɪ', 'W':'eɪ', 'Q':'ɒ', 'o':'o', 'O':'ʊ', 'U':'u', 'P':'ɔɪ', 'y':'j'}
    def print_words(self):
        #Outputs word list
        self.dict_output.delete(0.0, END)
        for word in self.kawthi_dict:
            text = "\n" + word.english + ": " + word.kawthi + "\n" + word.meaning + "\n"
            self.dict_output.insert(END, text)
    def delete(self):
        for word in self.kawthi_dict:
            if word.english == self.english_input.get():
                self.kawthi_dict.remove(word)
            elif word.kawthi == self.kawthi_input.get():
                self.kawthi_dict.remove(word)
        self.clear()
    def clear(self):
        self.english_input.delete(0, END)
        self.kawthi_input.delete(0, END)
        self.meaning_input.delete(0, END)
        self.ipa_display.delete(0, END)
        self.english_input.focus() #moves focus back to first field
    def to_ipa(self, word):
        ipa_word = word
        for key in self.ipa:
            ipa_word = ipa_word.replace(key, self.ipa[key])
        return ipa_word
    def export(self):
        with open("kawthi_dictionary.html", "w") as file:
            file.write("<html>")
            file.write("<head>")
            file.write("<title>Kawthi Dictionary</title>")
            file.write("</head>")
            file.write("<body>")
            file.write("<h1>Kawthi Dictionary</h1>")
            for word in self.kawthi_dict:
                file.write('<p><b>' + word.english + ': </b><font face="Kawthi">' + word.kawthi + '</font> [' + self.to_ipa(word.kawthi) + '] ' + word.meaning + '.</p>')
            file.write("</body>")
            file.write("</html>") 
        self.output.delete(0.0, END)
        self.output.insert(END, "Dictionary exported to kawthi_dictionary.html.")
    def click(self):
        self.output.delete(0.0, END) #Clears output box
        #looks up kawthi word if already in dictionary
        if self.kawthi_input.get() == "":
            for word in self.kawthi_dict:
                if word.english == self.english_input.get():
                    if not self.kawthi_input.get() == "":   #seperates definitions by two word marks.
                        self.kawthi_input.insert(END, "  ")
                        self.meaning_input.insert(END, "; ")                    
                    self.kawthi_input.insert(END, word.kawthi)
                    self.meaning_input.insert(END, word.meaning)
            self.print_words()
            if self.kawthi_input.get() == "": #check to see if it found the word in the list
                self.output.insert(END, "Word not found")
        #looks up english word if already in dictionary
        elif self.english_input.get() == "":
            for word in self.kawthi_dict:
                if word.kawthi == self.kawthi_input.get():
                    if not self.english_input.get() == "":   #seperates definitions by commas.
                        self.english_input.insert(END, ", ")
                    self.english_input.insert(END, word.english)
                    if self.meaning_input.get() == "":
                        self.meaning_input.insert(END, word.meaning)
            self.print_words()
        elif self.meaning_input.get() == "":
            self.output.insert(END, "Please Fill out All Required Fields!")
        else:
            word_count = 0
            entries = 0
            for word in self.kawthi_dict:
                word_count += 1
                if word.english == self.english_input.get() and word.kawthi == self.kawthi_input.get():
                    self.output.insert(END, "The word already exists in the dictionary!")
                    entries += 1
                elif word.english == self.english_input.get():
                    self.output.insert(END, "An entry for that english word already exists!")
                elif word.kawthi == self.kawthi_input.get():
                    self.output.insert(END, "An entry for that Kawthi word already exists!")
            #Records words if no matching entries are found
            if word_count == 0 or entries == 0:
                    #Records new word into dictionary word object list 
                    new_word = Word(self.english_input.get(), self.kawthi_input.get(), self.meaning_input.get())
                    self.kawthi_dict.append(new_word)
                    self.clear()
                    text = str(word_count) + " words in dictionary"
                    self.output.insert(END, text)
            self.print_words()
        #sorts aphabetically by english words and saves word list
        self.kawthi_dict.sort(key=lambda x: x.english, reverse=False)
        with open(path.join(self.game_folder, "kawthi_dictionary.pkl"), "wb", -1) as FILE:
            pickle.dump(self.kawthi_dict, FILE)
        #displays the ipa pronunciation for the kawthi word
        self.ipa_display.delete(0, END)
        self.ipa_display.insert(END, self.to_ipa(self.kawthi_input.get()))

class Word():
    def __init__(self, eng, kawthi, desc):
        self.english = eng
        self.kawthi = kawthi
        self.meaning = desc

if __name__ == '__main__':
    w = GUI()
    w.tk.mainloop()
