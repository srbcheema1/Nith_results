#!/usr/bin/env python3

import argparse
import json
import sys
from sys import argv, exit

from util.getter import get_year, get_branch, get_year, get_branch, get_branch_name
from util.limits import default_no_of_std, iiitu_no_of_std, dual_no_of_std, base_year, get_class_set, debug
from util.srbjson import extract_data, dump_data
from util.string_constants import cache_path
from util.student import Student


from srblib import abs_path
from srblib import Colour
from srblib import SrbJson
from srblib import verify_folder

def sort_sgpa(std):
    return float(std.sgpa)
def sort_cgpa(std):
    return float(std.cgpa)


def get_data(roll):
    cache = SrbJson(cache_path,template={"nith_results":{}}) # load cache
    data=[]
    temp = roll[:-2]
    a,b = 1,default_no_of_std
    if(roll[0]=='i'):
        b=iiitu_no_of_std
    if(roll[2]=='m'):
        b=dual_no_of_std

    for i in range(a,b):
        roll = temp
        roll += "%02d"%(i)
        Colour.print('Extracting '+roll,Colour.GREEN)
        if(roll in cache):
            item = cache[roll]
            std = Student(item['Rollno'])
            std.cached_data(item['Name'],item['Gender'],item['Sgpa'],item['Cgpa'],item['Points'])
            if(std.name!='-' and std.cgpa!='0'):
                data.append(std)
                Colour.print('got chached '+roll,Colour.BLUE)
            else:
                Colour.print('Bad chached '+roll,Colour.BLUE)
        else:
            std = Student(roll)
            std.fetch_data()
            if(std.name!='-' and std.cgpa!='0'):
                data.append(std)
                cache[std.roll_num] = std.get_cache()

    return data


def print_data(data):
    rank = 1
    for item in data:
        print(rank,end=" ")
        print(item.get_result())
        print()
        rank +=1

def full_class(roll):
    data=[]
    data.extend(get_data(roll))
    print_data(data)

    save_stdout = sys.stdout
    branch_name = get_branch_name(get_branch(roll))
    verify_folder(abs_path('./result/text/'+branch_name))

    data.sort(key=sort_sgpa,reverse=True)
    sys.stdout = open('result/text/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_sgpi.txt','w')
    print("sorting by sgpi....\n\n\n")
    print_data(data)
    dump_data(data,'result/json/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_sgpi.json')

    data.sort(key=sort_cgpa,reverse=True)
    sys.stdout = open('result/text/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_cgpi.txt','w')
    print("sorting by cgpi....\n\n\n")
    print_data(data)
    dump_data(data,'result/json/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_cgpi.json')

    sys.stdout = save_stdout
    print("written into files in result folder....\n\n")


def full_year(roll):
    data=[]
    y = get_year(roll)
    classes = get_class_set(y)
    verify_folder(abs_path('./result'))
    save_stdout = sys.stdout

    for roll in classes:
        class_data = get_data(roll)
        branch_name = get_branch_name(get_branch(roll))
        verify_folder(abs_path('./result/text/'+branch_name))

        class_data.sort(key=sort_sgpa,reverse=True)
        sys.stdout = open('result/text/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_sgpi.txt','w')
        print("sorting by sgpi....\n\n\n")
        print_data(class_data)
        dump_data(class_data,'result/json/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_sgpi.json')

        class_data.sort(key=sort_cgpa,reverse=True)
        sys.stdout = open('result/text/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_cgpi.txt','w')
        print("sorting by cgpi....\n\n\n")
        print_data(class_data)
        dump_data(class_data,'result/json/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_cgpi.json')

        data.extend(class_data)
        sys.stdout = save_stdout

    verify_folder(abs_path('./result/text/FULL_YEAR'))
    data.sort(key=sort_sgpa,reverse=True)
    sys.stdout = open('result/text/FULL_YEAR/full_year_'+get_year(roll)+'_sgpi.txt','w')
    print("sorting by sgpi....\n\n\n")
    print_data(data)
    dump_data(data,'result/json/FULL_YEAR/full_year_'+get_year(roll)+'_sgpi.json')

    data.sort(key=sort_cgpa,reverse=True)
    sys.stdout = open('result/text/FULL_YEAR/full_year_'+get_year(roll)+'_cgpi.txt','w')
    print("sorting by cgpi....\n\n\n")
    print_data(data)
    dump_data(data,'result/json/FULL_YEAR/full_year_'+get_year(roll)+'_cgpi.json')

    sys.stdout = save_stdout
    print("written into files in result folder....\n\n")

def full_college():
    data=[]
    by = base_year # prefix of first year
    roll_set = []
    for b in range(0,4):
        roll_set.append(str(by-b)+'mi535')
    save_stdout = sys.stdout

    for roll in roll_set:
        year_data=[]
        y = get_year(roll)
        classes = get_class_set(y)

        for roll in classes:
            class_data = get_data(roll)
            branch_name = get_branch_name(get_branch(roll))
            verify_folder(abs_path('./result/text/'+branch_name))

            class_data.sort(key=sort_sgpa,reverse=True)
            sys.stdout = open('result/text/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_sgpi.txt','w')
            print("sorting by sgpi....\n\n\n")
            print_data(class_data)
            dump_data(class_data,'result/json/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_sgpi.json')

            class_data.sort(key=sort_cgpa,reverse=True)
            sys.stdout = open('result/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_cgpi.txt','w')
            print("sorting by cgpi....\n\n\n")
            print_data(class_data)
            dump_data(class_data,'result/json/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_cgpi.json')

            year_data.extend(class_data)
            sys.stdout = save_stdout

        verify_folder(abs_path('./result/text/FULL_YEAR'))

        year_data.sort(key=sort_sgpa,reverse=True)
        sys.stdout = open('result/text/FULL_YEAR/full_year_'+get_year(roll)+'_sgpi.txt','w')
        print("sorting by sgpi....\n\n\n")
        print_data(year_data)
        dump_data(year_data,'result/json/FULL_YEAR/full_year_'+get_year(roll)+'_sgpi.json')

        year_data.sort(key=sort_cgpa,reverse=True)
        sys.stdout = open('result/text/FULL_YEAR/full_year_'+get_year(roll)+'_cgpi.txt','w')
        print("sorting by cgpi....\n\n\n")
        print_data(year_data)
        dump_data(year_data,'result/json/FULL_YEAR/full_year_'+get_year(roll)+'_cgpi.json')

        sys.stdout = save_stdout
        data.extend(year_data)

    verify_folder(abs_path('./result/text/FULL_COLLEGE'))
    data.sort(key=sort_sgpa,reverse=True)
    sys.stdout = open('result/text/FULL_COLLEGE/full_college_sgpi.txt','w')
    print("sorting by sgpi....\n\n\n")
    print_data(data)
    dump_data(data,'result/text/FULL_COLLEGE/full_college_sgpi.json')

    data.sort(key=sort_cgpa,reverse=True)
    sys.stdout = open('result/text/FULL_COLLEGE/full_college_cgpi.txt','w')
    print("sorting by cgpi....\n\n\n")
    print_data(data)
    dump_data(data,'result/text/FULL_COLLEGE/full_college_cgpi.json')

    sys.stdout = save_stdout
    print("written into files in result folder....\n\n")


if(__name__=="__main__"):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-b", "--branch", action="store_true", help="full result of your branch")
    group.add_argument("-y", "--year", action="store_true", help="full result of your year")
    group.add_argument("-a", "--all", action="store_true", help="full result of college")
    parser.add_argument("roll",nargs=1,help="your roll number")
    args = parser.parse_args()

    roll = args.roll[0].lower()
    std = Student(roll)
    std.fetch_data()
    print(std.get_result())

    try:
        if(args.branch):
            full_class(roll)
        if(args.year):
            full_year(roll)
        if(args.all):
            full_college()
    except KeyboardInterrupt:
        Colour.print('Exiting on KeyboardInterrupt ...',Colour.YELLOW)
    Colour.print('A script by srbcheema1',Colour.PURPLE)
