#!/usr/bin/env python3
from functions.functions import *;

print("Welcome to the Polymorphic Shellcode Tool from the Cebago TEAM")

quit = False
choice = 0

while not quit:
    print("What do you want to do ?")
    print("1- Polymorph a file")
    print("2- See a polymorphed file")
    print("3- Generate the shellcode")
    print("4- Verify a shellcode")
    print("5- Quit")
    
    choice = input("choice: ")
    
    if choice == "1":
        print("\n\n\n=====Polymorph File=====")
        print("Which file do you want to polymorph ?")
        file = selectFile("input")
        if file != False:
            readAsm(file)
            print(f"Polymorphed file generated in 'shellcode/{file}'")
        print("=====End Polymorph File=====\n\n\n")
    elif choice == "2":
        print("\n\n\n=====See Assembly File=====")
        print("Which file do you want to see ?")
        file = selectFile("output")
        if file != False:
            displayFile("output", file)
            print("goToFunction")
        print("=====End See Assembly File=====\n\n\n")
    elif choice == "3":
        print("\n\n\n=====Generate Shellcode=====")
        folder = chooseFolder()
        if folder != False:
            print("Which file do you want to generate shellcode from :")
            file = selectFile(folder)
            if file != False:
                generateShellcode(folder, file)
        print("=====End Generate Shellcode=====\n\n\n")
    elif choice == "4":
        print("\n\n\n=====Shellcode scanner=====")
        print("Which file do you want to scan ?")
        file = selectFile("shellcode")
        if file != False:
            if verifyFile("shellcode", file):
                print("No null bytes detected")
            else:
                print("OhOh! A null byte was found")
        print("=====End Shellcode scanner=====\n\n\n")
    elif choice == "5":
        quit = True
    else:
        print("Bad choice")
