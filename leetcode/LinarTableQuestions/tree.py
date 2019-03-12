#encoding=utf-8
import os
from os.path import isdir, isfile

def list_sub_dir(dir):
    return filter(lambda i: isdir(i), [dir+x for x in os.listdir(dir)])

def list_sub_file(dir):
    return filter(lambda i: isfile(i), [dir+x for x in os.listdir(dir)])

'''print dirs & files like tree commnad in linux'''
def tree(dir, count=0):
    files = list_sub_file(dir)
    dirs = list_sub_dir(dir)
    
    for i in files:
        print('    '*count + i)
        
    #关键在于:要记一个变量来表明当前是在递归的第几层!并利用python的默认值写法来逐层加1!
    for j in dirs:
        print('    '*count + j)
        tree(j+'/', count=count+1)

tree('/tmp/d/')
