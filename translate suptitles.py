from tkinter import *
from tkinterdnd2 import * 
import re
import os
import pyperclip
import os 


def createGUI(functionFilePath):
    ws = TkinterDnD.Tk()
    ws.title('PythonGuides')
    ws.geometry('400x300')
    ws.config(bg='#fcb103')
    ws.drop_target_register(DND_FILES)
    ws.dnd_bind('<<Drop>>', functionFilePath)

    frame = Frame(ws)
    frame.pack()
    ws.mainloop()


def show_text(event):    
    filePath = event.data 
    timeLine = removeArrow(filePath)

    #Copy in clipboard
    pyperclip.copy(textFromFile("suptitles/English.txt"))
    pyperclip.paste()
     
    def show_text2 (event):
        filePath2 = event.data[1:len(event.data)-1]

        textSpanish = textFromFile(filePath2).split("\n")
        unionString(timeLine, textSpanish, filePath)
        
    createGUI(show_text2)

    
def removeArrow(filePath):  
    splitText = re.split("\n", textFromFile(filePath).replace("<", "b"))
    
    if(splitText[0] != "WEBVTT"):
        splitText.insert(0, "WEBVTT \n \n") 

    splitText.pop(1)    

    resultSuptitle = ""  
    timeLine = [] 

    j = 0
    for i in splitText: 
        if "-->" in i:
            splitText.pop(j - 1)
        j += 1
            
    for i in splitText:
        if "-->" not in i and "WEBVTT" not in i: 
            resultSuptitle += i + '\n' 
        elif i not in "WEBVTT": 
            timeLine.append(i.replace(",", "."))  

    saveTextInFile("suptitles/English.txt", resultSuptitle)

    return timeLine



    
   
def unionString(timeLine, splitTextSpanish, filePathResurt):
    splitTextEnglish = re.split("\n", textFromFile("suptitles/English.txt")) 
    os.remove("suptitles/English.txt")

    unionResult = "WEBVTT \n \n" + timeLine[0] + "\n"

    j = 0
    jT = 1
    for i in splitTextEnglish:
        if i != "" and j < len(splitTextSpanish):
            unionResult += i + "\n" + splitTextSpanish[j]+ "\n"
        elif jT < len(timeLine):
            unionResult += "\n" + timeLine[jT] + "\n"
            jT += 1
        j += 1  

    filePathResurt = filePathResurt + ".vtt"
    saveTextInFile(filePathResurt, str(unionResult))


#Helpers function
def saveTextInFile(path, textToSave):
    file = open(path, "a", encoding="utf8")
    file.write(textToSave)
    file.close() 
    
def textFromFile(path):
    file = open(path, "r", encoding="utf8")
    fileText = file.read()
    file.close()
    return fileText

#Start program, encoding='cp856', errors='ignore'
createGUI(show_text)


