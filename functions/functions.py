import os
import re
import json

registers = ["rax", "rbx", "rcx", "rdx", "rdi", "rsi", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]

def selectFile(folder):
    while True:
        files = os.listdir('./'+folder)
        for x in range(len(files)):
            print(str(x+1)+"- "+files[x])
        print("!q- Quit")
        file = input("choice: ")
        try:
            x = int(file)
            if (x >= 1 and x <= len(files)):
                return files[x-1]
            else:
                print("Not a good value")                
        except ValueError:
            if file == "!q":
                return False
            print("Not a good value")

def openDico():
    tabDico = []
    file = open("dico.json")
    data = json.load(file)
    for search in data['searches']:
        # print(search)
        tabDico.append(search)
    file.close()
    return tabDico

def readAsm(search):

    toModify = [] #tableau 2 dimensions pour mettre la ligne remplçable et le numéro de la ligne remplaçable
    try:
        file = open("test.asm", "r")
        for line in enumerate(file):
            print(line) 
            for searchDico in search:
                if search == line:
                    toModify.append([line][search])
    finally:
        file.close()

def displayFile(folder, file):
    os.system('less ' + './' + folder + '/' + file)

def verifyFile(folder, file):
    with open('./' + folder + '/' + file, 'r') as f:
        content = f.read()
    search = re.search(".*\\\\x00.*", str(content))
    if search:
        return False
    return True

def replaceInStr(str):
    split = re.split(r"\, |\,| ", str)
    reg = []
    returnStr = str
    for x in split:
        if x in registers:
            returnStr = re.sub(x, "${REG}", returnStr)
            reg.append(x)
    # CALL FUNCTION FOR SEARCHING AN ALIAS IN DICO JSON
    print(returnStr)
    print(reg)
    return returnStr