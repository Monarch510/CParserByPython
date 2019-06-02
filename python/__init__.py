# -------------------------------
# -*- coding: utf-8 -*- 
# @Time : 2019/5/13 16:27 
# @Author : monarch
# @Site :  
# @File : __init__.py.py 
# @Software: PyCharm
# -------------------------------
from antlr4 import FileStream, CommonTokenStream

from python.MyVisitor import MyVisitor
from python.cGrammer.CLexer import CLexer
from python.cGrammer.CParser import CParser


def translate_c():
    file = 'D:\source\python\\translatorSystem\\resources\cFile\\hello.c'
    inputs = FileStream(file)
    lexer = CLexer(inputs)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.compilationUnit()
    mv = MyVisitor()
    mv.visit(tree)
    for x in mv.prolog_list.keys():
        prolog = mv.prolog_list[x]
        prolog.toString()


if __name__=="__main__":
    translate_c()