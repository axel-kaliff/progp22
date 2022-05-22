import re
from tokenprogp import Token
from tokenclass import TokenClass


class Lexer:
    c = ""
    buffer = ""
    tokens = []
    numBuffer = ""
    row = 1
    needBreak = False
    last_c = ""
    hexActive = False
    commentLine = False
    whitespace = False
    lastWhitespace = False
    result = None

    def addToken(self, tokenClass, number):
        self.result = tokenClass
        if number:
            if self.numBuffer[:1] == "0":
                self.tokens.append(Token(TokenClass.ERROR, self.row, self.numBuffer))
            else:
                self.tokens.append(Token(tokenClass, self.row, self.numBuffer))
            self.numBuffer = ""
        else:
            if self.numBuffer:
                self.numBuffer = ""
                self.tokens.append(Token(TokenClass.ERROR, self.row, self.buffer))
            else:
                self.tokens.append(Token(tokenClass, self.row, self.buffer))
            self.buffer = ""

    def checkBufferForToken(self):

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

        # hexmatch
        if re.findall(r"^([\s])*#([A-Fa-f0-9]{6})$", self.buffer):
            self.addToken(TokenClass.HEX, False)

        if re.findall(r'^([\s])*[0-9][0-9]*$', self.buffer):
            if len(self.buffer) > 7:
                self.addToken(TokenClass.ERROR, False)
            else:
                self.numBuffer = self.numBuffer + self.c
                self.buffer = ""

        # dot
        if re.findall(r'^([\s])*(\.)$', self.buffer):
            if self.numBuffer:
                self.addToken(TokenClass.DECIMAL, True)
            self.addToken(TokenClass.PERIOD, False)

        # citation
        if re.findall(r'([\s])*\"', self.buffer):
            self.addToken(TokenClass.QUOTE, False)

        # rep
        if re.findall(r'([\s])*REP([\s])+', self.buffer):
            self.addToken(TokenClass.REP, False)

    def handleComments(self):
        if self.c == "%":
            self.commentLine = True

        if self.commentLine:
            if self.c == "\n":
                #self.buffer = self.buffer + " "
                #self.checkBufferForToken()
                #self.handleWhitespace()
#                print('%s buffer from comment' % self.buffer)
                #self.row = self.row + 1
                #self.buffer = ""
                self.commentLine = False
                return True
            else:
                return True
        return False

    def handleWhitespace(self):
        if not self.result:
            if re.findall(r'^([\s])+$', self.buffer):
                if self.numBuffer:
                    self.addToken(TokenClass.DECIMAL, True)
            else:
                if re.findall(r'^([\s])+$', self.c) and not re.findall(r'^([\s])+$', self.buffer):
                    self.addToken(TokenClass.ERROR, False)

    def tokenize(self, text):

        idx = 0

        while idx < len(text):
            self.c = text[idx]
            idx = idx + 1

            self.c = self.c.upper()
            #if not self.handleComments():
                #if self.c == "\n":
                #    print('%s buffer' % self.buffer)
                #    if not self.commentLine:
                #        self.row = self.row + 1
            #    self.buffer = self.buffer + self.c

            self.handleComments()

            if self.c == "\n":
                if not re.findall(r'^([\s])+$', self.buffer):
                    #                   print("buffer: '%s' at %s" % (self.buffer, self.row))
                    self.buffer = self.buffer + " "
                    self.checkBufferForToken()
                    self.handleWhitespace()
                self.row = self.row + 1


            if not self.commentLine:
                self.buffer = self.buffer + self.c
                self.result = None
                self.checkBufferForToken()
                self.handleWhitespace()

            if len(self.buffer.strip()) > 7:
                #print(self.buffer)
                self.addToken(TokenClass.ERROR, False)

            if not self.c:
                break

#        for token in self.tokens:
#            print("%s: %s || %s" % (token.row, token.tokenclass, token.value))
        return self.tokens
