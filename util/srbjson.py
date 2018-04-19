import json

from util.getter import get_curr_year
from util.abs_path import abs_path
from util.string_constants import default_file_name

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
    """
    Extracts json data from the given file
    if there is no such file
        it will create one
    if there is currupt file
        it will create new
    if file is ok
        it will return its content
    """
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


def create_info_dict(rank,std):
    info = {}
    info['Rank'] = str(rank)
    info['G_rank'] = std.g_rank
    info['Name'] = std.name
    info['Rollno'] = std.roll_num
    info['Gender'] = std.gender
    info['Year'] = get_curr_year(std.roll_num)
    info['Cgpa'] = std.cgpa
    info['Sgpa'] = std.sgpa
    info['Points'] = std.points
    info['Branch_name'] = std.branch_name
    return info


def create_info_list(rank,std):
    info = []
    info.append({"Rank":str(rank)})
    info.append({"G_Rank":g_rank})
    info.append({"Name":std.name})
    info.append({"Rollno":std.roll_num})
    info.append({"Gender":std.gender})
    info.append({"Year":get_curr_year(std.roll_num)})
    info.append({"Cgpa":std.cgpa})
    info.append({"Sgpa":std.sgpa})
    info.append({"Points":std.points})
    info.append({"Branch_name":std.branch_name})
    return info


def write_data(data,file_name=default_file_name):
    """
    Write data into a json file
    """
    fille = abs_path(file_name)
    jfile = open(fille, 'w')
    json.dump(data,jfile,indent = 4,ensure_ascii = False)
    jfile.close()


def dump_data(data,file_name=default_file_name):
    """
    take a list of Students and burn it into json file
    """
    fille = abs_path(file_name)
    create_file(fille)
    dictt = extract_data()
    rank = 1
    for item in data:
        info = create_info_dict(rank,item)
        # info = create_info_list(rank,item)
        dictt['Students'].append(info)
        rank +=1
    write_data(dictt)

