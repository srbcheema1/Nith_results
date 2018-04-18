#!/usr/bin/env python3

import requests
import json

from os import environ
from bs4 import BeautifulSoup
from sys import argv, exit

from abs_path import abs_path
from srbColour import Colour

default_file_name = './results.json'

def get_year(roll):
    roll = str(roll)
    if(roll[0]=='i'):#iitu
        year = roll[5:7]
    else:
        year = roll[0:2]
    return year


def get_college(roll):
    roll = str(roll)
    if(roll[0]=='i'):#iitu
        college = "iiitu"
    else:
        college = "nith"
    return college


def get_c_id(roll):
    roll = str(roll)
    if(roll[0]=='i'):#iitu
        c_id="iiituna"
    else:
        c_id="scheme"
    return c_id


def get_num(roll):
    roll = str(roll)
    if(roll[2]=='m' or roll[2]=='M'):
        num=roll[5:7]
    elif(roll[0]=='i'):
        num=roll[8:10]
    else:
        num=roll[3:5]
    return num


def get_branch(roll):
    roll = str(roll)
    if(roll[2]=='m' or roll[2]=='M'):
        branch=roll[2:4].lower()
        branch+=str(roll[4])
    elif(roll[0]=='i'):
        branch=roll[7]
    else:
        branch=roll[2]
    return branch


def get_branch_name(branch):
    branch_data = {
            "1":"Civil",
            "2":"Electrical",
            "3":"Mechanical",
            "4":"Ece",
            "5":"Cse",
            "6":"Architecture",
            "7":"Chemical",
            "mi5":"Cse dual",
            "mi4":"Ece dual",
            "0":"unknown"
    }
    if(branch in branch_data):
        return branch_data[branch]
    else:
        return branch_data['0']


def get_curr_year(roll):
    # set base_year as year of 1st year students
    base_year = 17
    year = get_year(roll)
    curr_year = base_year - int(year) + 1
    return str(curr_year)


class Student:
    try:
        proxyDict = {
                    'http_proxy': environ['http_proxy'],
                    'https_proxy': environ['https_proxy'],
                    'ftp_proxy': environ['ftp_proxy']
                }
    except KeyError:
        proxyDict = None

    def __init__(self,roll):
        roll = str(roll)
        self.inflate_data(roll)

    def inflate_data(self,roll):
        self.year = get_year(roll)
        self.num = get_num(roll)
        self.branch = get_branch(roll)
        self.branch_name = get_branch_name(self.branch)
        self.c_id = get_c_id(roll)
        self.college = get_college(roll)
        self.roll_num = self.year+self.branch+self.num
        if(roll[0]=='i'):
            self.roll_num = "iiitu" + self.roll_num
        self.name = ""
        self.sgpa = ""
        self.cgpa = ""
        self.points = ""
        self.rank = '0'
        self.g_rank = '0'
        self.gender = ''

    def cached_data(self,name,gender,sgpa,cgpa,points,rank,g_rank):
        self.name = name
        self.sgpa = sgpa
        self.cgpa = cgpa
        self.points = points
        self.rank = rank
        self.g_rank = g_rank
        self.gender = gender

    def fetch_data(self):
        try:
            url = "http://14.139.56.15/"+self.c_id+self.year+"/studentresult/details.asp"
            page = requests.post(url,data={'RollNumber':self.roll_num},proxies=Student.proxyDict,verify=False)
            soup = BeautifulSoup(page.text,'lxml')
            self.all_data = soup.find_all(class_='ewTable')
            self.name=self.all_data[0].find_all('tr')[0].find_all('td')[1].text.strip()
            res = self.all_data[-1].find_all('tr')[1].find_all('td')
            self.sgpa = res[0].text.strip().split("=")[1]
            cgpa_ = res[2].text.strip()
            self.points = cgpa_.split("/")[0]
            self.cgpa = cgpa_.split("=")[1]
        except:
            self.name = '-'
            self.sgpa = self.points = self.cgpa = '0'

    def get_result(self):
        out = self.roll_num +"\n\t" + self.name + "\n\t" + self.sgpa + "\n\t" +self.points+ "\n\t" + self.cgpa
        return out


def sort_sgpa(std):
    return float(std.sgpa)
def sort_cgpa(std):
    return float(std.cgpa)


def get_data(roll):
    data=[]
    temp = roll[:-2]
    a,b = 1,90
    if(roll[0]=='i'):
        b=40
    if(roll[2]=='m'):
        b=65

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
