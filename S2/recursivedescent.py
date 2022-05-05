# Whole program builds a parse-tree for the sequence of tokens

from parser import Lexer, Token, TokenClass
from leona import Leona
from node import Node

import sys


# TODO Have to rewrite to work with new structure of tokens


# The needed global variables, fix later TODO

FILE_PATH = "./data.txt"

global current_index
global token_array
global NO_TOKENS


#### Functions used for parsing ####

def get_next_token():

    global current_index

    current_index += 1
    if current_index == NO_TOKENS:
#        print(f"DEBUG current index too high")
        error(token_array[current_index-1].row)

#    print(f" ")
#    print(f"DEBUG tokenclass = {token_array[current_index].tokenclass}")
#    print(f"DEBUG value = {token_array[current_index].value}")
#    print(f"DEBUG row = {token_array[current_index].row}")
    return token_array[current_index]

def peek_next_token():

    return token_array[current_index+1].tokenclass

def expect(expected_token):

    next_token = get_next_token()
    if next_token.tokenclass != expected_token:
#        print(f"DEBUG unexpected token, expected {expected_token}, got {next_token.tokenclass}")
#        print(f"DEBUG value: {next_token.value}")
        error(next_token.row)
    else:
        return next_token.value

def error(row):

    sys.stdout.write(f"Syntaxfel på rad {row} \n")
    quit()



#### Functions for all non-terminals ####

# Returns a reps-node with the number of reps as its left child and the 
# block to repeat as its right child
def reps():

    get_next_token() #Remove the reps-token
    node = Node("reps")
    
    node.left = Node(expect(TokenClass.DECIMAL))

    
    next_token = peek_next_token()

    if next_token == TokenClass.REP:
        node.right = reps()
    elif next_token == TokenClass.QUOTE:
        get_next_token() 

        node.right = block()

        expect(TokenClass.QUOTE)
    else:
        node.right = command()

    return node

# Created a command-node with its numberic value as the left child (no right child)
def command():

    global current_index

    node = None 

    next_token = get_next_token()
    type = next_token.tokenclass

    if type == TokenClass.FORW:
        node = Node("forw")
        node.left = Node(expect(TokenClass.DECIMAL))
    elif type == TokenClass.BACK:
        node = Node("back")
        node.left = Node(expect(TokenClass.DECIMAL))
    elif type == TokenClass.LEFT:
        node = Node("left")
        node.left = Node(expect(TokenClass.DECIMAL))
    elif type == TokenClass.RIGHT:
        node = Node("right")
        node.left = Node(expect(TokenClass.DECIMAL))
    elif type == TokenClass.DOWN:
        node = Node("down")
    elif type == TokenClass.UP:
        node = Node("up")
    elif type == TokenClass.COLOR:
        node = Node("color")
        node.left = Node(expect(TokenClass.HEX))
    else:
#        print(f"DEBUG not correct token for command")
#        print(f"DEBUG current token: {type}")
#        print(f"DEBUG current token value: {next_token.value}")
        error(next_token.row)

    expect(TokenClass.PERIOD)

    return node



# Returns a block-node with its content as the left child and the next block as the right
def block():

    node = Node("block")

    global current_index
    if current_index < NO_TOKENS-1:
        next_token = peek_next_token()
        if next_token == TokenClass.REP:
            node.left = reps()
        elif next_token == TokenClass.QUOTE:
            return node
        elif next_token == TokenClass.ERROR:
#            print(f"DEBUG found error-token")
            error(get_next_token().row)
        else:
            node.left = command()

        node.right = block()

    return node
    


def main():

    global current_index
    global token_array
    global NO_TOKENS

    current_index = -1

    input_lines = [] #TODO fix this shit

    for line in sys.stdin:
        input_lines.append(line)

    input_text = ''.join(input_lines)
#    print(input_text)
    token_array = Lexer.tokenize(input_text)
    NO_TOKENS = len(token_array)

    root = block()
#    print(root)

    leona = Leona()
    leona.read_node(root)


if __name__=="__main__":

    main()
