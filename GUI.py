# -*- coding: utf-8 -*-

import tkinter as Tkinter
from retrieval.queryData import performQuery, retrieveCards, retrieveSetNames
from retrieval.storage import changeCardInDatabase, addCardToDatabase, removeCardFromDatabase, addSetToDatabase
from googletrans import Translator
from PIL import ImageTk, Image
from image_logic.image_searcher import imageQuery

class gengoFlashApp_tk:
    def __init__(self, master):
        self.master = master
        self.frame = Tkinter.Frame(self.master)
        self.numberOfRadioButtons = 0
        self.initialize(master)
        
    def initialize(self, master):
        self.frame.grid()
        
        self.DEFAULT_SET_TEXT = "Enter keywords related to the topic (or a name of the set to be added)"
        self.DEFAULT_CARD_TEXT = "Enter the words that the desired set might contain"
        
        #menu
        # create a toplevel menu
        menubar = Tkinter.Menu(master)
        menubar.add_command(label="Add set", command = self.add_set)

        # display the menu
        master.config(menu=menubar)
        #menu end
        
        #radio selection variable
        self.radioVariable = Tkinter.IntVar()
        
        #set entry field
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(
                self.frame, textvariable = self.entryVariable, width = 80)
        self.entry.grid(column = 0, row = 0, rowspan = 2, sticky = 'EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(self.DEFAULT_SET_TEXT)
        
        #card entry field
        self.entryVariableCard = Tkinter.StringVar()
        self.entryCard = Tkinter.Entry(
                self.frame, textvariable = self.entryVariableCard, width = 80)
        self.entryCard.grid(column = 0, row = 1, rowspan = 2, sticky = 'EW')
        self.entryVariableCard.set(self.DEFAULT_CARD_TEXT)
        self.entryCard.bind("<Return>", self.OnPressEnter)

        
        
        button = Tkinter.Button(self.frame, text = u"Search",
                                command = self.OnButtonClick, width = 10)
        button.grid(column = 1, row = 0)
        
        buttonAdd = Tkinter.Button(self.frame, text = u"Add set",
                                command = self.add_set, width = 10)
        buttonAdd.grid(column = 1, row = 1)
        
        #===========Edited by Risa, please clean up cod eif necessary!!
        OPTIONS = [
                   "French",
                   "Spanish"
                   ] #etc.
        self.language = Tkinter.StringVar()
        self.language.set(OPTIONS[0]) #default lanaguage
        w = Tkinter.OptionMenu(self.frame, self.language, *OPTIONS, command = self.languageSelect)
        w.grid(column = 1, row = 2)
        
        
        #===========Edited by Risa, END
        
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self.frame, textvariable = self.labelVariable,
                              anchor = "w", fg = "white", bg = "blue")
        label.grid(column = 0, row = 12, columnspan = 2, sticky = 'EW')
        self.labelVariable.set(u"Hello !")
        
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
    
    def add_set(self):
        addSetToDatabase(self.entryVariable.get(), self.language.get())
    
    def OnButtonClick(self):
        self.setLabelToEnteredText()
        self.searchForKeywords()
    
    def OnPressEnter(self, event):
        self.setLabelToEnteredText()
        self.searchForKeywords()
        
    def setLabelToEnteredText(self):
        self.labelVariable.set( "Search for: " + self.entryVariable.get() )
        
    def createRadioButtons(self, listForRadio):
        self.setTitles = retrieveSetNames(listForRadio - 1, self.language.get())
        
        #clean first
        for label in self.frame.grid_slaves():
            if (int(label.grid_info()["row"]) >= 3) and (int(label.grid_info()["row"]) != 12):
                label.grid_forget()               
            
            
        for x in range(0, len(listForRadio)):
            self.numberOfRadioButtons = len(listForRadio)
            Tkinter.Radiobutton(self.frame, indicatoron = 0, command = self.OnRadioClick,
            text= self.setTitles[x],
            padx = 80,
            value= listForRadio[x],
            variable = self.radioVariable).grid(column = 0, row = (3 + x),  columnspan = 2, sticky = 'EW')

    def searchForKeywords(self):
        query = self.entryVariable.get()
        if (query == self.DEFAULT_SET_TEXT):
            query = ""
            
        queryCard = self.entryVariableCard.get()
        if (queryCard == self.DEFAULT_CARD_TEXT):
            queryCard = ""
        
        listOfResultIndices = performQuery([query], [queryCard] , self.language.get())
        self.createRadioButtons(listOfResultIndices)     
        
        
    def OnRadioClick(self):
        indexOfSet = (self.radioVariable.get() - 1)
        cardSet = retrieveCards(indexOfSet, self.language.get())
        self.new_card_window(cardSet, indexOfSet, self.language.get())


    def new_card_window(self, cardSet, indexOfSet, language):
        self.newWindow = Tkinter.Toplevel(self.master)
        self.app = CardWindow(self.newWindow, cardSet, indexOfSet, language)
        
    def languageSelect(self, value):
        print("language is: "+ value)
        



class CardWindow:
    def __init__(self, master, cardSet, indexOfSet, language):
        self.master = master
        self.cardSet = cardSet
        self.indexInDatabase =indexOfSet
        self.currentIndex = 0
        self.language = language
        self.frame = Tkinter.Frame(self.master)
        self.initialize(master)
        
    def initialize(self, master):
        self.frame.grid()
        
        #menu
        # create a toplevel menu
        menubar = Tkinter.Menu(master)
        menubar.add_command(label="Add new", command = self.add_card)
        menubar.add_command(label="Delete current", command = self.delete_card)
        menubar.add_command(label="Edit", command = self.edit_card)
        menubar.add_command(label="Translate", command = self.propose_translation)
        menubar.add_command(label="Save edit", command = self.confirm_edit_card)
        menubar.add_command(label="Add Image", command = self.get_picture)

        # display the menu
        master.config(menu=menubar)
        #menu end
        
        self.currentCard = self.cardSet[self.currentIndex]
        
        self.showAnswerButton = Tkinter.Button(self.frame, text = 'Show answer', command = self.show_answer)
        self.showAnswerButton.grid(column = 1, row = 3)
        
        self.nextButton = Tkinter.Button(self.frame, text = 'Next', width = 8, command = self.next_card)
        self.nextButton.grid(column = 2, row = 3)
        
        self.prevButton = Tkinter.Button(self.frame, text = 'Previous', width = 8, command = self.previous_card)
        self.prevButton.grid(column = 0, row = 3)
        
        self.questionText = Tkinter.Text(self.frame, width = 25, height = 3)
        self.questionText.grid(column = 0, row = 0)
        self.questionText.insert(Tkinter.INSERT, '\n' + self.currentCard[0])
        self.questionText.config(state= Tkinter.DISABLED)
        
        self.answerText = Tkinter.Text(self.frame, width = 25, height = 3)
        self.answerText.grid(column = 2, row = 0)
        self.answerText.config(state= Tkinter.DISABLED)
        
        #add space for image
        window = master
        window.title("Card Image")
        window.geometry("485x300")
        window.resizable(width = True, height = True)
        window.configure(background='grey')
        
        path = "tiger.jpg"
        self.anotherPath = "0020_2462706533.jpg"
        
        img = ImageTk.PhotoImage(Image.open(path))
        self.imagePanel = Tkinter.Label(window, image = img)
        self.imagePanel.image = img
        self.imagePanel.grid(column = 0, row = 4)
        #self.imagePanel.place(x = 0, y = 4)
        #self.imagePanel.pack(side="top", fill="both", expand=True)
        # add space between rows
        self.frame.grid_rowconfigure(3, minsize=20)

    def get_picture(self):
        textToQueryForImage = self.questionText.get(1.0 ,Tkinter.END)
        paths = imageQuery([textToQueryForImage])
        if (len(paths) > 0):
            img = ImageTk.PhotoImage("0020_2462706533.jpg")
            #Image.open(path.relpath(paths[0])))
            print(textToQueryForImage)
            print(paths[0])
            self.imagePanel.image = img

    def propose_translation(self):
        if (self.answerText['state'] == 'normal'):
            textToTranslate = self.questionText.get(1.0 ,Tkinter.END)
            translator = Translator()
            result = translator.translate(textToTranslate, src = 'English', dest = self.language).text
            self.answerText.delete(1.0 , Tkinter.END)
            self.answerText.insert(Tkinter.INSERT, '\n' + result)

    def delete_card(self):
        removeCardFromDatabase(self.currentCard, self.language)
        self.cardSet.remove(self.currentCard)
        if (len(self.cardSet) == 0):
            self.add_card()
        else: 
            self.next_card()


    def add_card(self):
        addCardToDatabase(self.indexInDatabase, 'Question', 'Answer', self.language)
        self.cardSet.append(['Question','Answer'])
        self.currentIndex = abs(len(self.cardSet) - 2)
        self.next_card()
        self.show_answer()

    def confirm_edit_card(self):
        changedQuestion = self.questionText.get(1.0 ,Tkinter.END).strip()
        changedAnswer= self.answerText.get(1.0 , Tkinter.END).strip()
        changeCardInDatabase(self.indexInDatabase, self.currentCard, changedQuestion, changedAnswer, self.language)
        self.currentCard[0] = changedQuestion
        self.currentCard[1] = changedAnswer
        
        self.answerText.config(state= Tkinter.DISABLED)
        self.questionText.config(state= Tkinter.DISABLED)


    def edit_card(self):
        self.show_answer()
        self.answerText.config(state= Tkinter.NORMAL)
        self.questionText.config(state= Tkinter.NORMAL)


    def show_answer(self):
        self.answerText.config(state= Tkinter.NORMAL)
        if (len(self.answerText.get(1.0 , Tkinter.END)) == 1):
            self.answerText.insert(Tkinter.INSERT, '\n' + self.currentCard[1])
        self.answerText.config(state= Tkinter.DISABLED)
    
    
    def next_card(self):
        self.currentIndex = (self.currentIndex + 1) % len(self.cardSet)
        self.questionText.config(state= Tkinter.NORMAL)
        self.questionText.delete(1.0 , Tkinter.END)
        self.answerText.config(state= Tkinter.NORMAL)
        self.answerText.delete(1.0 , Tkinter.END)
        self.answerText.config(state= Tkinter.DISABLED)
        self.currentCard = self.cardSet[self.currentIndex]
        self.questionText.insert(Tkinter.INSERT, '\n' + self.currentCard[0])
        self.questionText.config(state= Tkinter.DISABLED)
    
    
    def previous_card(self):
        if ((self.currentIndex - 1) >= 0) :
            self.currentIndex -= 1
        else:
            self.currentIndex = len(self.cardSet) - 1
                
        self.questionText.config(state= Tkinter.NORMAL)
        self.questionText.delete(1.0 , Tkinter.END)
        self.answerText.config(state= Tkinter.NORMAL)
        self.answerText.delete(1.0 , Tkinter.END)
        self.answerText.config(state= Tkinter.DISABLED)
        self.currentCard = self.cardSet[self.currentIndex]
        self.questionText.insert(Tkinter.INSERT, '\n' + self.currentCard[0])
        self.questionText.config(state= Tkinter.DISABLED)
    

if __name__ == "__main__":
    root = Tkinter.Tk()
    app = gengoFlashApp_tk(root)
    root.title('GengoFlash')
    root.mainloop()