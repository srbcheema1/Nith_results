#!/usr/bin/env python3

import json
from sys import argv, exit

from util.abs_path import abs_path
from util.srbColour import Colour
from util.student import Student
from util.getter import get_year, get_curr_year
from util.string_constants import default_file_name
from util.limits import default_no_of_std, iiitu_no_of_std, dual_no_of_std


def sort_sgpa(std):
    return float(std.sgpa)
def sort_cgpa(std):
    return float(std.cgpa)


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
            if(std.name!='-'):
                data.append(std)
            print('got chached data')
        else:
            std = Student(roll)
            std.fetch_data()
            if(std.name!='-'):
                data.append(std)

    return data


def print_data(data):
    rank = 1
    for item in data:
        print(rank,end=" ")
        print(item.get_result())
        print()
        rank +=1


def create_file(fille):
    template = {
        "Students":[
            # "roll_num":{
                # "Name":"name_of_std",
                # "Gender":"0",
                # "Year":"0",
                # "Rank_overall":"0",
                # "Gender_rank":"0",
                # "CGPI":"0",
                # "SGPI":"0",
                # "Points":"0",
                # "Branch_name":"name_of_branch"
            # }
        ]
    }
    jfile = open(fille, 'w')
    json.dump(template,jfile,indent = 4,ensure_ascii = False)
    jfile.close()


def extract_data(file_name=default_file_name):
    fille = abs_path(file_name)
    try:
        jfile = open(fille)
    except FileNotFoundError:
        create_file(fille)
    jfile = open(fille)
    data = json.load(jfile)
    if(not 'Students' in data.keys()):
        create_file(fille)
        jfile = open(fille)
        data = json.load(jfile)
    return data


std_map = {}
def create_std_map():
    data = extract_data()
    data = data['Students']
    global std_map
    for item in data:
        std = Student(item['Rollno'])
        std.cached_data(item['Name'],item['Gender'],item['Sgpa'] \
            ,item['Cgpa'],item['Points'],item['Rank'],item['G_rank'])
        std_map[item['Rollno']] = std


def create_info_dict(rank,std):
    info = {}
    info['Rank'] = str(rank)
    info['G_rank'] = ""
    info['Name'] = std.name
    info['Rollno'] = std.roll_num
    info['Gender'] = ""
    info['Year'] = get_curr_year(std.roll_num)
    info['Cgpa'] = std.cgpa
    info['Sgpa'] = std.sgpa
    info['Points'] = std.points
    info['Branch_name'] = std.branch_name
    return info


def create_info_list(rank,std):
    info = []
    info.append({"Rank":str(rank)})
    info.append({"G_Rank":""})
    info.append({"Name":std.name})
    info.append({"Rollno":std.roll_num})
    info.append({"Gender":''})
    info.append({"Year":get_curr_year(std.roll_num)})
    info.append({"Cgpa":std.cgpa})
    info.append({"Sgpa":std.sgpa})
    info.append({"Points":std.points})
    info.append({"Branch_name":std.branch_name})
    return info


def write_data(data,file_name=default_file_name):
    fille = abs_path(file_name)
    jfile = open(fille, 'w')
    json.dump(data,jfile,indent = 4,ensure_ascii = False)
    jfile.close()


def dump_data(data,file_name=default_file_name):
    fille = abs_path(file_name)
    create_file(fille)
    dictt = extract_data()
    rank = 1
    for item in data:
        info = create_info_dict(rank,item)
        # info = create_info_list(rank,item)
        dictt['Students'].append(info)
        rank +=1
    # print(dictt)
    write_data(dictt)


def full_class(roll):
    data=[]
    data.extend(get_data(roll))

    data.sort(key=sort_sgpa,reverse=True)
    print("sorting by sgpi....\n\n\n")
    print_data(data)

    data.sort(key=sort_cgpa,reverse=True)
    print("sorting by cgpi....\n\n\n")
    print_data(data)
    dump_data(data)


def full_year(roll):
    y = get_year(roll)
    classes = [y+'101',y+'201',y+'301',y+'401',y+'501',y+'601',y+'701',y+'mi501',y+'mi401','iiitu'+y+'101']
    data=[]
    for roll in classes:
        data.extend(get_data(roll))

    data.sort(key=sort_cgpa,reverse=True)
    dump_data(data)


if(__name__=="__main__"):
    ans = 'n'
    if(len(argv)==2):
        roll=argv[1]
        ans = 'y'
    else:
        print("enter ur roll : ",end='')
        roll = str(input())
        roll = roll.lower()
        print("do you want relult of whole class y or n : ",end='')
        ans = input()

    std = Student(roll)
    std.fetch_data()
    print(std.get_result())

    if(ans!='y'):
        exit()

    create_std_map()
    # full_class(roll)
    full_year(roll)
