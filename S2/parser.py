#!/usr/bin/env python
# -*- coding: utf-8 -*-

import enum
# Using enum class create enumerations
class Tokens(enum.Enum):
   ERROR = 0
   FORW = 1
   BACK = 2
   RIGHT = 3
   DOWN = 4
   UP = 5
   COLOR = 6
   REP = 7
   PERIOD = 8
   QUOTE = 9
   DECIMAL = 10
   HEX = 11

def main():

    tokens = []
    
    with open('data.txt') as f:
         
        buffer = "" 
        last_c = ""
        
        while True:
             
            # Read from file
            c = f.read(1)

               
            # new line works as space
            if c == "\n":
                c = " "

            
            # does not add repeating whitespace
            if not ((last_c == " ") and (c == " ")):
                
                buffer = buffer + c
                

            # check if buffer matches any tokens
            if buffer == ".":
                tokens.append(Tokens.PERIOD)
                buffer = ""

            if buffer == "FORW ":
                tokens.append(Tokens.FORW)
                buffer = ""

            if buffer == "BACK ":
                tokens.append(Tokens.FORW)
                buffer = ""

            if buffer.strip() == "UP":
                tokens.append(Tokens.UP)
                buffer = ""

            if buffer == "DOWN":
                tokens.append(Tokens.DOWN)
                buffer = ""

            # TODO decimal


            # TODO hex



            # if there has been some sort of command
            if (c == " " or c == "\n") and not (buffer == "" or buffer == " " or buffer == "\n"):
                tokens.append(Tokens.ERROR)
                buffer = ""



            last_c = c
            if not c:
                break
         
                # print the character
                print("b")
                print(buffer)
                print(tokens)
    print(tokens)

if __name__=="__main__":
    main()
