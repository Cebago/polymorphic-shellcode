import os
import re
import json
import random

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


#print(getRandomReg("rax"))

def getReplacement(tab_dico, action_key, val_tab):
    replacement = random.choice(tab_dico["values"][action_key])
    random_reg = getRandomReg(val_tab[0])
    replacement = re.sub(r"\${REG}", random_reg, replacement)
    replacement = re.sub(r"\${VAL1}", val_tab[0], replacement)
    replacement = re.sub(r"\${VAL2}", val_tab[1], replacement)
    

    print(f"\n\nValeur de remplacement \n{replacement}\n\n")
    return replacement

def readAsm(search):

    toModify = [] #tableau 2 dimensions pour mettre la ligne remplçable et le numéro de la ligne remplaçable
    with open("test.asm", "r") as shellcode:
        #while shellcode != EOF:
        for line in shellcode:
            str = replaceInStr(line)
            for key in search["searches"]:
                print(f"key: {str[0]}")
                if  str[0] == key:
                    print("élément similaire trouvé")
                    #print(f"values : {str[1]}")
                    replace_value = getReplacement(search, search["searches"][key], str[1])
                    #aliasDico(key)
                    #print(f"founded : {line}")


   
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
    reg = [] 
    split = re.split(r"\, |\,| ", str) # mov rax, 5 => ["mov", "rax", "5"] | xor rax, rax
    returnStr = str
    for iterator in range (0, len(split)):
        val = "${{VAL{}}}".format(iterator)
        if split[iterator] in registers:
            # mov rax, 5 => mov ${REG}, 5
            returnStr = re.sub(split[iterator], val , returnStr)
            reg.append(split[iterator])  # [rax]
        elif re.search("[0-9]+", split[iterator]):
            # mov ${REG}, 5 => mov ${REG}, ${VAR}
            returnStr = re.sub(split[iterator], val, returnStr)
            reg.append(split[iterator])  # [rax, 5]
    return [returnStr.strip(), reg] # ["mov ${REG}, ${VAR}", ["rax", 5]]

def aliasDico(search, key, value):
    for keyword in search["values"]:
        if keyword == value:
            if not search["values"][keyword] == key:
                print("ok")
    return 0

                    

