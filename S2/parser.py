#!/usr/bin/env python
# -*- coding: utf-8 -*-

import enum
import re
 # Using enum class create enumerations
class TokenClass(enum.Enum):
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

class Token:
    def __init__(self, tokenclass, row, value):
        self.tokenclass = tokenclass
        self.row = row
        self.value = value

class Lexer:

    def tokenize(text):
        tokens = []
             
        buffer = "" 
        last_c = ""
        numBuffer = ""
        hexActive= False
        commentLine = False
        row = 1

        idx = 0
        
        while idx < len(text):
             
            # Read from file
            c = text[idx]
            idx = idx+1
               
            # detect comment
            if c == "%":
                commentLine = True
                row = row + 1

            if commentLine:
                if c == "\n":
                     commentLine = False
                     continue
                else: 
                    continue
                    


            if c == "\n":
                row = row + 1

            # all whitespace is equal
            if "\n" in c or "\t" in c:
                c = " "

            if c == " " and last_c == ".":
                # TODO should this be continue?
                continue
                # c == ""

            if last_c == "." and (" " in c or "\n" in c or "\t" in c):
                buffer = ""
                

           

            # does not add repeating whitespace or whitespace after period
            # TODO it still adds redundant whitespaces
            if not ((last_c == " ") and (c == " ")) and not (last_c == "." and c == " "):
                buffer = buffer + c
                

            # check if buffer matches any tokens
            if buffer == "." or buffer == " .":

                if not numBuffer == "":
                    tokens.append(Token(TokenClass.DECIMAL, row, numBuffer))
                    numBuffer = ""

                tokens.append(Token(TokenClass.PERIOD, row, buffer))
                buffer = ""

            if buffer == "FORW " or buffer == " FORW ":
                tokens.append(Token(TokenClass.FORW, row, buffer))
                buffer = ""

            if buffer == "\"" or buffer == " \"":
                if not numBuffer == "":
                    tokens.append(Token(TokenClass.DECIMAL, row, numBuffer))
                    numBuffer = ""


                tokens.append(Token(TokenClass.QUOTE, row, buffer))
                buffer = ""
                
            if buffer == "REP " or buffer == " REP ":
                tokens.append(Token(TokenClass.REP, row, buffer))
                buffer = ""




            if buffer == "LEFT " or buffer == " LEFT ":
                tokens.append(Token(TokenClass.LEFT, row, buffer))
                buffer = ""

            if buffer == "RIGHT " or buffer == " RIGHT ":
                tokens.append(Token(TokenClass.RIGHT, row, buffer))
                buffer = ""

            if buffer == "COLOR " or buffer == " COLOR ":
                tokens.append(Token(TokenClass.COLOR, row, buffer))
                buffer = ""

            if buffer == "BACK " or buffer == " BACK ":
                tokens.append(Token(TokenClass.BACK, row, buffer))
                buffer = ""

            if buffer.strip() == "UP":
                tokens.append(Token(TokenClass.UP, row, buffer))
                buffer = ""

            if buffer == "DOWN":
                tokens.append(Token(TokenClass.DOWN, row, buffer))
                buffer = ""

            if buffer== "#":
                hexActive = True

            if re.findall("^#([A-Fa-f0-9]{6})", buffer):
                tokens.append(Token(TokenClass.HEX, row, buffer))
                hexActive = False
                buffer = ""

            elif c.isnumeric() and not hexActive:
                numBuffer = numBuffer + c
                buffer = ""

        


            if not (buffer == "" or buffer == " ") and not numBuffer == "":
                tokens.append(Token(TokenClass.DECIMAL, row, numBuffer))
                numBuffer = ""



            # if there has been some sort of command
            if c == " " and not (buffer == "" or buffer == " "):
                # if there's a whitespace after something that wasn't a command (becuase the buffer would have been reset if it was)

                if not numBuffer == "":
                    tokens.append(Token(TokenClass.DECIMAL, row, numBuffer))
                    numBuffer = ""

                # TODO hex
                else:
                    tokens.append(Token(TokenClass.ERROR, row, buffer))
                    buffer = ""

            last_c = c
            if not c:
                break
         
        # print(tokens)
        return tokens



