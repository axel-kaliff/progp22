# Whole program builds a parse-tree for the sequence of tokens

from binarytree import Node
import enum


# TODO Have to rewrite to work with new structure of tokens


# The needed global variables, fix later TODO

global current_index

token_array = [Tokens.DOWN, Tokens.PERIOD, Tokens.REP, Tokens.DECIMAL, Tokens.QUOTE, Tokens.COLOR, Tokens.HEX, Tokens.PERIOD, Tokens.REP, Tokens.DECIMAL, Tokens.QUOTE, Tokens.DOWN, Tokens.PERIOD, Tokens.QUOTE, Tokens.FORW, Tokens.DECIMAL, Tokens.PERIOD, Tokens.QUOTE]

NO_TOKENS = len(token_array)

#### Functions used for parsing ####

def get_next_token():

    global current_index

    current_index += 1
    if current_index == NO_TOKENS:
        print(f"DEBUG current index too high")
        error(fixlater)
    return token_array[current_index]

def peak_next_token():

    return token_array[current_index+1].tokenclass

def expect(expected_token):

    next_token = get_next_token()
    if next_token.tokenclass != expected_token:
        print(f"DEBUG unexpected token, expected {expected_token.tokenclass}, got {next_token}")
        error(next_token.row)
    else:
        return next_token.value

def error(row):

    print(f"Syntaxfel på rad {row}")
    quit()



#### One function for each non-terminal ####

# Returns a reps-node with the number of reps as its left child and the 
# block to repeat as its right child
def reps():

    get_next_token() #Remove the reps-token
    
    node = Node ("reps")
    node.left = Node(expect(TokenClass.DECIMAL))

    expect(TokenClass.QUOTE)

    node.right = block()

    expect(TokenClass.QUOTE)

    return node

# Created a command-node with its numberic value as the left child (no right child)
def command():

    global current_index

    node = None 

    type = get_next_token().tokentype

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
        print(f"DEBUG not correct token for command")
        error(fixlater)

    expect(TokenClass.PERIOD)

    return node



# Returns a block-node with its content as the left child and the next block as the right
def block():

    node = Node("block")

    global current_index
    if current_index < NO_TOKENS-1:
        next_token = peak_next_token()
        if next_token == TokenClass.REP:
            node.left = reps()
        elif next_token == TokenClass.QUOTE:
            return node
        else:
            node.left = command()

        node.right = block()

    return node
    


def main():

    global current_index
    current_index = -1
    root = block()
    print(root)



if __name__=="__main__":

    main()
