# -*- coding: utf-8 -*-

import tkinter as Tkinter
import itertools
from retrieval.queryData import performQuery, retrieveCards, retrieveSetNames

class gengoFlashApp_tk:
    def __init__(self, master):
        self.master = master
        self.frame = Tkinter.Frame(self.master)
        self.initialize(master)
        
    def initialize(self, master):
        self.frame.grid()
        
        #radio selection variable
        self.radioVariable = Tkinter.IntVar()
        
        
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(
                self.frame, textvariable = self.entryVariable, width = 80)
        self.entry.grid(column = 0, row = 0, sticky = 'EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter keywords related to the topic")
        
        button = Tkinter.Button(self.frame, text = u"Search",
                                command = self.OnButtonClick, width = 10)
        button.grid(column = 1, row = 0)
        
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self.frame, textvariable = self.labelVariable,
                              anchor = "w", fg = "white", bg = "blue")
        label.grid(column = 0, row = 12, columnspan = 2, sticky = 'EW')
        self.labelVariable.set(u"Hello !")
        
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        
    def OnButtonClick(self):
        self.setLabelToEnteredText()
        self.searchForKeywords()
    
    def OnPressEnter(self, event):
        self.setLabelToEnteredText()
        self.searchForKeywords()
        
    def setLabelToEnteredText(self):
        self.labelVariable.set( "Search for: " + self.entryVariable.get() )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        
    def createRadioButtons(self, listForRadio):
        self.setTitles = retrieveSetNames(listForRadio - 1)
        for x in range(0, len(listForRadio)):
            Tkinter.Radiobutton(self.frame, indicatoron = 0, command = self.OnRadioClick,
            text= self.setTitles[x],
            padx = 80,
            value= listForRadio[x],
            variable = self.radioVariable).grid(column = 0, row = (1 + x),  columnspan = 2, sticky = 'EW')

    def searchForKeywords(self):
        query = self.entryVariable.get()
        listOfResultIndices = performQuery([query])
        self.createRadioButtons(listOfResultIndices)     
        
        
    def OnRadioClick(self):
        indexOfSet = (self.radioVariable.get() - 1)
        cardSet = retrieveCards(indexOfSet)
        self.new_card_window(cardSet, indexOfSet)


    def new_card_window(self, cardSet, indexOfSet):
        self.newWindow = Tkinter.Toplevel(self.master)
        self.app = CardWindow(self.newWindow, cardSet, indexOfSet)
        

class CardWindow:
    def __init__(self, master, cardSet, indexOfSet):
        self.master = master
        self.cardSet = itertools.cycle(cardSet)
        self.indexInDatabase =indexOfSet 
        self.frame = Tkinter.Frame(self.master)
        self.initialize(master)
        
    def initialize(self, master):
        self.frame.grid()
        
        self.currentCard = next(self.cardSet)
        
        self.showAnswerButton = Tkinter.Button(self.frame, text = 'Show answer', command = self.show_answer)
        self.showAnswerButton.grid(column = 1, row = 2)
        
        self.nextButton = Tkinter.Button(self.frame, text = 'Next', width = 8, command = self.next_card)
        self.nextButton.grid(column = 2, row = 2)
        
        self.questionText = Tkinter.Text(self.frame, width = 15, height = 3)
        self.questionText.grid(column = 0, row = 0)
        self.questionText.insert(Tkinter.INSERT, '\n' + self.currentCard[0])
        self.questionText.config(state= Tkinter.DISABLED)
        
        self.answerText = Tkinter.Text(self.frame, width = 15, height = 3)
        self.answerText.grid(column = 2, row = 0)
        self.answerText.config(state= Tkinter.DISABLED)


    def show_answer(self):
        self.answerText.config(state= Tkinter.NORMAL)
        self.answerText.insert(Tkinter.INSERT, '\n' + self.currentCard[1])
        self.answerText.config(state= Tkinter.DISABLED)
    
    
    def next_card(self):
        self.questionText.config(state= Tkinter.NORMAL)
        self.questionText.delete(1.0 , Tkinter.END)
        self.answerText.config(state= Tkinter.NORMAL)
        self.answerText.delete(1.0 , Tkinter.END)
        self.answerText.config(state= Tkinter.DISABLED)
        self.currentCard = next(self.cardSet)
        self.questionText.insert(Tkinter.INSERT, '\n' + self.currentCard[0])
        self.questionText.config(state= Tkinter.DISABLED)
    

if __name__ == "__main__":
    root = Tkinter.Tk()
    app = gengoFlashApp_tk(root)
    root.title('GengoFlash')
    root.mainloop()