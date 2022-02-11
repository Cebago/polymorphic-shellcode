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
    print("4- Quit")
    
    choice = input("choice: ")
    
    if choice == "1":
        print("\n\n\n=====Polymorph File=====")
        print("Which file do you want to polymorph ?")
        file = selectFile("input")
        if file != False:
            #goToFunction
            print("goToFunction")
        print("=====End Polymorph File=====\n\n\n")
    elif choice == "2":
        print("See")
    elif choice == "3":
        print("Generated")
    elif choice == "4":
        quit = True
    else:
        print("Bad choice")
