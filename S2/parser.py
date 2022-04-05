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
   LEFT = 12

def main():

    tokens = []
    
    with open('data.txt') as f:
         
        buffer = "" 
        last_c = ""
        numBuffer = ""
        hexBuffer = ""
        commentLine = False
        
        while True:
             
            # Read from file
            c = f.read(1)
               
            # detect comment
            if c == "%":
                commentLine = True

            if commentLine:
                if c == "\n":
                     commentLine = False
                     continue
                else: 
                     continue
                    



            # all whitespace is equal
            if "\n" in c or "\t" in c:
                c = " "

            if c == " " and last_c == ".":
                c == ""

            if last_c == "." and (" " in c or "\n" in c or "\t" in c):
                buffer = ""
                

           

            # does not add repeating whitespace or whitespace after period
            if not ((last_c == " ") and (c == " ")) or not (last_c == "." and c == " "):
                buffer = buffer + c
                

            # check if buffer matches any tokens
            if buffer == ".":

                if not numBuffer == "":
                    tokens.append(Tokens.DECIMAL)
                    numBuffer = ""
                if not hexBuffer == "":
                    tokens.append(Tokens.HEX)
                    hexBuffer = ""

                tokens.append(Tokens.PERIOD)
                buffer = ""

            if buffer == "FORW " or buffer == " FORW ":
                tokens.append(Tokens.FORW)
                buffer = ""

            if buffer == "LEFT " or buffer == " LEFT ":
                tokens.append(Tokens.LEFT)
                buffer = ""

            if buffer == "RIGHT " or buffer == " RIGHT ":
                tokens.append(Tokens.RIGHT)
                buffer = ""


            if buffer == "BACK " or buffer == " BACK ":
                tokens.append(Tokens.BACK)
                buffer = ""

            if buffer.strip() == "UP":
                tokens.append(Tokens.UP)
                buffer = ""

            if buffer == "DOWN":
                tokens.append(Tokens.DOWN)
                buffer = ""

            if c.isnumeric():
                numBuffer = numBuffer + c
                buffer = ""

            # TODO hex
            



            # if there has been some sort of command
            if (c == " " or c == "\n") and not (buffer == "" or buffer == " " or buffer == "\n"):
                # if there's a whitespace after something that wasn't a command (becuase the buffer would have been reset if it was)

                # might have been a number or hex

                if not numBuffer == "" and not c.isnumeric():
                    tokens.append(Tokens.DECIMAL)
                    numBuffer = ""

                # TODO hex
                else:
                    print("e: ")
                    print("'" + buffer + "'")

                    tokens.append(Tokens.ERROR)
                    buffer = ""

            last_c = c
            if not c:
                break
         
    # print(tokens)
    print("##################################")
    for token in tokens:
        print(token)
        print(" ")

if __name__=="__main__":
    main()

