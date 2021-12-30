from tkinter import *
from tkinterdnd2 import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import re
import os


def createGUI():
    ws = TkinterDnD.Tk()
    ws.title('PythonGuides')
    ws.geometry('400x300')
    ws.config(bg='#fcb103')
    ws.drop_target_register(DND_FILES)
    ws.dnd_bind('<<Drop>>', show_text)

    frame = Frame(ws)
    frame.pack()
    ws.mainloop()


def show_text(event):    
    filePath = event.data 
    timeLine = removeArrow(filePath)
    textSpanish = trasnlate()
    unionString(timeLine, textSpanish, filePath)


def removeArrow(filePath): 
    file = open(filePath, "r") 
    splitText = re.split("\n", file.read().replace("<", "b"))
    
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

    file = open("suptitles/English.txt", "a")
    file.write(resultSuptitle)
    file.close() 

    return timeLine


def trasnlate():
    PATH = "./chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://translate.google.com/?op=docs") 

    driver.find_element_by_xpath("/html/body/c-wiz/div/div[2]/c-wiz/div[3]/c-wiz/div[1]/c-wiz/div[1]/c-wiz/div[5]/div/div[2]/div/div/span/button[2]/span[3]").click()

    upload_file = driver.find_element_by_xpath("/html/body/c-wiz/div/div[2]/c-wiz/div[3]/c-wiz/div[2]/c-wiz/div/div/form/div[1]/div[3]/input")
    upload_file.send_keys("C:/Users/unknow/Desktop/translate-subtitles-automatic-python-main (1)/translate-subtitles-automatic-python-main/suptitles/English.txt")

    driver.find_element_by_xpath("/html/body/c-wiz/div/div[2]/c-wiz/div[3]/c-wiz/div[2]/c-wiz/div/div/form/div[2]/div[2]/div/button").click()
    
    return driver.find_element_by_xpath("/html/body/pre").text.split("\n")
    
   
def unionString(timeLine, splitTextSpanish, filePathResurt):
    
    file = open("suptitles/English.txt", "r")
    splitTextEnglish = re.split("\n", file.read())
    file.close() 
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

    file = open(filePathResurt + ".vtt", "a", encoding="utf-8")
    file.write(str(unionResult))
    file.close() 


#Start program
createGUI()


