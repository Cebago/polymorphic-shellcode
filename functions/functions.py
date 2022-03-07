import json
import os
import random
import re
import subprocess

registers = ["rax", "rbx", "rcx", "rdx", "rdi", "rsi",
             "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]


def chooseFolder():
    """
    Function to select the folder to use 
    ```python
    @return str : Returns the folder choose by the user
    ```
    """
    quit = False
    while True:
        print("In which folder do you want to generate the shellcode from :")
        print("1- Input")
        print("2- Output")
        print("!q- Quit")
        choice = input("Choice: ")
        if (choice == "1"):
            return "input"
        elif (choice == "2"):
            return "output"
        elif (choice == "!q"):
            return False
        else:
            print("Not a good value")


def selectFile(folder: str):
    """
    Function to select the file to use 
    ```python
    @param str folder : The folder path wich content files
    @return str|bool : Returns the file descriptor of the specified one.
    ```
    """
    while True:
        files = os.listdir("./{}".format(folder))
        for x in range(len(files)):
            print("{}- {}".format(str(x + 1), files[x]))
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


def getRandomReg(current_reg_tab: list):
    """
    Pick a random value from the `registers` array 
    ```python
    @param list current_reg_tab : The current registers already used
    @return str : Returns a string containing random 64-bits register
    ```
    """
    while(True):
        random_reg = random.choice(registers)
        if(random_reg not in current_reg_tab):
            return random_reg


def replace(val_tab: list, replacement: str, random_reg: bool = False):
    """
    Replace formatted string with values
    ```python
    @param list val_tab : The list of values to use
    @param str replacement : The formatted string to replace in
    @param bool random_reg : A boolean to know if the getRandomReg() functions has been used
    @return str : Returns the formatted string with values
    ```
    """
    if random_reg:
        replacement = re.sub(r"\${REG}", random_reg, replacement)
    replacement = re.sub(r"\${VAL1}", val_tab[0], replacement)
    replacement = re.sub(r"\${VAL2}", val_tab[1], replacement)
    return replacement


def getRandomReplacement(tab_dico: list, action_key: str, current_value: str):
    """
    Return a random instruction from the dico
    ```python
    @param list tab_dico : The list of values to usepossible instructions from the dico
    @param str action_key : The key describing the action
    @param str current_value : The current value 
    @return str : Returns a formatted random string from the dico
    ```
    """
    while(True):
        random_replacement = random.choice(tab_dico[action_key])
        if(random_replacement != current_value):
            return random_replacement


def readAsm(fileName: str):
    """
    Read the asked file and tranform it to a polymorphed one
    ```python
    @param str fileName : The input file name
    ```
    """
    dico = openDico()
    with open(f"./input/{fileName}", "r") as input:
        with open(f"./output/{fileName}", "wt") as output:
            for line in input:
                formattedString = replaceInStr(line)
                founded = False
                for key in dico["searches"]:
                    if formattedString[0] == key:
                        replace_value_patern = getRandomReplacement(
                            dico["values"], dico["searches"][key], formattedString)
                        if re.search(r"\${REG}", replace_value_patern):
                            random_reg = getRandomReg(formattedString[1])
                        else:
                            random_reg = False
                        replace_value = replace(
                            formattedString[1], replace_value_patern, random_reg)
                        output.write(replace_value)
                        founded = True
                if not founded:
                    output.write(line)


def displayFile(folder: str, file: str):
    """
    Display the file
    """
    # os.system('less ' + './' + folder + '/' + file)
    os.system(f"less ./{folder}/{file}")


def verifyFile(folder: str, file: str):
    """
    Verify if a null-byte is in the shellcode
    ```python
    @return bool : Returns a boolean which is the result of a match of a null-byte shellcode
    ```
    """
    # with open('./' + folder + '/' + file, 'r') as f:
    with open(f"./{folder}/{file}", 'r') as f:
        content = f.read()
    search = re.search(".*\\\\x00.*", str(content))
    if search:
        return False
    return True


def replaceInStr(inputString: str):
    """
    Returns a formatted string
    ```python
    @param str inputString : The string to replace with keywords
    @return list : Returns the formatted string with keywords
    ```
    ---
    For example:
    ```python
    inputString = "mov rax, 5"
    reg = []
    split = ["mov", "rax", "5"]

    # first iteration
    "mov" not in registers
    and not match the regex
    inputString = "mov rax, 5"
    reg = []

    # second iteration
    "rax" is in registers
    replace "rax" by "${VAL1}"
    inputString = "mov ${VAL1}, 5"
    reg = ["rax"]

    # third iteration
    "5" is not in registers
    and match the regex
    replace "5" by "${VAL2}"
    inputString = "mov ${VAL1}, ${VAL2}"
    reg = ["rax" , "5"]

    ```
    """
    reg = []
    inputString = inputString.split(";")[0]
    inputString = inputString.strip()
    split = re.split(r"\, |\,| |\n| \n", inputString)
    returnStr = inputString
    for iterator in range(0, len(split)):
        val = "${{VAL{}}}".format(iterator)
        if split[iterator] in registers:
            returnStr = re.sub(split[iterator], val, returnStr)
            reg.append(split[iterator].strip())
        elif re.search("[0-9]+", split[iterator]):
            returnStr = re.sub(split[iterator], val, returnStr)
            reg.append(split[iterator])
    return [returnStr.strip(), reg]

def generateShellcode(folder:str, file:str):
    file = re.split("\.", file)[0]
    os.system(f"nasm -f elf64 -o ./shellcode/{file}.o ./{folder}/{file}.asm; ld -o ./shellcode/{file}.bin ./shellcode/{file}.o;")
    os.system(f"./functions/shellcode.sh ./shellcode/{file}.bin ./shellcode/{file}.txt")
    os.system(f"rm ./shellcode/*.o ./shellcode/*.bin 2> /dev/null > /dev/null")
