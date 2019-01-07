#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import os
import sys

from srblib import show_dependency_error_and_exit
from srblib import SrbJson, debug, Colour, abs_path

try:
    import argparse
    from argcomplete import autocomplete
except:
    raise # till next release of srblib
    show_dependency_error_and_exit()

from .constants import default_no_of_std, iiitu_no_of_std, dual_no_of_std, base_year, get_branch_set, max_seats
from .output import write_data
from .student import Student
from . import __version__, __mod_name__


def sort_sgpa(std):
    return float(std.sgpa)
def sort_cgpa(std):
    return float(std.cgpa)

def get_branch_list(roll):
    miss = 0
    max_miss = 5
    data=[]
    if(Student._is_legacy_roll(roll)):
        a,b = 1,default_no_of_std
        if(roll[0]=='i'): b=iiitu_no_of_std
        if(roll[2]=='m'): b=dual_no_of_std
        temp = roll[:-2]
        for i in range(a,b):
            std = Student(temp+"%02d"%(i))
            ret = std.fetch_data()
            if(ret):
                data.append(std)
                miss = 0
            else:
                miss+=1
                if(miss > max_miss):break
        return data

    if(int(roll[3]) >= 5): base_int = int(roll[:3])*1000 + 500 # 185535
    else: base_int = int(roll[:3])*1000 # 185535
    for i in range(1,max_seats):
        std = Student(str(base_int+i))
        ret = std.fetch_data()
        if(ret):
            data.append(std)
            miss = 0
        else:
            miss+=1
            if(miss > max_miss):break
    return data


def full_class(roll):
    branch = Student.get_branch(roll)
    batch = Student.get_batch(roll)
    data= get_branch_list(roll)

    data.sort(key=sort_sgpa,reverse=True)
    fout = branch+'/batch_'+batch+'_sgpi'
    write_data(data,fout)

    data.sort(key=sort_cgpa,reverse=True)
    fout = branch+'/batch_'+batch+'_cgpi'
    write_data(data,fout)

    return data

def full_year(roll):
    data=[]
    batch = Student.get_batch(roll)
    for roll in get_branch_set(roll):
        data.extend(full_class(roll))

    data.sort(key=sort_sgpa,reverse=True)
    fout = '/FULL_YEAR/full_year_batch'+batch+'_sgpi'
    write_data(data,fout)

    data.sort(key=sort_cgpa,reverse=True)
    fout = '/FULL_YEAR/full_year_batch'+batch+'_cgpi'
    write_data(data,fout)

    return data


def full_college():
    data=[]
    by = base_year # prefix of first year
    for b in range(0,4):
        temp_roll = str(by-b) + 'mi535'
        if(by-b >= 18): temp_roll = str(by-b) + '5535'
        data.extend(full_year(temp_roll))

    data.sort(key=sort_sgpa,reverse=True)
    fout = 'FULL_COLLEGE/full_college_sgpi'
    write_data(data,fout)

    data.sort(key=sort_cgpa,reverse=True)
    fout = 'FULL_COLLEGE/full_college_cgpi'
    write_data(data,fout)

    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--version",action='store_true',help='Display version number')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-b", "--branch", action="store_true", help="full result of your branch")
    group.add_argument("-y", "--year", action="store_true", help="full result of your year")
    group.add_argument("-a", "--all", action="store_true", help="full result of college")
    # parser.add_argument("roll",nargs=1,help="your roll number") # this is for exactly one, it returns array of 1 elem
    parser.add_argument("roll",nargs='?',help="your roll number") # this is for one or none, it doesnot return array

    autocomplete(parser)
    args = parser.parse_args()

    if(args.version):
        print(__mod_name__+'=='+__version__)
        sys.exit()

    if(args.roll):
        roll = args.roll.lower()
        print(roll)
    else:
        roll = input('Enter your roll number : ')
    std = Student(roll)
    std.fetch_data()
    print(std)

    try:
        if(args.branch):
            full_class(roll)
        if(args.year):
            full_year(roll)
        if(args.all):
            full_college()
        if(args.all or args.branch or args.year):
            Colour.print("written into files in result folder....\n\n",Colour.GREEN)
    except KeyboardInterrupt:
        Colour.print('Exiting on KeyboardInterrupt ...',Colour.YELLOW)
    # Colour.print('A script by srbcheema1',Colour.PURPLE)

if(__name__=="__main__"):
    main()
