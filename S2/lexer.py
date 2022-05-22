from tokenprogp import Token
from tokenclass import TokenClass
import re

class Lexer:
    c = ""
    buffer = ""
    tokens = []
    numBuffer = ""
    row = 1
    needBreak = False
    last_c = ""
    hexActive= False
    commentLine = False
    whitespace = False
    lastWhitespace = False
    result = None


    def addToken(self, tokenClass, number):
        self.result = tokenClass
        if number:
               self.tokens.append(Token(tokenClass, self.row, self.numBuffer))
               self.numBuffer = ""
        else:
            if self.numBuffer:
                self.numBuffer= ""
                self.tokens.append(Token(TokenClass.ERROR, self.row, self.buffer))
            else:
                self.tokens.append(Token(tokenClass, self.row, self.buffer))
            self.buffer = ""

    def checkBufferForToken(self):
            print(self.buffer)

            if re.findall(r'^([\s])*FORW([\s])+$', self.buffer):
                self.addToken(TokenClass.FORW, False)
            if re.findall(r'^([\s])*BACK([\s])+$', self.buffer):
                self.addToken(TokenClass.BACK, False)
            if re.findall(r'^([\s])*LEFT([\s])+$', self.buffer):
                self.addToken(TokenClass.LEFT, False)
            if re.findall(r'^([\s])*RIGHT([\s])+$', self.buffer):
                self.addToken(TokenClass.RIGHT, False)
            if re.findall(r'^([\s])*COLOR([\s])+$', self.buffer):
                self.addToken(TokenClass.COLOR, False)
            if re.findall(r'^([\s])*UP([\s])*$', self.buffer):
                self.addToken(TokenClass.UP, False)
            if re.findall(r'^([\s])*DOWN([\s])*$', self.buffer):
                self.addToken(TokenClass.DOWN, False)

            if re.findall(r'^([\s])*[0-9][0-9]*$', self.buffer):
                if len(self.buffer) > 6:
                    self.addToken(TokenClass.ERROR, False)
                else:
                    self.numBuffer = self.numBuffer + self.c
                    self.buffer = ""

            # dot
            if re.findall(r'^([\s])*(\.)$', self.buffer):
                if self.numBuffer:
                    self.addToken(TokenClass.DECIMAL, True)
                self.addToken(TokenClass.PERIOD, False)

            #citation
            if re.findall(r'([\s])*\"', self.buffer):
                self.addToken(TokenClass.QUOTE, False)

            #rep
            if re.findall(r'([\s])*REP([\s])+', self.buffer):
                self.addToken(TokenClass.REP, False)

            #hexmatch
            if re.findall("^#([A-Fa-f0-9]{6})$", self.buffer):
                self.addToken(TokenClass.HEX, False)


    def handleComments(self):
            if self.c == "%":
                self.commentLine = True
                self.row = self.row + 1

            if self.commentLine:
                if self.c == "\n":
                    self.commentLine = False
                    self.buffer = self.buffer + " "
                    self.checkBufferForToken()
                    self.handleWhitespace()
                    return True
                else:
                    return True

    def handleWhitespace(self):
        if not self.result:
            if re.findall(r'^([\s])+$', self.buffer):
                if self.numBuffer:
                    self.addToken(TokenClass.DECIMAL, True)
            else:
                if re.findall(r'^([\s])+$', self.c):
                    self.addToken(TokenClass.ERROR, False)

    def tokenize(self, text):

        idx = 0

        while idx < len(text):
           self.c = text[idx]
           idx = idx+1

           if self.handleComments():
                continue
           else:
               self.buffer = self.buffer + self.c


           self.result = None
           self.checkBufferForToken()
           self.handleWhitespace()

           if not self.c:
                break

        return self.tokens


