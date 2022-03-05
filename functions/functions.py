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



def getRandomReg(current_reg_tab):
    while(True):
        random_reg = random.choice(registers)
        if(random_reg not in current_reg_tab):
            return random_reg


#print(getRandomReg("rax"))

def replace(val_tab, replacement, random_reg = False):
    if random_reg:
        replacement = re.sub(r"\${REG}", random_reg, replacement)
        
    replacement = re.sub(r"\${VAL1}", val_tab[0], replacement)
    replacement = re.sub(r"\${VAL2}", val_tab[1], replacement)
    return replacement 


def getReplacement(tab_dico, action_key, val_tab):
    replacement = random.choice(tab_dico["values"][action_key])
    random_reg = getRandomReg(val_tab[0])
   
    return replacement

def getRandomReplacement(tab_dico, action_key, current_value):
    while(True):
        random_replacement = random.choice(tab_dico[action_key])
        if(random_replacement != current_value):
            return random_replacement



def readAsm(search):

    with open("test.asm", "r") as input:
        with open("output.asm", "wt") as output:
            for line in input:
                str = replaceInStr(line)
                founded = False
                for key in search["searches"]:
                    if  str[0] == key:
                        print(f"élément :{str}")
                        #print(f"values : {str[1]}")
                        replace_value_patern = getRandomReplacement(search["values"], search["searches"][key], str)

                
                        if re.search(r"\${REG}",replace_value_patern):
                            random_reg= getRandomReg(str[1])
                        else:
                            random_reg = False

                        replace_value = replace(str[1], replace_value_patern, random_reg)


                        output.write(replace_value)
                        founded = True
                if not founded:
                    output.write(line)

   
    return 'ok'

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

    str = str.split(";")[0]
    str = str.strip()
    split = re.split(r"\, |\,| |\n| \n", str) # mov rax, 5 => ["mov", "rax", "5"] | xor rax, rax
    returnStr = str
    for iterator in range (0, len(split)):
        val = "${{VAL{}}}".format(iterator)
        if split[iterator] in registers:
            # mov rax, 5 => mov ${REG}, 5
            returnStr = re.sub(split[iterator], val , returnStr)
            reg.append(split[iterator].strip())  # [rax]
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

                    

