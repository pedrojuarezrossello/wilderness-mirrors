from cProfile import label
import tkinter as tk
from tkinter import BOTH, LEFT, NE, NSEW, NW, TOP, Y, ttk
from tkinter import font
import sys
import os
import shelve
import random

#pedro juarez rosello 15 / 08 /2022

 #preliminary definitions --------------------------------------------------------

db = shelve.open('dictionary') #stores the words
to_learn = shelve.open('tolearn') #words I'm struggling with
i_know = shelve.open('iknow') #words I know
to_learn.update(db) 
db.close()

# -------------------------------------------------------------------------------

def restart_program():
   #restarts the programme so it updates upon adding / deleting an entry
    python = sys.executable
    os.execl(python, python, * sys.argv)

#define a class for entries -----------------------------------------------------

class Entry: 
    def __init__(self,word,definition='',synonym='',example=''):
        self.word = word
        self.definition = definition
        self.synonym = synonym
        self.example = example

#we define the frame where we'll show the entries' data ------------------------------------------------

class WordDef(tk.Frame):
    def __init__(self,master,wrd,definition,synonym='',example=''):
        super().__init__(master,width='334',height='400')
        
        self.word = Entry(wrd,definition,synonym,example)
    
        canvas = tk.Canvas(self,width=500, height=400)
        card_title = canvas.create_text(35, 35, anchor=tk.NW, text=self.word.word, font=("Ariel", 30, "italic"))

        canvas.config(bg='sky blue',highlightthickness=0)
        card_def = canvas.create_text(75, 100, anchor=tk.NW, text='DEFINITION: %s' % self.word.definition, font=("Ariel", 12))
        recdef = canvas.create_rectangle(70,90,425,187)

        if not synonym=='':
            entry_syn = canvas.create_text(75,225, anchor=tk.NW, text='SYNONYMS: \n %s' % self.word.synonym, font=('Ariel',12),justify=tk.CENTER)
        else: pass

        if not example=='':
            entry_example = canvas.create_text(100,150,anchor = tk.NW, text=self.word.example, font=('Ariel',12,'italic'))
        else: pass
        canvas.pack(fill=BOTH,expand=True)

        self.deletebutton = tk.Button(canvas,text='Delete',command= self.delete_entry)
        self.deletebutton.pack(side='bottom')

    #delete entry button (restarts script)
    def delete_entry(self):
        db = shelve.open('lifeisverylong')
        del db[self.word.word]
        db.close()
    
        restart_program()

#new entry pop up window ------------------------------------------------------------------------

class Popupself(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)
        self.config(bg='skyblue')
        options = {'padx': 5, 'pady': 5}

        #word
        self.word_label = ttk.Label(self, text = 'Word:', font='Arial 15')
        self.word_label.grid(column=0, row=0, sticky=tk.W, **options)
        
        self.word = tk.StringVar()
        self.word_entry = ttk.Entry(self, textvariable=self.word,font=('Arial 14'))
        self.word_entry.grid(column=1, row=0, **options)
        self.word_entry.focus()
       
       #definition
        self.defi_label = ttk.Label(self, text = 'Definition:',font='Arial 15')
        self.defi_label.grid(column=0, row=1, sticky=tk.W, **options)

        self.defi_entry = tk.Text(self,height=4,font='Arial 14',width=56) 
        self.defi_entry.grid(column=1, row=1, **options)
        self.defi_entry.focus()

        #synonym
        self.syn_label = ttk.Label(self, text = 'Synonym:',font='Arial 15')
        self.syn_label.grid(column=0, row=2, sticky=tk.W, **options)

        self.syn_entry = tk.Text(self, height=4,font='Arial 15',width=50) 
        self.syn_entry.grid(column=1, row=2, **options)
        self.syn_entry.focus()

        #example
        self.example_label = ttk.Label(self, text = 'Example:',font='Arial 15')
        self.example_label.grid(column=0, row=3, sticky=tk.W, **options)

        self.example_entry = tk.Text(self,height=4,font='Arial 15',width=50)
        self.example_entry.grid(column=1, row=3, **options)
        self.example_entry.focus()

        #save button (restarts script)
        self.save_button = ttk.Button(self, text='Save',command=lambda:[self.save(), self.destroy(), restart_program()])
        self.save_button.grid(column=0, row=5, sticky=tk.W, **options)
        #close button
        self.button_close = ttk.Button(self, text="Close", command=self.destroy)
        self.button_close.grid(column=6, row= 5, sticky=tk.W, **options)

    def save(self):
        if not self.word.get(): #if nothing is saved simply closed
            self.destroy()
        else: #we create an instance of the Entry class with the user's input and store it in shelve
            db = shelve.open('lifeisverylong')
            db[self.word.get()]=Entry(self.word.get(),self.defi_entry.get('1.0','end'),self.syn_entry.get('1.0','end'),self.example_entry.get('1.0','end'))
            db.close()

#main frame -----------------------------------------------------

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('685x350')
        self.root.resizable(False,False)
        self.root.title('Personal Dictionary')
        #paned window
        global pan
        pan = self.pan()

        #menu
        self.initUI()

        #list of entries
        self.list_entries = tk.Listbox(pan)
        self.list_entries.configure(background="dark blue", foreground="white", font=('Arial 15'))

        db = shelve.open('lifeisverylong')
        for index,word in enumerate(sorted(db.keys())):
            self.list_entries.insert(index,word)
        db.close()

        self.list_entries.bind('<Double-1>', self.item_selected) #shows entry's info upon double clicking
      
        #creating a set of frames for each entry so we can navigate thru them
        auxiliary = ttk.Frame(pan)

        self.frames={}
        db = shelve.open('lifeisverylong')
        for index,word in enumerate(sorted(db.keys())):
            frame = WordDef(auxiliary,word,db[word].definition,db[word].synonym,db[word].example)
            self.frames[index]=frame
            frame.pack(fill=BOTH,expand=1)
        
        pan.pack(fill=BOTH,expand=1)
        pan.add(self.list_entries)
        pan.add(auxiliary)
        self.show_frame(0)

    #paned window
    def pan(self):
        paned = tk.PanedWindow(self.root)
        return paned

    #change entry showing
    def show_frame(self, frame_num):
        for frame in self.frames.values():
            frame.pack_forget()
        frame = self.frames[frame_num]
        frame.pack(fill=BOTH,expand=1)

    def item_selected(self,event):
        selected_index = self.list_entries.curselection()[0]
        self.show_frame(selected_index)

    #menu
    def initUI(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu = menubar)
        filemenu = tk.Menu(menubar)
        filemenu.add_command(label = "New entry", command = self.popup)
        filemenu.add_command(label='Test',command=self.flashcards)
        menubar.add_cascade(label = "Actions", menu = filemenu)

    #word entry info
    def wordpopup(self,wrd):
        WordDef(self,wrd)

    #new entry popup window
    def popup(self):
        Popupself(self.root)

    #main loop 
    def run(self):
        self.root.mainloop()

    #flashcards
    def flashcards(self):
        Flashcard(self.root)
        
#class to create flashcards in a popup window -------------------------------------

class Flashcard(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)
        self.grab_set()
        try: #we create two shelves: one for the words we know and the other for the ones we don't
                #words are randomly chosen with a 0.75 probability of drawing from the to_learn shelve and 0.25 from i_know
            self.current_card = random.choice(random.choice(random.choices([list(to_learn.values()),list(i_know.values())],weights=[3,1],k=1)))
        except IndexError:
            self.current_card = random.choice(list(i_know.values()))

        self.card = tk.Canvas(self, width=500,height=400)
        self.card_title = self.card.create_text(35,35, anchor=tk.NW, text=self.current_card.word, font=('Arial','30','italic'))
        self.card.grid(row=0, column=0, columnspan=2)
        self.card.config(bg='sky blue',highlightthickness=0)

        
        self.nextbutton = tk.Button(self, text='Next',command=self.next_card)
        

        self.unknown_button = tk.Button(self, text='IDK',command=self.idontknow)
        self.unknown_button.grid(row=1, column=0, sticky="W")

        self.known_button = tk.Button(self, text='YEAH',command=self.iknow)
        self.known_button.grid(row=1, column=1, sticky="E")

    def next_card(self):
        #closes current flashcard and creates a new instance, which gives us a new randomly chosen word
        self.destroy()
        Flashcard(self.master)
    
    def idontknow(self):
        #i don't know the word: it's added to to_learn and we flip the card
        to_learn[self.current_card.word]=self.current_card
        self.flip_card()

    def iknow(self):
        #i know the word: it's either removed from to_learn and added to i_know, or just added to i_know
        if self.current_card in list(to_learn.values()):
            del to_learn[self.current_card.word]
            i_know[self.current_card.word] = self.current_card
        else:
            i_know[self.current_card.word] = self.current_card
        self.flip_card() #flip card
        
    def flip_card(self):
        #we reveal the word's meaning
        self.card_def = self.card.create_text(75, 100, anchor=tk.NW, text='DEFINITION: %s' % self.current_card.definition, font=("Ariel", 12))
        self.recdef = self.card.create_rectangle(70,90,425,187)

        if not self.current_card.synonym=='':
            self.entry_syn = self.card.create_text(75,225, anchor=tk.NW, text='SYNONYMS: \n %s' % self.current_card.synonym, font=('Ariel',12),justify=tk.CENTER)
        else: pass

        if not self.current_card.example=='':
            self.entry_example = self.card.create_text(100,150,anchor = tk.NW, text=self.current_card.example, font=('Ariel',12,'italic'))
        else: pass
        #we show the 'next' button that calls the new instance
        self.nextbutton.grid(column=0,row=1,sticky='E')
       #and we hide the known or unknown buttons 
        self.unknown_button.grid_forget()
        self.known_button.grid_forget()
        
# --- main ---

app = App()
app.run()
i_know.close()
to_learn.close()


