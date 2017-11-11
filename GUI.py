# -*- coding: utf-8 -*-

import tkinter as Tkinter
from retrieval.queryData import performQuery, retrieveCards, retrieveSetNames
from retrieval.storage import addSetToDatabase
#from retrieval.storage import changeCardInDatabase, addCardToDatabase, removeCardFromDatabase, addSetToDatabase
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
        
        OPTIONS = [
                   "French",
                   "Spanish"
                   ] #etc.
        self.language = Tkinter.StringVar()
        self.language.set(OPTIONS[0]) #default lanaguage
        w = Tkinter.OptionMenu(self.frame, self.language, *OPTIONS, command = self.languageSelect)
        w.grid(column = 1, row = 2)
        
        
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
        if (query == self.DEFAULT_SET_TEXT or query == ""):
            query = ""
            
        queryCard = self.entryVariableCard.get()
        if (queryCard == self.DEFAULT_CARD_TEXT or queryCard == ""):
            queryCard = ""
        
        listOfResultIndices = performQuery([query], [queryCard] , self.language.get())
        self.createRadioButtons(listOfResultIndices)     
        
        
    def OnRadioClick(self):
        indexOfSet = (self.radioVariable.get() - 1)
        cardSet = retrieveCards(indexOfSet, self.language.get())
        self.new_card_window(cardSet, indexOfSet, self.language.get())
        self.radioVariable.set(0)


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
        self.image_path_pairs = {0: "", 1: ""}
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

        menubar.add_command(label="Add/Edit Image", command = self.image_select)


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
        

        self.frame1 = Tkinter.Frame(self.master)
        self.frame1.grid()
        
        self.show_image()
        
        # add space between rows
        self.frame.grid_rowconfigure(3, minsize=20)
        
        
        for i in range(len(self.cardSet)):
            self.image_path_pairs[i] = ""
            

    def show_image(self):
        #refresh
        for label in self.frame1.grid_slaves():
            if int(label.grid_info()["row"]) < 6:
                label.grid_forget()
                
        path = self.image_path_pairs.get(self.currentIndex)
        if (path != ""):
            img = ImageTk.PhotoImage(Image.open(path))
            imagePanel = Tkinter.Label(self.frame1, image = img)
            imagePanel.image = img
            imagePanel.grid(column = 0, row = 1)
        else:
            notFound = Tkinter.Text(self.frame1, width = 40, height = 4)
            notFound.tag_configure("center", justify='center')
            notFound.insert("1.0", "No Images to Show", "center")
            notFound.grid(column = 0, row = 4)



    def get_picture(self):
        textToQueryForImage = self.questionText.get(1.0 ,Tkinter.END)
        paths = imageQuery([textToQueryForImage])
        if (len(paths) > 0):
            " "
        return paths;
        
    def image_select(self):
        
        #refresh
        for label in self.frame1.grid_slaves():
            if int(label.grid_info()["row"]) < 6:
                label.grid_forget()
        
        img_sample = ImageTk.PhotoImage(Image.open("ox.jpg"))
        
        ImgButton1 = Tkinter.Button(self.frame1, image = img_sample,
                                height = 100, width = 125, bg = "white", 
                                command = lambda: self.image_button(""))
        ImgButton2 = Tkinter.Button(self.frame1, image = img_sample,
                                height = 100, width = 125, bg = "white", 
                                command = lambda: self.image_button(""))
        ImgButton3 = Tkinter.Button(self.frame1, image = img_sample,
                                height = 100, width = 125, bg = "white", 
                                command = lambda: self.image_button(""))
        ImgButton4 = Tkinter.Button(self.frame1, image = img_sample,
                                height = 100, width = 125, bg = "white", 
                                command = lambda: self.image_button(""))
        notFound = Tkinter.Text(self.frame1, width = 40, height = 4)
        notFound.tag_configure("center", justify='center')
        notFound.insert("1.0", "No Relevant Images Found", "center")
        
        path_array = self.get_picture();
        numImage =  len(path_array)
        
        if (numImage == 0):
            #self.frame1.grid_forget()
            #self.frame1.grid()
            ImgButton1.grid_remove()
            ImgButton2.grid_remove()
            ImgButton3.grid_remove()
            ImgButton4.grid_remove()
            
            notFound.grid(column = 0, row = 4)
            
        
        if (numImage == 1):
            notFound.grid_forget()
            image_orig1 = Image.open(path_array[0])
            resized1 = image_orig1.resize((125, 100), Image.ANTIALIAS)
            img1 = ImageTk.PhotoImage(resized1)
            
            self.imagePanel = Tkinter.Label(self.frame1, image = img1, text = "Image 1")
            self.imagePanel.image = img1
            #self.imagePanel.grid(column = 0, row = 5)
            ImgButton1.config(image = img1, command = lambda: self.image_button(path_array[0]))
            ImgButton1.grid(column = 0, row = 4)
            
            
        if (numImage == 2):
            image_orig1 = Image.open(path_array[0])
            resized1 = image_orig1.resize((125, 100), Image.ANTIALIAS)
            img1 = ImageTk.PhotoImage(resized1)
            image_orig2 = Image.open(path_array[1])
            resized2 = image_orig2.resize((125, 100), Image.ANTIALIAS)
            img2 = ImageTk.PhotoImage(resized2)
            self.imagePanel1 = Tkinter.Label(self.frame1, image = img1, text = "Image 1")
            self.imagePanel1.image = img1
            self.imagePanel2 = Tkinter.Label(self.frame1, image = img2, text = "Image 2")
            self.imagePanel2.image = img2
            ImgButton1.config(image = img1, command = lambda: self.image_button(path_array[0]))
            ImgButton2.config(image = img2, command = lambda: self.image_button(path_array[1]))
            ImgButton1.grid(column = 0, row = 4)
            ImgButton2.grid(column = 1, row = 4)

            
        if (numImage == 3):
            image_orig1 = Image.open(path_array[0])
            resized1 = image_orig1.resize((125, 100), Image.ANTIALIAS)
            img1 = ImageTk.PhotoImage(resized1)
            image_orig2 = Image.open(path_array[1])
            resized2 = image_orig2.resize((125, 100), Image.ANTIALIAS)
            img2 = ImageTk.PhotoImage(resized2)
            image_orig3 = Image.open(path_array[2])
            resized3 = image_orig3.resize((125, 100), Image.ANTIALIAS)
            img3 = ImageTk.PhotoImage(resized3)
            self.imagePanel1 = Tkinter.Label(self.frame1, image = img1, text = "Image 1")
            self.imagePanel1.image = img1
            self.imagePanel2 = Tkinter.Label(self.frame1, image = img2, text = "Image 2")
            self.imagePanel2.image = img2
            self.imagePanel3 = Tkinter.Label(self.frame1, image = img3, text = "Image 3")
            self.imagePanel3.image = img3
            ImgButton1.config(image = img1, command = lambda: self.image_button(path_array[0]))
            ImgButton2.config(image = img2, command = lambda: self.image_button(path_array[1]))
            ImgButton3.config(image = img3, command = lambda: self.image_button(path_array[2]))
            ImgButton1.grid(column = 0, row = 4)
            ImgButton2.grid(column = 1, row = 4)
            ImgButton3.grid(column = 2, row = 4)

            
        if (numImage == 4):
            image_orig1 = Image.open(path_array[0])
            resized1 = image_orig1.resize((125, 100), Image.ANTIALIAS)
            img1 = ImageTk.PhotoImage(resized1)
            image_orig2 = Image.open(path_array[1])
            resized2 = image_orig2.resize((125, 100), Image.ANTIALIAS)
            img2 = ImageTk.PhotoImage(resized2)
            image_orig3 = Image.open(path_array[2])
            resized3 = image_orig3.resize((125, 100), Image.ANTIALIAS)
            img3 = ImageTk.PhotoImage(resized3)
            image_orig4 = Image.open(path_array[3])
            resized4 = image_orig4.resize((125, 100), Image.ANTIALIAS)
            img4 = ImageTk.PhotoImage(resized4)
            self.imagePanel1 = Tkinter.Label(self.frame1, image = img1, text = "Image 1")
            self.imagePanel1.image = img1
            self.imagePanel2 = Tkinter.Label(self.frame1, image = img2, text = "Image 2")
            self.imagePanel2.image = img2
            self.imagePanel3 = Tkinter.Label(self.frame1, image = img3, text = "Image 3")
            self.imagePanel3.image = img3
            self.imagePanel4 = Tkinter.Label(self.frame1, image = img4, text = "Image 4")
            self.imagePanel4.image = img4
            ImgButton1.config(image = img1, command = lambda: self.image_button(path_array[0]))
            ImgButton2.config(image = img2, command = lambda: self.image_button(path_array[1]))
            ImgButton3.config(image = img3, command = lambda: self.image_button(path_array[2]))
            ImgButton4.config(image = img4, command = lambda: self.image_button(path_array[3]))
            ImgButton1.grid(column = 0, row = 4)
            ImgButton2.grid(column = 1, row = 4)
            ImgButton3.grid(column = 0, row = 5)
            ImgButton4.grid(column = 1, row = 5)

        
    def image_button(self, value):
        self.image_path_pairs[self.currentIndex] = value
        self.show_image()
        
    def propose_translation(self):
        if (self.answerText['state'] == 'normal'):
            textToTranslate = self.questionText.get(1.0 ,Tkinter.END)
            translator = Translator()
            result = translator.translate(textToTranslate, src = 'English', dest = self.language).text
            self.answerText.delete(1.0 , Tkinter.END)
            self.answerText.insert(Tkinter.INSERT, '\n' + result)

    def delete_card(self):
        #removeCardFromDatabase(self.currentCard, self.language)
        self.cardSet.remove(self.currentCard)
        if (len(self.cardSet) == 0):
            self.add_card()
        else: 
            self.next_card()


    def add_card(self):
        #addCardToDatabase(self.indexInDatabase, 'Question', 'Answer', self.language)
        self.cardSet.append(['Question','Answer'])
        self.currentIndex = abs(len(self.cardSet) - 2)
        self.next_card()
        self.show_answer()

    def confirm_edit_card(self):
        changedQuestion = self.questionText.get(1.0 ,Tkinter.END).strip()
        changedAnswer= self.answerText.get(1.0 , Tkinter.END).strip()
        #changeCardInDatabase(self.indexInDatabase, self.currentCard, changedQuestion, changedAnswer, self.language)
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
        self.show_image()
    
    
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
        self.show_image()
    

if __name__ == "__main__":
    root = Tkinter.Tk()
    app = gengoFlashApp_tk(root)
    root.title('GengoFlash')
    root.mainloop()