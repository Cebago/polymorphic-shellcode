import json
import os
import random
import re

registers = ["rax", "rbx", "rcx", "rdx", "rdi", "rsi",
             "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]


def selectFile(folder):
    """
    Function to select the file to use 
    ```python
    @param str folder : The folder path wich content files
    @return file|bool : Returns the file descriptor of the specified one.
    ```
    """
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
    """
    Function to open the dico for assembly change 
    ```python
    @return json : Returns the content of the file use for dico
    ```
    """
    file = open("dico.json")
    data = json.load(file)
    file.close()
    return data


def getRandomReg(current_reg_tab):
    """
    Pick a random value from the `registers` array 
    ```python
    @return str : Returns a string containing random 64-bits register
    ```
    """
    while(True):
        random_reg = random.choice(registers)
        if(random_reg not in current_reg_tab):
            return random_reg


def replace(val_tab, replacement, random_reg=False):
    """
    Replace formatted string with values
    ```python
    @return str : Returns the formatted string with values
    ```
    """
    if random_reg:
        replacement = re.sub(r"\${REG}", random_reg, replacement)
    replacement = re.sub(r"\${VAL1}", val_tab[0], replacement)
    replacement = re.sub(r"\${VAL2}", val_tab[1], replacement)
    return replacement


def getReplacement(tab_dico, action_key, val_tab):
    replacement = random.choice(tab_dico["values"][action_key])
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
                    if str[0] == key:
                        print(f"élément :{str}")
                        replace_value_patern = getRandomReplacement(
                            search["values"], search["searches"][key], str)
                        if re.search(r"\${REG}", replace_value_patern):
                            random_reg = getRandomReg(str[1])
                        else:
                            random_reg = False
                        replace_value = replace(
                            str[1], replace_value_patern, random_reg)
                        output.write(replace_value)
                        founded = True
                if not founded:
                    output.write(line)


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
    # mov rax, 5 => ["mov", "rax", "5"] | xor rax, rax
    split = re.split(r"\, |\,| |\n| \n", str)
    returnStr = str
    for iterator in range(0, len(split)):
        val = "${{VAL{}}}".format(iterator)
        if split[iterator] in registers:
            # mov rax, 5 => mov ${REG}, 5
            returnStr = re.sub(split[iterator], val, returnStr)
            reg.append(split[iterator].strip())  # [rax]
        elif re.search("[0-9]+", split[iterator]):
            # mov ${REG}, 5 => mov ${REG}, ${VAR}
            returnStr = re.sub(split[iterator], val, returnStr)
            reg.append(split[iterator])  # [rax, 5]
    return [returnStr.strip(), reg]  # ["mov ${REG}, ${VAR}", ["rax", 5]]
