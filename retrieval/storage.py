
import re
def addSetToDatabase(setName):
    lastIndex = 0
    with open("retrieval/data/SETTITLES.ALL") as f:
        for line in f:
            if ".I" in line:
                lastIndex = int(re.search(r'\d+', line).group())
    with open("retrieval/data/SETTITLES.ALL", "a") as myfile:
        myfile.write(".I " + str(lastIndex + 1) + '\n')
        myfile.write(".W\n")
        myfile.write(setName + '\n')           
                
    with open("retrieval/data/WHOLESETS.ALL", "a") as myfile:
        myfile.write(".I " + str(lastIndex + 1) + '\n')
        myfile.write(".W\n")
        myfile.write('Question - Answer' + '\n')   
                
def removeCardFromDatabase(currentCard):
    # Read in the file
    with open('retrieval/data/WHOLESETS.ALL', 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(currentCard[0] + ' - ' + currentCard[1] + ';', '')
    filedata = filedata.replace(currentCard[0] + ' - ' + currentCard[1], '')

    # Write the file out again
    with open('retrieval/data/WHOLESETS.ALL', 'w') as file:
        file.write(filedata)
    
    
def changeCardInDatabase(indexInDatabase, currentCard, changedQuestion, changedAnswer):
    # Read in the file
    with open('retrieval/data/WHOLESETS.ALL', 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(currentCard[0] + ' - ' + currentCard[1], changedQuestion + ' - ' + changedAnswer)

    # Write the file out again
    with open('retrieval/data/WHOLESETS.ALL', 'w') as file:
        file.write(filedata)
def addCardToDatabase(indexInDatabase, Question, Answer):
    f = open("retrieval/data/WHOLESETS.ALL", "r")
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

    f = open("retrieval/data/WHOLESETS.ALL", "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()
