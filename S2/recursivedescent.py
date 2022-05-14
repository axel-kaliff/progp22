# Whole program builds a parse-tree for the sequence of tokens

#from parser import Lexer, Token, TokenClass
#from parser import Lexer
#from parser import TokenClass
#from parser import Token
from leona import Leona
from node import Node
from tokenprogp import Token
from tokenclass import TokenClass
from lexer import Lexer

import sys
import enum
import re


class RecursiveDescent:


    def __init__(self, array):
        self.token_array = array
        self.NO_TOKENS = len(array)

        self.current_index = -1

    #### Functions used for parsing ####

    def get_next_token(self):

        self.current_index += 1
        if self.current_index == self.NO_TOKENS:
            error(self.token_array[self.current_index-1].row)

        return self.token_array[self.current_index]

    def peek_next_token(self):

        return self.token_array[self.current_index+1].tokenclass

    def expect(self, expected_token):

        next_token = self.get_next_token()
        if next_token.tokenclass != expected_token:
            error(next_token.row)
        else:
            return next_token.value

    def error(self, row):

        sys.stdout.write(f"Syntaxfel på rad {row} \n")
        quit()



    #### Functions for all non-terminals ####

    # Returns a reps-node with the number of reps as its left child and the 
    # block to repeat as its right child
    def reps(self):

        self.get_next_token() #Remove the reps-token
        node = Node("reps")
        
        node.left = Node(self.expect(TokenClass.DECIMAL))

        
        next_token = self.peek_next_token()

        if next_token == TokenClass.REP:
            node.right = self.reps()
        elif next_token == TokenClass.QUOTE:
            self.get_next_token() 

            node.right = self.block()

            self.expect(TokenClass.QUOTE)
        else:
            node.right = self.command()

        return node

    # Created a command-node with its numberic value as the left child (no right child)
    def command(self):

        node = None 

        next_token = self.get_next_token()
        type = next_token.tokenclass

        if type == TokenClass.FORW:
            node = Node("forw")
            node.left = Node(self.expect(TokenClass.DECIMAL))
        elif type == TokenClass.BACK:
            node = Node("back")
            node.left = Node(self.expect(TokenClass.DECIMAL))
        elif type == TokenClass.LEFT:
            node = Node("left")
            node.left = Node(self.expect(TokenClass.DECIMAL))
        elif type == TokenClass.RIGHT:
            node = Node("right")
            node.left = Node(self.expect(TokenClass.DECIMAL))
        elif type == TokenClass.DOWN:
            node = Node("down")
        elif type == TokenClass.UP:
            node = Node("up")
        elif type == TokenClass.COLOR:
            node = Node("color")
            node.left = Node(self.expect(TokenClass.HEX))
        else:
            self.error(next_token.row)

        self.expect(TokenClass.PERIOD)

        return node



    # Returns a block-node with its content as the left child and the next block as the right
    def block(self):

        node = Node("block")

        if self.current_index < self.NO_TOKENS-1:
            next_token = self.peek_next_token()
            if next_token == TokenClass.REP:
                node.left = self.reps()
            elif next_token == TokenClass.QUOTE:
                return node
            elif next_token == TokenClass.ERROR:
                self.error(get_next_token().row)
            else:
                node.left = self.command()

            node.right = self.block()

        return node
        


def main():

    input_lines = [] 

    for line in sys.stdin:
        input_lines.append(line)



    input_text = ''.join(input_lines)

    token_array = Lexer.tokenize(input_text)

    rd = RecursiveDescent(token_array)
    root = rd.block()

    leona = Leona()
    leona.read_node(root)


main()

