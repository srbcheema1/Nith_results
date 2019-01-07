from srblib import verify_file, abs_path, SrbJson

def create_info_dict(rank,std):
    info = {}
    info['Rank'] = str(rank)
    info['G_rank'] = std.g_rank
    info['Name'] = std.name
    info['Rollno'] = std.roll_num
    info['Gender'] = std.gender
    info['Year'] = std.year
    info['Cgpa'] = std.cgpa
    info['Sgpa'] = std.sgpa
    info['Points'] = std.points
    info['Branch'] = std.branch
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


def write_data(data,fout):
    dump_data(data,'result/json/'+fout+'.json')
    out = ""
    rank = 1
    for item in data:
        out+=str(rank)+" "+item.get_result()+"\n\n"
        rank+=1
    fout = abs_path('result/text/' + fout + '.txt')
    verify_file(fout)
    open(fout,'w').write(out)
