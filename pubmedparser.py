#!/usr/bin/env python
# encoding: utf-8

import sys
import os
from pyparsing import Word, alphas, nums, alphanums, Keyword, OneOrMore, Group, Suppress, OneOrMore, Forward, ZeroOrMore, oneOf, Literal, restOfLine        

def PubMedQueryParser():
    word = Word(alphanums +".-/&§")
    complex_structure = Suppress('"') + Group(OneOrMore(word)) + Suppress('"') + Suppress('[') + Group(OneOrMore(word)) + Suppress(']')
    medium_structure = Group(OneOrMore(word)) + Suppress('[') + Group(OneOrMore(word)) + Suppress(']')
    easy_structure = Group(OneOrMore(word))
    parse_structure = complex_structure | medium_structure | easy_structure
    operators = oneOf("and or", caseless=True).suppress()
    expr = Forward()
    atom = Group(parse_structure) + ZeroOrMore(operators + expr)
    atom2 = Group(Suppress('(') + atom + Suppress(')')) + ZeroOrMore(operators + expr) | atom
    expr << atom2
    return expr
    
if __name__ == "__main__":
    expr = PubMedQueryParser()
    def test(s):
        results = expr.parseString(s)
        print s, '->', results
        
test('("breast neoplasms"[MeSH Terms] OR breast cancer[Acknowledgments] OR breast cancer[Figure/Table Caption] OR breast cancer[Section Title] OR breast cancer[Body - All Words] OR breast cancer[Title] OR breast cancer[Abstract] OR breast cancer[Journal]) AND (prevention[Acknowledgments] OR prevention[Figure/Table Caption] OR prevention[Section Title] OR prevention[Body - All Words] OR prevention[Title] OR prevention[Abstract])')
test('micro[All Fields] AND ("penis"[MeSH Terms] OR penis[Acknowledgments] OR penis[Figure/Table Caption] OR penis[Section Title] OR penis[Body - All Words] OR penis[Title] OR penis[Abstract])')