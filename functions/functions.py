import os
import re
import json
import random

registers = ["rax", "rbx", "rcx", "rdx", "rdi", "rsi", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]
reg = []

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
    keyDico = []
    valueDico = []
    file = open("dico.json")
    data = json.load(file)     
    file.close()
    return data



def getRandomReg(current_reg):
    while(True):
        random_reg = random.choice(registers)
        if(random_reg != current_reg):
            return random_reg


print(getRandomReg("rax"))

def readAsm(search):
    toModify = [] #tableau 2 dimensions pour mettre la ligne remplçable et le numéro de la ligne remplaçable
    with open("test.asm", "r") as shellcode:
        #while shellcode != EOF:
        for line in shellcode:
            #print(replaceInStr(line))
            for key in search["searches"]:
                if  re.search(key,repr(line)):
                    #aliasDico(key)
                    print(f"founded : {line}")
   
    return toModify

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
    returnStr = str
    tmp = []
    for x in split:
        if x in registers:
            returnStr = re.sub(x, "${REG}", returnStr)
            tmp.append(x)
        elif re.search("[0-9]+", x):
            returnStr = re.sub(x, "${VAR}", returnStr)
            tmp.append(x)
    if len(tmp) != 0:
        reg.append(tmp)
    # CALL FUNCTION FOR SEARCHING AN ALIAS IN DICO JSON
    alias = aliasDico()
    print(returnStr)
    print(reg)
    return returnStr

def aliasDico(toModify, search, key):
    toReplace = []
    for keyword in search["values"]:
        for value in toModify:
            if keyword == value:
                for values in search["values"][keyword]:
                    toReplace.append(values)
    return toReplace
                    

