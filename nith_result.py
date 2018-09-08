#!/usr/bin/env python3

import argparse
import json
import sys
from sys import argv, exit

from util.abs_path import abs_path
from util.getter import get_year, get_branch, get_year, get_branch, get_branch_name
from util.limits import default_no_of_std, iiitu_no_of_std, dual_no_of_std, base_year, get_class_set, debug
from util.srbColour import Colour
from util.srbjson import extract_data, dump_data
from util.string_constants import default_file_name
from util.student import Student
from util.files import verify_folder


# dump switches
dump_it = False


def sort_sgpa(std):
    return float(std.sgpa)
def sort_cgpa(std):
    return float(std.cgpa)

std_map = {}
def create_std_map(file_name=default_file_name):
    if(debug): print("created map "+file_name)
    data = extract_data(file_name)
    data = data['Students']
    global std_map
    for item in data:
        std = Student(item['Rollno'])
        std.cached_data(item['Name'],item['Gender'],item['Sgpa'] \
            ,item['Cgpa'],item['Points'],item['Rank'],item['G_rank'])
        std_map[item['Rollno']] = std


def get_data(roll):
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
        print(Colour.GREEN+'Extracting '+roll+Colour.END)
        if(roll in std_map):
            std = std_map[roll]
            if(std.name!='-' and std.cgpa!='0'):
                data.append(std)
                print('got chached data')
        else:
            std = Student(roll)
            std.fetch_data()
            if(std.name!='-' and std.cgpa!='0'):
                data.append(std)

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
    verify_folder(abs_path('./result/'+branch_name))

    data.sort(key=sort_sgpa,reverse=True)
    sys.stdout = open('result/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_sgpi.txt','w')
    print("sorting by sgpi....\n\n\n")
    print_data(data)

    data.sort(key=sort_cgpa,reverse=True)
    sys.stdout = open('result/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_cgpi.txt','w')
    print("sorting by cgpi....\n\n\n")
    print_data(data)

    sys.stdout = save_stdout
    print("written into files in result folder....\n\n")
    if(dump_it):
        dump_data(data,default_file_name)


def full_year(roll):
    data=[]
    y = get_year(roll)
    classes = get_class_set(y)
    verify_folder(abs_path('./result'))
    save_stdout = sys.stdout

    for roll in classes:
        class_data = get_data(roll)
        branch_name = get_branch_name(get_branch(roll))
        verify_folder(abs_path('./result/'+branch_name))

        class_data.sort(key=sort_sgpa,reverse=True)
        sys.stdout = open('result/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_sgpi.txt','w')
        print("sorting by sgpi....\n\n\n")
        print_data(class_data)

        class_data.sort(key=sort_cgpa,reverse=True)
        sys.stdout = open('result/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_cgpi.txt','w')
        print("sorting by cgpi....\n\n\n")
        print_data(class_data)

        data.extend(class_data)
        sys.stdout = save_stdout

    verify_folder(abs_path('./result/FULL_YEAR'))
    data.sort(key=sort_sgpa,reverse=True)
    sys.stdout = open('result/FULL_YEAR/full_year_'+get_year(roll)+'_sgpi.txt','w')
    print("sorting by sgpi....\n\n\n")
    print_data(data)

    data.sort(key=sort_cgpa,reverse=True)
    sys.stdout = open('result/FULL_YEAR/full_year_'+get_year(roll)+'_cgpi.txt','w')
    print("sorting by cgpi....\n\n\n")
    print_data(data)

    sys.stdout = save_stdout
    print("written into files in result folder....\n\n")
    if(dump_it):
        dump_data(data,default_file_name)

def full_college():
    data=[]
    by = base_year
    roll_set = []
    for b in range(0,4):
        roll_set.append(str(by-b)+'mi535')
    save_stdout = sys.stdout

    for roll in roll_set:
        year_data=[]
        y = get_year(roll)
        classes = get_class_set(y)
        verify_folder(abs_path('./result'))

        for roll in classes:
            class_data = get_data(roll)
            branch_name = get_branch_name(get_branch(roll))
            verify_folder(abs_path('./result/'+branch_name))

            class_data.sort(key=sort_sgpa,reverse=True)
            sys.stdout = open('result/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_sgpi.txt','w')
            print("sorting by sgpi....\n\n\n")
            print_data(class_data)

            class_data.sort(key=sort_cgpa,reverse=True)
            sys.stdout = open('result/'+branch_name+'/'+branch_name+'_'+get_year(roll)+'_cgpi.txt','w')
            print("sorting by cgpi....\n\n\n")
            print_data(class_data)

            year_data.extend(class_data)
            sys.stdout = save_stdout

        verify_folder(abs_path('./result/FULL_YEAR'))

        year_data.sort(key=sort_sgpa,reverse=True)
        sys.stdout = open('result/FULL_YEAR/full_year_'+get_year(roll)+'_sgpi.txt','w')
        print("sorting by sgpi....\n\n\n")
        print_data(year_data)

        year_data.sort(key=sort_cgpa,reverse=True)
        sys.stdout = open('result/FULL_YEAR/full_year_'+get_year(roll)+'_cgpi.txt','w')
        print("sorting by cgpi....\n\n\n")
        print_data(year_data)

        sys.stdout = save_stdout
        data.extend(year_data)

    verify_folder(abs_path('./result/FULL_COLLEGE'))
    data.sort(key=sort_sgpa,reverse=True)
    sys.stdout = open('result/FULL_COLLEGE/full_college_sgpi.txt','w')
    print("sorting by sgpi....\n\n\n")
    print_data(data)

    data.sort(key=sort_cgpa,reverse=True)
    sys.stdout = open('result/FULL_COLLEGE/full_college_cgpi.txt','w')
    print("sorting by cgpi....\n\n\n")
    print_data(data)

    sys.stdout = save_stdout
    print("written into files in result folder....\n\n")
    if(dump_it):
        dump_data(data,default_file_name)


if(__name__=="__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dump", action="store_true", help="used to dump the output to json file")
    parser.add_argument("-c", "--cached", action="store_true", help="use cached_data from json file")
    parser.add_argument("-f", "--file", default=default_file_name, help="name of json file to be written")
    parser.add_argument("-i", "--input", help="name of json file to be read")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-b", "--branch", action="store_true", help="full result of your branch")
    group.add_argument("-y", "--year", action="store_true", help="full result of your year")
    group.add_argument("-a", "--all", action="store_true", help="full result of college")

    parser.add_argument("-r", "--roll", help="ROLL number eg:- 15mi535")
    args = parser.parse_args()

    if(args.dump):
        dump_it = True

    if(args.roll):
        roll = args.roll
    else:
        roll = input('Enter your roll number : ')
        print('use: python3 nith_results.py -h for help')

    roll = roll.lower()
    std = Student(roll)
    std.fetch_data()
    print(std.get_result())

    default_file_name = args.file

    if(args.cached):
        if(args.input):
            create_std_map(args.input)
        else:
            create_std_map(args.file)
        print('created map')
    if(args.branch):
        full_class(roll)
    if(args.year):
        full_year(roll)
    if(args.all):
        full_college()
    print(Colour.PURPLE+'A script by srbcheema1'+Colour.END)
