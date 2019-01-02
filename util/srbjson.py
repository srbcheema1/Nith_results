import json

from util.getter import get_curr_year

from srblib import verify_file, abs_path, SrbJson

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


def dump_data(data,file_name):
    """
    take a LIST of Students and burn it into json file
    create RAW data from LIST
    creates totally new file
    """
    jfile = SrbJson(file_name,[])
    jfile.data = []
    jfile._burn_data_to_file() # force empty
    rank = 1
    for item in data:
        info = create_info_dict(rank,item)
        jfile.data.append(info) # using jfile.data instead of jfile to speed up
        rank +=1
    jfile._burn_data_to_file() # required if we are using jfile.data

