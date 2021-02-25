import random
import os
from os import path
import sys
import pickle
from tkinter import *

#functions

def contains():
    for word in kawthi_dict:
        if kawthi_lookup.get() in word.kawthi:
            print(word.kawthi + "     " + word.english)
            #word.kawthi = word.kawthi.replace('Q', 'e')
    save()

def save():
    #sorts aphabetically by english words and saves word list
    kawthi_dict.sort(key=lambda x: x.english.casefold(), reverse=False)
    with open(path.join(game_folder, "kawthi_dictionary.pkl"), "wb", -1) as FILE:
        pickle.dump(kawthi_dict, FILE)

def display_ipa():
    #displays the ipa pronunciation for the kawthi word
    ipa_display.configure(state="normal")
    ipa_display.insert(END, to_ipa(kawthi_input.get()))
    ipa_display.configure(state="disabled")

def english_search():
    #looks up kawthi word if already in dictionary
    global lang_searched
    global word_searched
    lang_searched = "english"
    word_searched = english_lookup.get()
    output.delete(0.0, END)
    clear()
    for word in kawthi_dict:
        if word.english == word_searched:
            if not kawthi_input.get() == "":   #seperates definitions by two word marks.
                kawthi_input.insert(END, "  ")
                meaning_input.insert(END, "; ")
            kawthi_input.insert(END, word.kawthi)
            meaning_input.insert(END, word.meaning)
    english_input.insert(END, word_searched)
    display_ipa()
    print_words()
                
    if kawthi_input.get() == "": #check to see if it found the word in the list
        output.insert(END, "Word not found! Please add the word.")

def kawthi_search():
    #looks up english word if already in dictionary
    lang_searched = "kawthi"
    word_searched = kawthi_lookup.get()
    output.delete(0.0, END)
    clear()
    for word in kawthi_dict:
        if word.kawthi == word_searched:
            if not english_input.get() == "":   #seperates definitions by commas.
                english_input.insert(END, ", ")
            english_input.insert(END, word.english)
            if meaning_input.get() == "":
                meaning_input.insert(END, word.meaning)
    kawthi_input.insert(END, word_searched)
    display_ipa()
    print_words()

    if english_input.get() == "": #check to see if it found the word in the list
        output.insert(END, "Word not found! Please add the word.")

def to_ipa(word):
    ipa_word = word
    for key in ipa:
        ipa_word = ipa_word.replace(key, ipa[key])          
    return ipa_word
    

def export():
    file = open("kawthi_dictionary.html","w") 
    file.write("<html>")
    file.write("<head>")
    file.write("<title>Kawthi Dictionary</title>")
    file.write("</head>")
    file.write("<body>")
    file.write("<h1>Kawthi Dictionary</h1>")
    for word in kawthi_dict:
        file.write('<p><b>' + word.english + ': </b><font face="Kawthi">' + word.kawthi + '</font> [' + to_ipa(word.kawthi) + '] ' + word.meaning + '.</p>')
    file.write("</body>")
    file.write("</html>") 
    file.close()
    
    output.delete(0.0, END)
    output.insert(END, "Dictionary exported to kawthi_dictionary.html.")

def print_words():
    dict_output.delete(0.0, END)
    #Counts words entries and displays how many there are
    i = 0
    for word in kawthi_dict:
        i += 1
    text = str(i) + " words entries in dictionary. \n"
    dict_output.insert(END, text)   
        
    #Outputs word list
    for word in kawthi_dict:
        text = "\n" + word.english + ": " + word.kawthi + "\n" + word.meaning + "\n"
        dict_output.insert(END, text)

def delete():
    entries_deleted = 0
    for word in kawthi_dict:
        if word.english == english_input.get() and word.kawthi == kawthi_input.get():
            index = kawthi_dict.index(word)
            entries_deleted += 1
    clear() 
    
    if entries_deleted == 0:
        output.insert(END, "Word not found or multiple words entered!")
    else:
        del kawthi_dict[index]
        output.insert(END, "Entry Deleted")
        save()
              

def clear():
    english_lookup.delete(0, END)
    kawthi_lookup.delete(0, END)
    english_input.delete(0, END)
    kawthi_input.delete(0, END)
    meaning_input.delete(0, END)
    ipa_display.configure(state="normal")
    ipa_display.delete(0.0, END)
    ipa_display.configure(state="disabled")

def edit_word():
    output.delete(0.0, END)
    for word in kawthi_dict:
        if " " in kawthi_input.get() or "," in english_input.get():
            output.insert(END, "Invalid format: word entries must only contain one word when editing.")
            return                 
        if lang_searched == "kawthi" and word.kawthi == word_searched:
            word.kawthi = kawthi_input.get()
            word.english = english_input.get()
            word.meaning = meaning_input.get()
            clear()
            output.insert(END, "Word Updated")
            save()
        elif lang_searched == "english" and word.english == word_searched:
            word.kawthi = kawthi_input.get()
            word.english = english_input.get()
            word.meaning = meaning_input.get()
            clear()
            output.insert(END, "Word Updated")
            save()
        
    
    
def add_word():
    output.delete(0.0, END)
    if english_input.get() == "" or kawthi_input.get() == "" or meaning_input.get() == "":
        output.insert(END, "Please Fill out All Required Fields!")
           
    else:
        word_count = 0
        entries = 0
        eng_entries = 0
        kawthi_entries = 0
        for word in kawthi_dict:
            word_count += 1
            if word.english == english_input.get() and word.kawthi == kawthi_input.get():
                output.insert(END, "The word already exists in the dictionary!")
                entries += 1
            elif word.english == english_input.get():
                eng_entries +=1
            elif word.kawthi == kawthi_input.get():
                kawthi_entries += 1
        if entries == 0 and (eng_entries + kawthi_entries) > 0:
            output.insert(END, "An entry for that word already exists! New definition added")            

        #Records words if no matching entries are found
        if word_count == 0 or entries == 0:
            #Records new word into dictionary word object list 
            new_word = Word(english_input.get(), kawthi_input.get(), meaning_input.get())
            kawthi_dict.append(new_word)
            if output.get("1.0",'end-1c') == "":
                text = "Word added."
            else:
                text = ""
            output.insert(END, text)
            save()

            clear()        
            print_words()
    english_input.focus() #moves focus back to first field

class Word():
    def __init__(self, eng, kawthi, desc):
        self.english = eng
        self.kawthi = kawthi
        self.meaning = desc

# set up assets (images, sounds, words) folders
game_folder = path.dirname(__file__) #finds the location of the game file
img_folder = path.join(game_folder, "img") #finds image folder in game folder
sound_folder = path.join(game_folder, "sounds")
words_folder = path.join(game_folder, "words")

#loads dictionary as a list of objects
kawthi_dict = list()
if os.path.exists(path.join(game_folder, "kawthi_dictionary.pkl")):
    with open(path.join(game_folder, "kawthi_dictionary.pkl"), "rb", -1) as FILE:
        kawthi_dict=pickle.load(FILE)
else:
    with open(path.join(game_folder, "kawthi_dictionary.pkl"), "wb", -1) as FILE:
        pickle.dump(kawthi_dict, FILE)

#This dictionary maps Kawthi to the IPA
ipa = {'h':'h', 'm':'m', 'f':'f', 'p':'p', 'w':'w', 'v':'v', 'b':'b', 'T':'θ', 'n':'n', 's':'s', 't':'t', 'D':'ð', 'l':'l', 'z':'z', 'd':'d', 'S':'ʃ', 'M':'ɲ', 'c':'tʃ', 'r':'r', 'J':'ʒ', 'j':'dʒ', 'x':'χ', 'N':'ŋ', 'q':'x', 'k':'k', 'R':'ʁ', 'L':'ʟ', 'G':'ɣ', 'g':'g', 'a':'a', 'u':'ʌ', 'i':'ɪ', 'A':'æ', 'e':'ɛ', 'E':'e', 'Y':'i', 'I':'aɪ', 'W':'eɪ', 'o':'o', 'O':'ʊ', 'U':'u', 'P':'ɔɪ', 'y':'j'}

#MAIN
#global variables
lang_searched = ""
word_searched = ""
window = Tk()
window.title("Kawthi Dictionary")
    

#photo1 = PhotoImage(file="fish.gif")
#Label (window, image=photo1, bg="black") .grid(row=0, column=0, sticky=E)

Label(window, text="English to Kawthi", font="none 12 bold").grid(row=1,column=0, sticky=W)
english_lookup = Entry(window, width=35, bg="white")
english_lookup.grid(row=2, column=0, sticky=W)
eng_button = Button(window, text="LOOKUP", width=6, command=english_search)
eng_button.grid(row=2, column=0)
english_lookup.bind("<Return>", lambda event: eng_button.invoke())

Label(window, text="Kawthi to English", font="none 12 bold").grid(row=3,column=0, sticky=W)
kawthi_lookup = Entry(window, width=11, bg="white", font ="Kawthi 20")
kawthi_lookup.grid(row=4, column=0, sticky=W)
kaw_button = Button(window, text="LOOKUP", width=6, command=kawthi_search)
kaw_button.grid(row=4, column=0)
kawthi_lookup.bind("<Return>", lambda event: kaw_button.invoke())

Label(window, text="English Word", font="none 12 bold").grid(row=5,column=0, sticky=W)
english_input = Entry(window, width=50, bg="white")
english_input.grid(row=6, column=0, sticky=W)

Label(window, text="Kawthi Word", font="none 12 bold").grid(row=7,column=0, sticky=W)
kawthi_input = Entry(window, width=16, bg="white", font ="Kawthi 20")
kawthi_input.grid(row=8, column=0, sticky=W)

Label(window, text="IPA Pronunciation", font="none 12 bold").grid(row=7,column=0, sticky=E)
ipa_display = Text(window, state="disabled", width=20, height=1, bg="white", font="none 14")
ipa_display.grid(row=8, column=0, sticky=E)

Label(window, text="Enter Literal Meaning", font="none 12 bold").grid(row=9,column=0, sticky=W)
meaning_input = Entry(window, width=82, bg="white")
meaning_input.grid(row=10, column=0, sticky=W)


button1 = Button(window, text="ADD WORD", width=10, command=add_word)
button1.grid(row=11, column=0, sticky=W)
meaning_input.bind("<Return>", lambda event: button1.invoke())
button2 = Button(window, text="CLEAR", width=6, command=clear)
button2.grid(row=11, column=0, padx=100, sticky=E)
window.bind("<Control-d>", lambda event: button2.invoke())
Button(window, text="EDIT", width=6, command=edit_word).grid(row=11, column=0)
Button(window, text="DELETE", width=6, command=delete).grid(row=11, column=0, sticky=E)
Button(window, text="Export", width=6, command=export).grid(row=14, column=0, sticky=W)
Button(window, text="Contains", width=6, command=contains).grid(row=14, column=0, sticky=E)

output = Text(window, width=70, height=1, wrap=WORD, background="white")
output.grid(row=12, column=0, columnspan=1, sticky=E)

Label(window, text="Dictionary", font="none 12 bold").grid(row=12,column=0, sticky=W)
dict_output = Text(window, width=82, height=10, wrap=WORD, background="white")
dict_output.grid(row=13, column=0, columnspan=1, sticky=W)

Label(window, text="ctrl + d clears fields, SUBMIT or ENTER looks up a word if only one box is filled otherwise a new entry is made.", font="none 9").grid(row=15,column=0, sticky=W)

window.mainloop()
