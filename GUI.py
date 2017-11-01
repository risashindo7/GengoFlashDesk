# -*- coding: utf-8 -*-

import tkinter as Tkinter
from retrieval.queryData import performQuery, retrieveCards, retrieveSetNames

class gengoFlashApp_tk(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
        
    def initialize(self):
        self.grid()
        
        #radio selection variable
        self.radioVariable = Tkinter.IntVar()
        
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(
                self, textvariable = self.entryVariable, width = 80)
        self.entry.grid(column = 0, row = 0, sticky = 'EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter keywords related to the topic")
        
        button = Tkinter.Button(self, text = u"Search",
                                command = self.OnButtonClick, width = 10)
        button.grid(column = 1, row = 0)
        
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable = self.labelVariable,
                              anchor = "w", fg = "white", bg = "blue")
        label.grid(column = 0, row = 12, columnspan = 2, sticky = 'EW')
        self.labelVariable.set(u"Hello !")
        
        self.grid_columnconfigure(0, weight = 1)
        self.resizable(True, False)
        self.update()
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
        setTitles = retrieveSetNames(listForRadio - 1)
        for x in range(0, len(listForRadio)):
            Tkinter.Radiobutton(self, indicatoron = 0, command = self.OnRadioClick,
            text= setTitles[x],
            padx = 80,
            value= listForRadio[x],
            variable = self.radioVariable).grid(column = 0, row = (1 + x),  columnspan = 2, sticky = 'EW')

    def searchForKeywords(self):
        query = self.entryVariable.get()
        listOfResultIndices = performQuery([query])
        self.createRadioButtons(listOfResultIndices)     
        
        
    def OnRadioClick(self):
        indexOfSet = (self.radioVariable.get() - 1)
        print (retrieveCards(indexOfSet))


if __name__ == "__main__":
    app = gengoFlashApp_tk(None)
    app.title('GengoFlash')
    app.mainloop()