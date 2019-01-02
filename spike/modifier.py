#! /usr/bin/env python3

'''
whole file is out of sync
'''
from util.student import Student
from util.abs_path import abs_path
from util.srbjson import extract_data, create_info_dict

def edit_gender(std):
    if(std.gender == 'b' or std.gender == 'g'):
        return std.gender

    print(std.print_info())
    print("Enter new gender value b/g : ",end='')
    gender = input()
    if(gender == 'b' or gender == 'g'):
        return gender
    if(gender == 'q'):
        return 'q'
    return 'u'


def modifier(file_name=cache_path):
    data = extract_data()
    data = data['Students']
    for i in range(len(data)):
        item = data[i]
        std = Student(item['Rollno'])
        std.cached_data(item['Name'],item['Gender'],item['Sgpa'] \
            ,item['Cgpa'],item['Points'],item['Rank'],item['G_rank'])

        gender = edit_gender(std)
        if(gender == 'q'):
            break
        elif(gender == 'u'):
            std.gender = 'u'
        else:
            std.gender = gender

        data[i] = create_info_dict(std.rank,std)
    file_name = abs_path(file_name)
    create_file(file_name)
    new_data = extract_data()
    new_data['Students'] = data
    write_data(new_data) # removed method

if(__name__=="__main__"):
    modifier()
