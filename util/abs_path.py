#!/usr/bin/env python3
import os
from sys import argv

def reactified(path):
    direc = []
    nodes = path.split("/")

    nodes = nodes[1:]
    for node in nodes:
        if(node=='.'): continue
        elif(node=='..'):direc.pop()
        else: direc.append(node)

    path = ""
    for item in direc:
        path = path + "/"
        path = path + item

    return path


'''
takes relative path as string argument as a path in linux
returns absolute path without '/' at end
means it will write /home/srb instead of /home/srb/
'''
def abs_path(path):
    pwd = str(os.getcwd())#always return without / at end;
    home_path = os.getenv("HOME")#always return without / at end

    if(len(path)>1 and path[-1]=='/'):#remove last backslash
        path=path[:-1]
    if(path[0]=='/'):
        return reactified(path)
    if(path[0]=='~'):
        return reactified(home_path + path[1:])
    if(path[0]!='.'):
        return reactified(pwd + '/' + path)


    return reactified(pwd +'/'+ path)

help1 = "require 1 argument as path name to be made absolute"
if(__name__=="__main__"):
    if(len(argv)!=2):
        print(help1)
        exit()
    print(abs_path(argv[1]))
