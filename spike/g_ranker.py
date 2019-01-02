#! /usr/bin/env python3
'''
whole file is out of sync
'''

from util.student import Student
from util.abs_path import abs_path
from util.srbjson import extract_data, write_data, create_info_dict, create_file
from util.string_constants import cache_path


def modifier(file_name=cache_path):
    data = extract_data()
    data = data['Students']
    b_rank = 1
    g_rank = 1
    for i in range(len(data)):
        item = data[i]
        std = Student(item['Rollno'])
        std.cached_data(item['Name'],item['Gender'],item['Sgpa'] \
            ,item['Cgpa'],item['Points'],item['Rank'],item['G_rank'])

        if(std.gender == 'b'):
            std.g_rank = b_rank
            b_rank +=1
        if(std.gender == 'g'):
            std.g_rank = g_rank
            g_rank +=1

        data[i] = create_info_dict(std.rank,std)
    file_name = abs_path(file_name)
    create_file(file_name)
    new_data = extract_data()
    new_data['Students'] = data
    write_data(new_data)

if(__name__=="__main__"):
    modifier()
