# -------------------------------
# -*- coding: utf-8 -*- 
# @Time : 2019/5/17 15:07 
# @Author : monarch
# @Site :  
# @File : Prolog.py 
# @Software: PyCharm
# -------------------------------


class Prolog(object):

    def __init__(self, name, id, value, father_id, children_id=set(), ):
        self.name = name
        self.id = id
        self.value = value
        self.father_id = father_id
        self.children_id = children_id

    def toString(self):
        print('%s(%d,%d,[' %
              (self.name, self.id, self.father_id), end='')
        while self.children_id.__len__() > 1:
            print('%d,' % self.children_id.pop(), end='')
        if self.children_id.__len__() == 1:
            print('%d' % self.children_id.pop(), end='')
        print('],\'%s\').'% self.value)

    def getChildrenCount(self):
       return self.children_id.__len__()

