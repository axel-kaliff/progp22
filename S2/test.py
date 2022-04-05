#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parser import Lexer, Token, TokenClass

l = Lexer()


for token in Lexer.tokenize("data.txt"):
    print(token.row)
    print(token.value)
    print("\n")
