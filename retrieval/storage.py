
import re
def addSetToDatabase(setName, language):
    lastIndex = 0
    if (language == "Spanish"):
        with open('retrieval/data/data_spanish/SETTITLES.ALL') as f:
            for line in f:
                if ".I" in line:
                    lastIndex = int(re.search(r'\d+', line).group())
        with open('retrieval/data/data_spanish/SETTITLES.ALL', "a") as myfile:
            myfile.write(".I " + str(lastIndex + 1) + '\n')
            myfile.write(".W\n")
            myfile.write(setName + '\n')           
                    
        with open('retrieval/data/data_spanish/WHOLESETS.ALL', "a") as myfile:
            myfile.write(".I " + str(lastIndex + 1) + '\n')
            myfile.write(".W\n")
            myfile.write('Question - Answer' + '\n')   
    elif (language == "French"):
        with open('retrieval/data/data_french/SETTITLES.ALL') as f:
            for line in f:
                if ".I" in line:
                    lastIndex = int(re.search(r'\d+', line).group())
        with open('retrieval/data/data_french/SETTITLES.ALL', "a") as myfile:
            myfile.write(".I " + str(lastIndex + 1) + '\n')
            myfile.write(".W\n")
            myfile.write(setName + '\n')           
                    
        with open('retrieval/data/data_french/WHOLESETS.ALL', "a") as myfile:
            myfile.write(".I " + str(lastIndex + 1) + '\n')
            myfile.write(".W\n")
            myfile.write('Question - Answer' + '\n') 
                
def removeCardFromDatabase(currentCard, language):
    # Read in the file
    if (language == "Spanish"):
        with open('retrieval/data/data_spanish/WHOLESETS.ALL', 'r') as file :
            filedata = file.read()
    
        # Replace the target string
        filedata = filedata.replace(currentCard[0] + ' - ' + currentCard[1] + ';', '')
        filedata = filedata.replace(currentCard[0] + ' - ' + currentCard[1], '')
    
        # Write the file out again
        with open('retrieval/data/data_spanish/WHOLESETS.ALL', 'w') as file:
            file.write(filedata)
            
    elif (language == "French"):
        with open('retrieval/data/data_french/WHOLESETS.ALL', 'r') as file :
            filedata = file.read()
    
        # Replace the target string
        filedata = filedata.replace(currentCard[0] + ' - ' + currentCard[1] + ';', '')
        filedata = filedata.replace(currentCard[0] + ' - ' + currentCard[1], '')
    
        # Write the file out again
        with open('retrieval/data/data_french/WHOLESETS.ALL', 'w') as file:
            file.write(filedata)
    
def changeCardInDatabase(indexInDatabase, currentCard, changedQuestion, changedAnswer, language):
    if (language == "Spanish"):
        # Read in the file
        with open('retrieval/data/data_spanish/WHOLESETS.ALL', 'r') as file :
            filedata = file.read()
    
        # Replace the target string
        filedata = filedata.replace(currentCard[0] + ' - ' + currentCard[1], changedQuestion + ' - ' + changedAnswer)
    
        # Write the file out again
        with open('retrieval/data/data_spanish/WHOLESETS.ALL', 'w') as file:
            file.write(filedata)
    elif (language == "French"):
        with open('retrieval/data/data_french/WHOLESETS.ALL', 'r') as file :
            filedata = file.read()
    
        # Replace the target string
        filedata = filedata.replace(currentCard[0] + ' - ' + currentCard[1], changedQuestion + ' - ' + changedAnswer)
    
        # Write the file out again
        with open('retrieval/data/data_french/WHOLESETS.ALL', 'w') as file:
            file.write(filedata)
def addCardToDatabase(indexInDatabase, Question, Answer, language):
    if (language == "Spanish"):
        f = open("retrieval/data/data_spanish/WHOLESETS.ALL", "r")
    elif (language == "French"):
        f = open("retrieval/data/data_french/WHOLESETS.ALL", "r")
        
    contents = f.readlines()
    lookup = '.I ' + str(indexInDatabase + 1)
    f.close()
    index = 0
    endOfAddedLine = ""
    
    with open("retrieval/data/WHOLESETS.ALL") as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                index = num + 1
            if (index != 0 and num == index):
                if (len(line) > 0 and not(".I" in line)):
                    endOfAddedLine = ";"
            if (index != 0 and num > index):
                break

    value = Question + ' - ' + Answer + endOfAddedLine + '\n'
    contents.insert(index, value)

    if (language == "Spanish"):
        f = open("retrieval/data/data_spanish/WHOLESETS.ALL", "w")
    elif (language == "French"):
        f = open("retrieval/data/data_french/WHOLESETS.ALL", "w")
    
    contents = "".join(contents)
    f.write(contents)
    f.close()
